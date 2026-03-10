#!/usr/bin/env python
"""Add missing pipeline arrow notation to GeometricObjects .md files."""

from pathlib import Path

src = Path("src/Python/GeometricObjects")
count = 0

for md in sorted(src.glob("*.md")):
    text = md.read_text()
    if "\u2192" in text:
        continue

    stem = md.stem
    if stem.startswith("SourceObject"):
        p = "**Source \u2192 Mapper \u2192 Actor \u2192 Renderer \u2192 Window \u2192 Interactor**"
    elif stem.startswith("LinearCell") or stem.startswith("IsoParametricCell"):
        p = "**Cell \u2192 UnstructuredGrid \u2192 DataSetMapper \u2192 Actor + Glyphs + Labels \u2192 Renderer \u2192 Window \u2192 Interactor**"
    else:
        continue

    lines = text.splitlines()
    out = []
    inserted = False
    found_desc = False
    found_para = False

    for line in lines:
        out.append(line)
        if line.strip() == "### Description":
            found_desc = True
        elif found_desc and not found_para and line.strip():
            found_para = True
        elif found_para and not inserted and line.strip() == "":
            out.append(p)
            out.append("")
            inserted = True

    if inserted:
        md.write_text("\n".join(out))
        count += 1
        print(f"  Added: {md.name}")

print(f"\nUpdated {count} files")
