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
import os
import time
from collections import Counter, defaultdict
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent.parent
DOCS_DIR = _ROOT / "docs"
EXAMPLES_DIR = DOCS_DIR / "examples"
VITEPRESS_DIR = DOCS_DIR / ".vitepress"
PUBLIC_EXAMPLES_DIR = DOCS_DIR / "public" / "examples"
DEFAULT_EXPERIMENTS = _ROOT / "vendor" / "experiments.jsonl"

# Deployment base path (e.g. "/vtk-python-examples/" for a GitHub project site).
# VitePress auto-prefixes Markdown links/images and sidebar/nav entries with the
# configured base, but it does NOT rewrite raw HTML (<a href>, <img src>) that we
# emit below — so we prefix those root-absolute paths manually with this base.
BASE = "/" + os.environ.get("DOCS_BASE", "/").strip("/")
if BASE != "/":
    BASE += "/"


# ── Helpers ──────────────────────────────────────────────────────────

def _with_base(path: str) -> str:
    """Prefix a root-absolute path with the deployment base (for raw HTML only)."""
    return BASE.rstrip("/") + path


def _image_path(tag: str, image: str, size: str = "180") -> str:
    """Return path to pre-generated thumbnail or original image."""
    if not image:
        return ""
    base = image.replace(".png", "")
    thumb_path = PUBLIC_EXAMPLES_DIR / tag / f"{base}.thumb{size}.jpg"
    if thumb_path.exists():
        return f"/examples/{tag}/{base}.thumb{size}.jpg"
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


def _esc_html(s: str) -> str:
    """Escape characters that VitePress/Vue would otherwise interpret, so that
    parser-derived text renders literally. This covers:
      - HTML tags/directives: ``<image>`` -> ``&lt;image&gt;``
      - attribute blocks (markdown IAL): a trailing ``{:6.1f}`` would become a
        ``<td :6.1f="">`` directive, so curly braces are escaped too."""
    return (
        str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace("{", "&#123;")
        .replace("}", "&#125;")
    )


def _esc_pipe(s: str) -> str:
    return _esc_html(s).replace("|", "\\|").replace("\n", " ")


# Cap pathologically long single-line values (e.g. PointsDefinition coordinate
# arrays with thousands of entries). Emitting them verbatim produces multi-KB
# single lines that, after syntax highlighting, become AST expressions deep
# enough to overflow Rollup's call stack during the production build.
_MAX_VALUE_LEN = 2000


def _truncate(s: str, limit: int = _MAX_VALUE_LEN) -> str:
    s = str(s)
    if len(s) <= limit:
        return s
    return s[:limit] + f" … [truncated {len(s) - limit} chars]"


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
    lines = ["---", f"title: {section_label}", "layout: page", "---", ""]
    lines.append("<script setup>")
    lines.append("import examplesByCategory from '/.vitepress/generated/examples.mjs'")
    lines.append("</script>")
    lines.append("")
    lines.append("<div class=\"examples-page\">")
    lines.append("")
    lines.append(f"# {section_label}")
    lines.append("")
    lines.append("Browse all VTK Python examples by category. Click any title to view the DSL, source code, and event details.")
    lines.append("")
    
    # Get sorted categories
    by_cat: dict[str, list] = defaultdict(list)
    for r in results:
        by_cat[r["tag"]].append(r)
    
    for cat in sorted(by_cat.keys()):
        lines.append(f"<ExamplesTable category=\"{cat}\" :examples=\"examplesByCategory['{cat}']\" />")
        lines.append("")
    
    lines.append("</div>")
    return "\n".join(lines)


# ── Detail page ──────────────────────────────────────────────────────

def build_detail_md(r: dict) -> str:
    title = r["title"]
    tag = r["tag"]
    base = r["base"]
    
    lines = [
        "---",
        f'title: "{title}"',
        "layout: page",
        "---",
        "",
        "<script setup>",
        f"import example from '/.vitepress/generated/examples/{tag}/{base}.mjs'",
        "</script>",
        "",
        "<ExampleDetail :example=\"example\" />",
    ]
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
            entry["image"] = _image_path(r["tag"], r["image"], size="180")
            entry["imageSmall"] = _image_path(r["tag"], r["image"], size="44")
        gallery.append(entry)
    return gallery


def build_examples_data(results: list[dict]) -> dict:
    """Build examples data grouped by category."""
    by_cat: dict[str, list] = defaultdict(list)
    for r in results:
        entry: dict = {
            "title": r["title"],
            "category": r["tag"],
            "link": f"/examples/{r['tag']}/{r['base']}",
            "n_events": r.get("n_events", 0),
            "n_phrases": r.get("n_phrases", 0),
            "topology": r.get("topology", "?"),
        }
        if _image_exists(r["tag"], r.get("image")):
            entry["imageSmall"] = _image_path(r["tag"], r["image"], size="44")
        by_cat[r["tag"]].append(entry)
    
    # Sort examples within each category
    for cat in by_cat:
        by_cat[cat] = sorted(by_cat[cat], key=lambda x: x["title"])
    
    return dict(by_cat)


def build_example_detail_data(r: dict) -> dict:
    """Build detailed data for a single example."""
    tag = r["tag"]
    base = r["base"]
    
    entry: dict = {
        "title": r["title"],
        "tag": tag,
        "base": base,
        "topology": r.get("topology", "?"),
        "n_events": r.get("n_events", 0),
        "n_phrases": r.get("n_phrases", 0),
        "description": r.get("explanation", "").strip().replace("Description\n", "").replace("Description:", ""),
    }
    
    # Image
    if _image_exists(tag, r.get("image")):
        entry["image"] = _image_path(tag, r["image"], size="180")
    
    # VTK classes
    vtk_classes = []
    for cls in r.get("vtk_classes", []):
        vtk_classes.append({
            "name": cls,
            "link": f"https://www.vtk.org/doc/nightly/html/class{cls}.html",
            "description": "",  # Could add descriptions if available
        })
    entry["vtkClasses"] = vtk_classes
    
    # Pipeline description
    entry["pipeline"] = r.get("pipeline", "")
    
    # Data files
    data_files = []
    for df in r.get("data_files", []):
        name = df.rstrip("/").split("/")[-1]
        # Use GitHub release URL for data files
        release_url = f"https://github.com/patrickoleary/vtk-python-examples/releases/download/data-v1/{name}"
        data_files.append({
            "name": name,
            "path": release_url,
        })
    entry["dataFiles"] = data_files
    
    # Source
    py = r.get("py_filename")
    if py:
        entry["sourcePath"] = f"/examples/{tag}/{py}"
        entry["sourceFile"] = py
        entry["sourceCode"] = r.get("code", "")
    
    # DSL
    phrases = r.get("phrases", [])
    if phrases:
        entry["dsl"] = " and ".join(phrases)
    
    # Event actions
    event_actions = []
    for i, ev in enumerate(r.get("events", []), 1):
        action: dict = {
            "index": i,
            "phase": ev.get("phase", ""),
            "type": ev.get("class_name", ""),
            "label": ev.get("label", ""),
            "dsl": ev.get("dsl_phrase", ""),
            "line": ev.get("line", ""),
            "vtkClass": ", ".join(ev.get("vtk_objects", [])),
            "verb": ev.get("verb", ""),
            "noun": ev.get("noun", ""),
            "properties": ev.get("properties", {}),
        }
        event_actions.append(action)
    entry["eventActions"] = event_actions
    
    return entry


def build_sidebar(results: list[dict]) -> dict:
    by_cat: dict[str, list] = defaultdict(list)
    for r in results:
        by_cat[r["tag"]].append(r)
    items = []
    for cat in sorted(by_cat.keys()):
        cat_items = sorted(by_cat[cat], key=lambda x: x["title"])
        items.append({
            "text": f"{cat} ({len(cat_items)})",
            "link": f"/examples/#{cat}",
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

    tagline = (
        f"A browsable gallery of VTK Python examples. {n:,} examples across "
        f"{n_tags} categories, mapped to a visualization DSL."
    )

    lines = [
        "---",
        "layout: page",
        "title: VTK Python Examples",
        "---",
        "",
        "<script setup>",
        "import gallery from './.vitepress/generated/gallery.mjs'",
        "</script>",
        "",
        '<div class="trapezoid-hero">',
        '  <div class="trapezoid-hero-text">',
        '    <h1 class="trapezoid-hero-title">VTK Python Examples</h1>',
        f'    <p class="trapezoid-hero-tagline">{tagline}</p>',
        '    <div class="trapezoid-hero-actions">',
        f'      <a href="{_with_base("/gallery")}" class="trapezoid-btn trapezoid-btn-brand">Browse the Gallery</a>',
        f'      <a href="{_with_base("/examples/")}" class="trapezoid-btn trapezoid-btn-alt">All examples</a>',
        "    </div>",
        "  </div>",
        '  <TrapezoidGallery :examples="gallery" />',
        "</div>",
        "",
    ]

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
    examples_data = build_examples_data(results)
    (gen_dir / "examples.mjs").write_text(
        "export default " + json.dumps(examples_data, indent=2) + "\n", encoding="utf-8"
    )
    
    # Individual example detail data files
    examples_gen_dir = gen_dir / "examples"
    examples_gen_dir.mkdir(parents=True, exist_ok=True)
    for r in results:
        tag = r["tag"]
        base = r["base"]
        tag_dir = examples_gen_dir / tag
        tag_dir.mkdir(parents=True, exist_ok=True)
        detail_data = build_example_detail_data(r)
        (tag_dir / f"{base}.mjs").write_text(
            "export default " + json.dumps(detail_data, indent=2) + "\n", encoding="utf-8"
        )

    print(f"  Landing: docs/index.md")
    print(f"  Examples: {len(results)} detail pages")
    print(f"  Gallery: {len(gallery_data)} entries")
    print(f"  Sidebar: {sidebar_path}")
    print(f"Done in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
