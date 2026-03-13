"""
Rebuild all documentation artifacts from test_manifest.json.

This is the **single command** to run after adding or modifying examples:

    uv run python scripts/generate_examples_jsonl.py

It reads:
    src/tests/test_manifest.json          (the single source of truth)
    src/Python/{category}/{title}.py      (source code)
    src/Python/{category}/{title}.md      (companion description)
    data/images/testing/{output_image}    (test screenshots)

It writes:
    data/examples.jsonl                              (full JSONL dataset)
    docs/.vitepress/generated/gallery.mjs            (gallery data for Vue)
    docs/.vitepress/generated/sidebar.mjs            (sidebar config for VitePress)
    docs/public/images/{output_image}                (screenshot copies for the site)
    docs/public/data/{data_file}                     (data file copies for the site)
    docs/examples/{category}/{title}.md              (per-example VitePress pages)
    docs/index.md                                    (updated example count)
"""

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "src" / "tests" / "test_manifest.json"
EXAMPLES_DIR = ROOT / "src" / "Python"
DOCS = ROOT / "docs"

# Output paths
JSONL_OUTPUT = ROOT / "data" / "examples.jsonl"
GENERATED_DIR = DOCS / ".vitepress" / "generated"
PUBLIC_IMAGES = DOCS / "public" / "images"
PUBLIC_DATA = DOCS / "public" / "data"
PAGES_DIR = DOCS / "examples"

BASE_URL = "https://github.com/Kitware/vtk-python-examples"
PAGES_URL = "https://kitware.github.io/vtk-python-examples"
SITE_BASE = "/vtk-python-examples"

CATEGORY_LABELS = {
    "Annotation": "Annotation",
    "Arrays": "Arrays",
    "CompositeData": "Composite Data",
    "DataManipulation": "Data Manipulation",
    "ExplicitStructuredGrid": "Explicit Structured Grid",
    "Filtering": "Filtering",
    "GeometricObjects": "Geometric Objects",
    "Graphs": "Graphs",
    "Grids": "Grids",
    "HyperTreeGrid": "Hyper Tree Grid",
    "ImageData": "Image Data",
    "ImageProcessing": "Image Processing",
    "Images": "Images",
    "ImplicitFunctions": "Implicit Functions",
    "Importers": "Importers",
    "Interaction": "Interaction",
    "Medical": "Medical",
    "Meshes": "Meshes",
    "Modeling": "Modeling",
    "Picking": "Picking",
    "Plotting": "Plotting",
    "PolyData": "PolyData",
    "Rendering": "Rendering",
    "ScalarVisualization": "Scalar Visualization",
    "SimpleOperations": "Simple Operations",
    "SpecialTopics": "Special Topics",
    "SurfaceOperations": "Surface Operations",
    "Texture": "Texture",
    "Tutorial": "Tutorial",
    "Utilities": "Utilities",
    "VectorVisualization": "Vector Visualization",
    "Visualization": "Visualization",
    "VolumeRendering": "Volume Rendering",
    "Widgets": "Widgets",
    "Qt": "Qt",
    "IO": "IO",
}


def extract_short_description(explanation: str | None) -> str:
    """Return the first paragraph after the ### Description header."""
    if not explanation:
        return ""
    # Strip the ### Description header
    text = re.sub(r"^###\s+Description\s*\n+", "", explanation.strip())
    # Take everything up to the first blank line (end of first paragraph)
    first_para = text.split("\n\n")[0]
    # Collapse to single line and strip markdown links to plain text
    line = " ".join(first_para.split())
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    return line


def extract_vtk_symbols(code: str) -> list[str]:
    """Extract VTK symbol names from import statements."""
    symbols = set()

    # Match: from vtkmodules.xxx import (Foo, Bar)
    for m in re.finditer(
        r"from\s+vtkmodules\.\S+\s+import\s+\(([^)]+)\)", code, re.DOTALL
    ):
        for name in re.findall(r"\b(vtk\w+)\b", m.group(1)):
            symbols.add(name)

    # Match single-line: from vtkmodules.xxx import Foo, Bar
    for m in re.finditer(
        r"from\s+vtkmodules\.\S+\s+import\s+(.+)$", code, re.MULTILINE
    ):
        for name in re.findall(r"\b(vtk\w+)\b", m.group(1)):
            symbols.add(name)

    return sorted(symbols)


def main():
    manifest = json.loads(MANIFEST.read_text())

    # Clean generated directories so stale files never linger
    for d in [PAGES_DIR, PUBLIC_IMAGES]:
        if d.exists():
            shutil.rmtree(d)
    vitepress_cache = DOCS / ".vitepress" / "cache"
    if vitepress_cache.exists():
        shutil.rmtree(vitepress_cache)

    # Ensure output directories exist
    for d in [JSONL_OUTPUT.parent, GENERATED_DIR, PUBLIC_IMAGES, PUBLIC_DATA]:
        d.mkdir(parents=True, exist_ok=True)

    records = []
    gallery_items = []
    sidebar_by_category: dict[str, list[dict]] = {}

    for entry in manifest:
        category = entry["category"]
        title = entry["title"]
        script_path = ROOT / entry["script_path"]
        output_image = entry["output_image"]
        data_file_names = entry.get("data_files", None)

        # Read source code
        code = ""
        if script_path.exists():
            code = script_path.read_text()

        # Read companion .md description
        md_path = EXAMPLES_DIR / category / f"{title}.md"
        explanation = None
        if md_path.exists():
            explanation = md_path.read_text().strip()

        # Extract VTK symbols
        uses_symbols = extract_vtk_symbols(code)

        # Build image URL (GitHub Pages)
        image_url = f"{PAGES_URL}/images/{output_image}"

        # Build data file URLs
        # Directories are zipped for website distribution
        # data_files_abs  → absolute URLs for JSONL (external consumers)
        # data_files_rel  → site-relative paths for markdown pages (works in dev + prod)
        data_files_abs = None
        data_files_rel = None
        if data_file_names:
            script_dir = ROOT / entry["script_path"]
            data_files_abs = []
            data_files_rel = []
            for f in data_file_names:
                src = script_dir.parent / f
                if src.is_dir():
                    data_files_abs.append(f"{PAGES_URL}/data/{f}.zip")
                    data_files_rel.append(f"{SITE_BASE}/data/{f}.zip")
                else:
                    data_files_abs.append(f"{PAGES_URL}/data/{f}")
                    data_files_rel.append(f"{SITE_BASE}/data/{f}")

        # ------------------------------------------------------------------
        # 1. JSONL record
        # ------------------------------------------------------------------
        records.append({
            "id": f"{BASE_URL}/blob/main/{entry['script_path']}",
            "source_type": "example",
            "language": "Python",
            "category": category,
            "title": title,
            "explanation": explanation,
            "code": code,
            "image_url": image_url,
            "uses_symbols": uses_symbols,
            "data_files": data_files_abs,
        })

        # ------------------------------------------------------------------
        # 2. Copy screenshot to docs/public/images/
        # ------------------------------------------------------------------
        img_src = ROOT / "data" / "images" / "testing" / output_image
        image_site_path = None
        if img_src.exists():
            shutil.copy2(img_src, PUBLIC_IMAGES / output_image)
            image_site_path = f"/images/{output_image}"

        # ------------------------------------------------------------------
        # 3. Copy data files to docs/public/data/
        # ------------------------------------------------------------------
        if data_file_names:
            script_dir = script_path.parent
            for data_file in data_file_names:
                data_src = script_dir / data_file
                if data_src.exists():
                    if data_src.is_dir():
                        # Zip directories for website distribution
                        zip_dest = PUBLIC_DATA / f"{data_file}.zip"
                        shutil.make_archive(
                            str(zip_dest.with_suffix("")), "zip",
                            root_dir=str(data_src.parent),
                            base_dir=data_file,
                        )
                    else:
                        dest = PUBLIC_DATA / data_file
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.copy2(data_src, dest)
                        dest.chmod(dest.stat().st_mode | 0o200)

        # ------------------------------------------------------------------
        # 4. Gallery item
        # ------------------------------------------------------------------
        gallery_items.append({
            "title": title,
            "category": category,
            "image": image_site_path,
            "link": f"/examples/{category}/{title}",
            "uses_symbols": uses_symbols,
        })

        # ------------------------------------------------------------------
        # 5. Sidebar item
        # ------------------------------------------------------------------
        short_desc = extract_short_description(explanation)
        sidebar_by_category.setdefault(category, []).append({
            "text": title,
            "link": f"/examples/{category}/{title}",
            "description": short_desc,
            "image": image_site_path,
        })

        # ------------------------------------------------------------------
        # 6. VitePress markdown page
        # ------------------------------------------------------------------
        page_dir = PAGES_DIR / category
        page_dir.mkdir(parents=True, exist_ok=True)

        md_lines = [f"# {title}", ""]

        if image_site_path:
            md_lines.append(
                f'<img class="example-image" src="{image_site_path}" alt="{title}" />'
            )
            md_lines.append("")

        if explanation:
            md_lines.append(explanation.replace("### ", "## "))
            md_lines.append("")

        if data_files_rel:
            md_lines.append("## Data")
            md_lines.append("")
            for url in data_files_rel:
                fname = url.rsplit("/", 1)[-1]
                md_lines.append(f'- <a href="{url}" download>{fname}</a>')
            md_lines.append("")

        if code:
            md_lines.extend(["## Python Code", "", "```python", code.rstrip(), "```", ""])

        (page_dir / f"{title}.md").write_text("\n".join(md_lines))

    # ======================================================================
    # Write aggregated outputs
    # ======================================================================

    # JSONL
    with open(JSONL_OUTPUT, "w") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"  data/examples.jsonl          ({len(records)} records)")

    # Gallery .mjs (sorted alphabetically by title)
    gallery_items.sort(key=lambda x: x["title"].lower())
    gallery_path = GENERATED_DIR / "gallery.mjs"
    gallery_json = json.dumps(gallery_items, indent=2, ensure_ascii=False)
    gallery_path.write_text(f"export default {gallery_json}\n")
    print(f"  .vitepress/generated/gallery.mjs  ({len(gallery_items)} items)")

    # Sidebar .mjs (categories and items sorted alphabetically)
    sidebar = [
        {
            "text": CATEGORY_LABELS.get(cat, cat),
            "collapsed": False,
            "items": sorted(items, key=lambda x: x["text"].lower()),
        }
        for cat in sorted(sidebar_by_category)
        for items in [sidebar_by_category[cat]]
    ]
    # Strip description from sidebar items (only needed for the index page)
    sidebar_clean = [
        {
            "text": group["text"],
            "collapsed": group["collapsed"],
            "items": [{"text": i["text"], "link": i["link"]} for i in group["items"]],
        }
        for group in sidebar
    ]
    sidebar_json = json.dumps(sidebar_clean, indent=2, ensure_ascii=False)
    sidebar_path = GENERATED_DIR / "sidebar.mjs"
    sidebar_path.write_text(f"export default {sidebar_json}\n")
    total_sidebar = sum(len(g["items"]) for g in sidebar)
    print(f"  .vitepress/generated/sidebar.mjs  ({total_sidebar} items)")

    # Examples index page (docs/examples/index.md) — card list with image + name + description
    index_lines = [
        "# Examples",
        "",
        "<style>",
        ".example-row { display:flex; gap:1rem; align-items:flex-start;"
        " padding:0.75rem 0; border-bottom:1px solid var(--vp-c-divider); }",
        ".example-row img { width:80px; height:80px; object-fit:cover;"
        " border-radius:6px; flex-shrink:0; background:#1a1a2e; }",
        ".example-row .example-info { min-width:0; }",
        ".example-row .example-name { font-weight:600; font-size:1rem;"
        " margin:0 0 0.25rem; }",
        ".example-row .example-name a { color:var(--vp-c-brand-1);"
        " text-decoration:none; }",
        ".example-row .example-name a:hover { text-decoration:underline; }",
        ".example-row .example-desc { font-size:0.85rem;"
        " color:var(--vp-c-text-2); margin:0; }",
        ".example-noimg { width:80px; height:80px; border-radius:6px;"
        " background:var(--vp-c-bg-soft); flex-shrink:0; }",
        "</style>",
        "",
    ]
    for group in sidebar:
        index_lines.append(f"## {group['text']}")
        index_lines.append("")
        for item in group["items"]:
            desc = item.get("description", "")
            img = item.get("image", "")
            link = f"{SITE_BASE}{item['link']}"
            if img:
                img_html = f'<img src="{SITE_BASE}{img}" alt="{item["text"]}" />'
            else:
                img_html = '<div class="example-noimg"></div>'
            index_lines.append(f'<div class="example-row">')
            index_lines.append(f'  {img_html}')
            index_lines.append(f'  <div class="example-info">')
            index_lines.append(f'    <p class="example-name"><a href="{link}">{item["text"]}</a></p>')
            if desc:
                index_lines.append(f'    <p class="example-desc">{desc}</p>')
            index_lines.append(f'  </div>')
            index_lines.append(f'</div>')
            index_lines.append("")
        index_lines.append("")
    (PAGES_DIR / "index.md").write_text("\n".join(index_lines))

    # Images
    print(f"  docs/public/images/          ({len(list(PUBLIC_IMAGES.glob('*.png')))} screenshots)")

    # Pages
    page_count = len(list(PAGES_DIR.rglob("*.md")))
    print(f"  docs/examples/               ({page_count} pages)")

    # Update example count in docs/index.md
    index_path = DOCS / "index.md"
    if index_path.exists():
        index_text = index_path.read_text()
        updated = re.sub(
            r"title: \d+ Examples",
            f"title: {len(records)} Examples",
            index_text,
        )
        if updated != index_text:
            index_path.write_text(updated)
            print(f"  docs/index.md                (updated count to {len(records)})")

    print(f"\nDone. {len(records)} examples processed.")


if __name__ == "__main__":
    main()
