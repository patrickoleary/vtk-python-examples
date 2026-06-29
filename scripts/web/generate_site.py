#!/usr/bin/env python3
"""Generate the VitePress example site from the corpus + slim experiments.jsonl.

Data sources:
  vendor/experiments.jsonl                    — per-example events/phrases/DSL
                                                (fetched from vtk-ontology release)
  docs/public/examples/{tag}/{name}.json      — metadata (explanation, image, symbols)
  docs/public/examples/{tag}/{name}.py        — source code
  docs/public/examples/{tag}/{name}.png       — rendered image (served in place)

Produces:
  docs/index.md                       — landing page (hero + stats + featured)
  docs/examples/index.md              — examples listing
  docs/examples/{tag}/{name}.md       — per-example detail pages
  docs/.vitepress/sidebar.json        — auto-generated sidebar
  docs/.vitepress/generated/gallery.mjs — gallery data for ExampleGallery.vue

Usage:
    python -m scripts.web.generate_site
    python -m scripts.web.generate_site --experiments vendor/experiments.jsonl
    python -m scripts.web.generate_site --tag filtering --limit 10
"""
from __future__ import annotations

import argparse
import json
import time
from collections import Counter, defaultdict
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = _ROOT / "docs"
EXAMPLES_DIR = DOCS_DIR / "examples"
VITEPRESS_DIR = DOCS_DIR / ".vitepress"
PUBLIC_EXAMPLES_DIR = DOCS_DIR / "public" / "examples"
DEFAULT_EXPERIMENTS = _ROOT / "vendor" / "experiments.jsonl"


# ── Helpers ──────────────────────────────────────────────────────────

def _image_path(tag: str, image: str) -> str:
    return f"/examples/{tag}/{image}"


def _image_exists(tag: str, image: str) -> bool:
    return bool(image) and (PUBLIC_EXAMPLES_DIR / tag / image).exists()


def _load_metadata(tag: str, base: str) -> dict:
    path = PUBLIC_EXAMPLES_DIR / tag / f"{base}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _load_code(tag: str, base: str) -> str:
    path = PUBLIC_EXAMPLES_DIR / tag / f"{base}.py"
    if path.exists():
        return path.read_text(encoding="utf-8")
    return ""


def _esc_pipe(s: str) -> str:
    return str(s).replace("|", "\\|").replace("\n", " ")


_NO_BREAK_AFTER = {
    "called", "with", "the", "from", "to",
    "create", "define", "add", "apply", "fashion", "forge", "launch",
    "load", "read", "write", "save", "show", "build", "use",
    "generate", "declare",
}


def _word_wrap(text: str, width: int = 80) -> list[str]:
    words = text.split()
    result: list[str] = []
    current: list[str] = []
    length = 0
    i = 0
    while i < len(words):
        word = words[i]
        if word in _NO_BREAK_AFTER and i + 1 < len(words):
            word = word + " " + words[i + 1]
            i += 1
        if current and length + 1 + len(word) > width:
            result.append(" ".join(current))
            current = [word]
            length = len(word)
        else:
            current.append(word)
            length += (1 if current[:-1] else 0) + len(word)
        i += 1
    if current:
        result.append(" ".join(current))
    return result


# ── Listing (examples/index.md) ──────────────────────────────────────

def build_listing_md(section_label: str, results: list[dict]) -> str:
    lines = ["---", f"title: {section_label}", "---", "", f"# {section_label}", ""]
    by_cat: dict[str, list] = defaultdict(list)
    for r in results:
        by_cat[r["tag"]].append(r)

    for cat in sorted(by_cat.keys()):
        items = sorted(by_cat[cat], key=lambda x: x["title"])
        lines.append(f"## {cat} ({len(items)})")
        lines.append("")
        lines.append("| Title | Events | Phrases | Topology |")
        lines.append("| --- | ---: | ---: | --- |")
        for r in items:
            link = f"./{r['tag']}/{r['base']}"
            if _image_exists(r["tag"], r.get("image")):
                thumb = (
                    f'<a href="{link}"><img src="{_image_path(r["tag"], r["image"])}" '
                    f'alt="{r["title"]}" '
                    'style="width:44px;height:44px;min-width:44px;object-fit:cover;'
                    'border-radius:4px;vertical-align:middle;display:inline-block" /></a>'
                )
            else:
                thumb = "—"
            lines.append(
                f"| {thumb} [{r['title']}]({link}) | {r['n_events']} | "
                f"{r['n_phrases']} | {r.get('topology', '?')} |"
            )
        lines.append("")

    return "\n".join(lines)


# ── Detail page ──────────────────────────────────────────────────────

def build_detail_md(r: dict) -> str:
    title = r["title"]
    tag = r["tag"]
    topology = r.get("topology", "?")

    lines = [
        "---",
        f'title: "{title}"',
        "---",
        "",
        f"# {title}",
        "",
        f"> Tag: {tag} · Topology: **{topology}** · "
        f"{r.get('n_events', 0)} events · {r.get('n_phrases', 0)} phrases",
        "",
    ]

    image = r.get("image")
    if _image_exists(tag, image):
        lines += [f"![{title}]({_image_path(tag, image)})", ""]

    explanation = r.get("explanation", "")
    if explanation:
        lines += [explanation.strip(), ""]

    data_files = r.get("data_files") or []
    if data_files:
        lines += ["### Data files", ""]
        for df in data_files:
            name = df.rstrip("/").split("/")[-1]
            lines.append(f'- <a href="/examples/{df}" target="_blank">{name}</a>')
        lines.append("")

    py = r.get("py_filename")
    if py:
        lines += [f'**Source:** <a href="/examples/{tag}/{py}" target="_blank">{py}</a>', ""]

    # DSL (collapsible)
    phrases = r.get("phrases", [])
    lines += ["### DSL", "", "<details>", ""]
    if phrases:
        joined = " and ".join(phrases)
        lines.append("```vtk-dsl")
        lines.extend(_word_wrap(joined, 75))
        lines.append("```")
    else:
        lines.append("*No DSL phrases generated.*")
    lines += ["", "</details>", ""]

    # Source code (collapsible)
    code = r.get("code", "")
    if code:
        lines += ["### Source Code", "", "<details>", "", "```python", code, "```", "", "</details>", ""]

    # Event actions (collapsible)
    events = r.get("events", [])
    lines += [f"### Event Actions ({len(events)})", "", "<details>", ""]
    for i, ev in enumerate(events, 1):
        phase = ev["phase"]
        class_name = ev["class_name"]
        label = ev.get("label", "")
        dsl = ev.get("dsl_phrase", "")
        props = ev.get("properties", {})
        label_str = f' "{label}"' if label else ""
        lines.append("<details>")
        lines.append(f"<summary>#{i} · {phase} · <b>{class_name}</b>{label_str}</summary>")
        lines.append("")
        if dsl:
            lines += ["```vtk-dsl", dsl, "```", ""]
        if ev.get("line") not in (None, ""):
            lines.append(f"- **line:** {ev['line']}")
        if ev.get("vtk_objects"):
            lines.append(f"- **vtk class:** {', '.join(ev['vtk_objects'])}")
        lines.append(f"- **verb:** {ev.get('verb', '')}")
        lines.append(f"- **noun:** {ev.get('noun', '')}")
        if ev.get("sources"):
            lines.append(f"- **source:** {', '.join(ev['sources'])}")
        if label:
            lines.append(f"- **label:** {label}")
        lines.append("")
        if props:
            lines += ["| Property | Value |", "| --- | --- |"]
            for k, v in props.items():
                lines.append(f"| {_esc_pipe(k)} | {_esc_pipe(str(v))} |")
            lines.append("")
        lines += ["</details>", ""]
    lines += ["</details>", ""]

    return "\n".join(lines)


# ── Gallery + sidebar ────────────────────────────────────────────────

def build_gallery_data(results: list[dict]) -> list[dict]:
    gallery = []
    for r in results:
        entry: dict = {
            "title": r["title"],
            "category": r["tag"],
            "link": f"/examples/{r['tag']}/{r['base']}",
        }
        if _image_exists(r["tag"], r.get("image")):
            entry["image"] = _image_path(r["tag"], r["image"])
        gallery.append(entry)
    return gallery


def build_sidebar(results: list[dict]) -> dict:
    by_cat: dict[str, list] = defaultdict(list)
    for r in results:
        by_cat[r["tag"]].append(r)
    items = []
    for cat in sorted(by_cat.keys()):
        cat_items = sorted(by_cat[cat], key=lambda x: x["title"])
        items.append({
            "text": f"{cat} ({len(cat_items)})",
            "collapsed": True,
            "items": [
                {"text": r["title"], "link": f"/examples/{r['tag']}/{r['base']}"}
                for r in cat_items
            ],
        })
    return {
        "/examples/": [{
            "text": "Examples",
            "items": [{"text": "Overview", "link": "/examples/"}, *items],
        }]
    }


# ── Landing page (index.md) ──────────────────────────────────────────

def build_landing_md(results: list[dict]) -> str:
    n = len(results)
    by_cat: dict[str, int] = Counter(r["tag"] for r in results)
    n_tags = len(by_cat)
    n_phrases = sum(r["n_phrases"] for r in results)
    featured = [r for r in results if _image_exists(r["tag"], r.get("image"))][:6]

    lines = [
        "---",
        "layout: home",
        "title: VTK Python Examples",
        "hero:",
        "  name: VTK Python Examples",
        "  text: A browsable gallery of VTK Python examples",
        f"  tagline: {n:,} examples across {n_tags} categories, mapped to a visualization DSL",
        "  actions:",
        "    - theme: brand",
        "      text: Browse the Gallery",
        "      link: /gallery",
        "    - theme: alt",
        "      text: All examples",
        "      link: /examples/",
        "features:",
        f"  - title: {n:,} examples",
        "    details: Real VTK Python scripts with rendered output, organized by category.",
        f"  - title: {n_tags} categories",
        "    details: From annotation and filtering to rendering, modelling, and IO.",
        f"  - title: {n_phrases:,} DSL phrases",
        "    details: Each example is parsed into declarative DSL phrases and pipeline events.",
        "---",
        "",
    ]

    if featured:
        lines += ["", "## Featured", "", '<div class="gallery-grid">']
        for r in featured:
            link = f"/examples/{r['tag']}/{r['base']}"
            img = _image_path(r["tag"], r["image"])
            lines += [
                '<div class="gallery-card">',
                f'<a href="{link}">',
                f'<img src="{img}" alt="{r["title"]}" loading="lazy" />',
                '<div class="card-body">',
                f'<p class="card-title">{r["title"]}</p>',
                f'<p class="card-category">{r["tag"]}</p>',
                "</div></a></div>",
            ]
        lines += ["</div>", ""]

    return "\n".join(lines)


# ── Main ─────────────────────────────────────────────────────────────

def load_experiments(path: Path) -> list[dict]:
    examples = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                examples.append(json.loads(line))
    return examples


def main() -> None:
    ap = argparse.ArgumentParser(description="Generate the VitePress example site")
    ap.add_argument("--experiments", default=str(DEFAULT_EXPERIMENTS),
                    help="Path to slim experiments.jsonl")
    ap.add_argument("--tag", help="Filter by tag")
    ap.add_argument("--title", help="Filter by title substring")
    ap.add_argument("--limit", type=int, help="Limit number of examples")
    args = ap.parse_args()

    exp_path = Path(args.experiments)
    if not exp_path.exists():
        raise SystemExit(
            f"ERROR: {exp_path} not found. Fetch it from a vtk-ontology release "
            f"(see scripts/fetch_artifacts.py) or pass --experiments."
        )

    t0 = time.time()
    examples = load_experiments(exp_path)
    if args.tag:
        examples = [e for e in examples if e.get("tag") == args.tag]
    if args.title:
        examples = [e for e in examples if args.title.lower() in e.get("title", "").lower()]
    if args.limit:
        examples = examples[:args.limit]

    print(f"Processing {len(examples)} examples from {exp_path.name}...")

    results: list[dict] = []
    for ex in examples:
        tag = ex.get("tag", "?")
        title = ex.get("title", "?")
        base = Path(ex.get("py_filename") or title).stem
        events = ex.get("events", [])
        phrases = ex.get("phrases", [])
        meta = _load_metadata(tag, base)

        ev_list = []
        for idx, ev in enumerate(events):
            ev = dict(ev)
            ev["dsl_phrase"] = phrases[idx] if idx < len(phrases) else ""
            ev_list.append(ev)

        results.append({
            "title": title,
            "tag": tag,
            "base": base,
            "topology": ex.get("topology", "?"),
            "image": meta.get("image"),
            "explanation": meta.get("explanation", ""),
            "code": _load_code(tag, base),
            "py_filename": ex.get("py_filename"),
            "data_files": meta.get("data_files") or [],
            "n_events": len(events),
            "n_phrases": len(phrases),
            "phrases": phrases,
            "events": ev_list,
        })

    # Landing page
    (DOCS_DIR / "index.md").write_text(build_landing_md(results), encoding="utf-8")

    # Listing + detail pages
    EXAMPLES_DIR.mkdir(parents=True, exist_ok=True)
    (EXAMPLES_DIR / "index.md").write_text(build_listing_md("Examples", results), encoding="utf-8")
    for r in results:
        tag_dir = EXAMPLES_DIR / r["tag"]
        tag_dir.mkdir(parents=True, exist_ok=True)
        (tag_dir / f"{r['base']}.md").write_text(build_detail_md(r), encoding="utf-8")

    # Sidebar
    sidebar_path = VITEPRESS_DIR / "sidebar.json"
    sidebar_path.write_text(json.dumps(build_sidebar(results), indent=2), encoding="utf-8")

    # Gallery data
    gen_dir = VITEPRESS_DIR / "generated"
    gen_dir.mkdir(parents=True, exist_ok=True)
    gallery_data = build_gallery_data(results)
    (gen_dir / "gallery.mjs").write_text(
        "export default " + json.dumps(gallery_data, indent=2) + "\n", encoding="utf-8"
    )

    print(f"  Landing: docs/index.md")
    print(f"  Examples: {len(results)} detail pages")
    print(f"  Gallery: {len(gallery_data)} entries")
    print(f"  Sidebar: {sidebar_path}")
    print(f"Done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
