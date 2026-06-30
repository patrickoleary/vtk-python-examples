#!/usr/bin/env python
"""Generate pre-rendered thumbnails for the VTK Python Examples website."""

from pathlib import Path
from PIL import Image

# Thumbnail sizes
THUMB_SMALL = (44, 44)  # For trapezoid and examples page
THUMB_GALLERY = (180, 180)  # For gallery page

PUBLIC_EXAMPLES_DIR = Path("docs/public/examples")


def generate_thumbnails() -> None:
    """Generate thumbnails for all PNG images in docs/public/examples."""
    print("Scanning for PNG images...")
    
    png_files = list(PUBLIC_EXAMPLES_DIR.rglob("*.png"))
    total = len(png_files)
    small_count = 0
    gallery_count = 0

    for i, source_path in enumerate(png_files, 1):
        # Extract tag and base from path
        rel_path = source_path.relative_to(PUBLIC_EXAMPLES_DIR)
        parts = rel_path.parts
        if len(parts) < 2:
            print(f"  [{i}/{total}] Skipping {rel_path} (invalid path)")
            continue
        
        tag = parts[0]
        filename = parts[-1]
        base = filename.replace(".png", "")

        try:
            with Image.open(source_path) as img:
                # Generate 44x44 thumbnail
                thumb_small_path = PUBLIC_EXAMPLES_DIR / tag / f"{base}.thumb44.jpg"
                thumb_small = img.resize(THUMB_SMALL, Image.Resampling.LANCZOS)
                thumb_small.save(thumb_small_path, "JPEG", quality=85, optimize=True)
                small_count += 1

                # Generate 180x180 thumbnail
                thumb_gallery_path = PUBLIC_EXAMPLES_DIR / tag / f"{base}.thumb180.jpg"
                thumb_gallery = img.resize(THUMB_GALLERY, Image.Resampling.LANCZOS)
                thumb_gallery.save(thumb_gallery_path, "JPEG", quality=85, optimize=True)
                gallery_count += 1

                print(f"  [{i}/{total}] Generated thumbnails for {tag}/{base}")
        except Exception as e:
            print(f"  [{i}/{total}] Error processing {rel_path}: {e}")

    print(f"\nGenerated {small_count} small thumbnails (44x44)")
    print(f"Generated {gallery_count} gallery thumbnails (180x180)")


if __name__ == "__main__":
    generate_thumbnails()
