#!/usr/bin/env python
"""Remove vtkNamedColors from all .py files.

Replaces `colors.GetColor3d("Name")` with inline RGB tuples and removes
the import and instantiation lines.

Color values are sourced from the VTK named colors table.
"""

import re
import sys
from pathlib import Path

# VTK named colors -> normalized RGB (0-1 floats, 3 decimal places)
# Source: https://www.vtk.org/doc/nightly/html/classvtkNamedColors.html
NAMED_COLORS = {
    "AliceBlue": (0.941, 0.973, 1.0),
    "AntiqueWhite": (0.980, 0.922, 0.843),
    "Aqua": (0.0, 1.0, 1.0),
    "Aquamarine": (0.498, 1.0, 0.831),
    "Azure": (0.941, 1.0, 1.0),
    "Banana": (0.890, 0.812, 0.341),
    "Beige": (0.961, 0.961, 0.863),
    "Bisque": (1.0, 0.894, 0.769),
    "Black": (0.0, 0.0, 0.0),
    "BlanchedAlmond": (1.0, 0.922, 0.804),
    "Blue": (0.0, 0.0, 1.0),
    "BlueViolet": (0.541, 0.169, 0.886),
    "Brick": (0.612, 0.204, 0.200),
    "Brown": (0.647, 0.165, 0.165),
    "BurlyWood": (0.871, 0.722, 0.529),
    "CadetBlue": (0.373, 0.620, 0.627),
    "Carrot": (0.900, 0.490, 0.130),
    "Chartreuse": (0.498, 1.0, 0.0),
    "Chocolate": (0.824, 0.412, 0.118),
    "Cobalt": (0.239, 0.349, 0.671),
    "ColdGrey": (0.502, 0.541, 0.529),
    "Coral": (1.0, 0.498, 0.314),
    "CornflowerBlue": (0.392, 0.584, 0.929),
    "Cornsilk": (1.0, 0.973, 0.863),
    "Crimson": (0.863, 0.078, 0.235),
    "Cyan": (0.0, 1.0, 1.0),
    "DarkBlue": (0.0, 0.0, 0.545),
    "DarkCyan": (0.0, 0.545, 0.545),
    "DarkGoldenrod": (0.722, 0.525, 0.043),
    "DarkGray": (0.663, 0.663, 0.663),
    "DarkGreen": (0.0, 0.392, 0.0),
    "DarkKhaki": (0.741, 0.718, 0.420),
    "DarkMagenta": (0.545, 0.0, 0.545),
    "DarkOliveGreen": (0.333, 0.420, 0.184),
    "DarkOrange": (1.0, 0.549, 0.0),
    "DarkOrchid": (0.600, 0.196, 0.800),
    "DarkRed": (0.545, 0.0, 0.0),
    "DarkSalmon": (0.914, 0.588, 0.478),
    "DarkSeaGreen": (0.561, 0.737, 0.561),
    "DarkSlateBlue": (0.282, 0.239, 0.545),
    "DarkSlateGray": (0.184, 0.310, 0.310),
    "DarkSlateGrey": (0.184, 0.310, 0.310),
    "DarkTurquoise": (0.0, 0.808, 0.820),
    "DarkViolet": (0.580, 0.0, 0.827),
    "DeepPink": (1.0, 0.078, 0.576),
    "DeepSkyBlue": (0.0, 0.749, 1.0),
    "DimGray": (0.412, 0.412, 0.412),
    "DimGrey": (0.412, 0.412, 0.412),
    "DodgerBlue": (0.118, 0.565, 1.0),
    "Eggshell": (0.988, 0.902, 0.788),
    "FireBrick": (0.698, 0.133, 0.133),
    "Flesh": (1.0, 0.490, 0.251),
    "FloralWhite": (1.0, 0.980, 0.941),
    "ForestGreen": (0.133, 0.545, 0.133),
    "Fuchsia": (1.0, 0.0, 1.0),
    "Gainsboro": (0.863, 0.863, 0.863),
    "GhostWhite": (0.973, 0.973, 1.0),
    "Gold": (1.0, 0.843, 0.0),
    "Goldenrod": (0.855, 0.647, 0.125),
    "Gray": (0.502, 0.502, 0.502),
    "Green": (0.0, 0.502, 0.0),
    "GreenYellow": (0.678, 1.0, 0.184),
    "Grey": (0.502, 0.502, 0.502),
    "Honeydew": (0.941, 1.0, 0.941),
    "HotPink": (1.0, 0.412, 0.706),
    "IndianRed": (0.804, 0.361, 0.361),
    "Indigo": (0.294, 0.0, 0.510),
    "Ivory": (1.0, 1.0, 0.941),
    "Khaki": (0.941, 0.902, 0.549),
    "Lavender": (0.902, 0.902, 0.980),
    "LavenderBlush": (1.0, 0.941, 0.961),
    "LawnGreen": (0.486, 0.988, 0.0),
    "LemonChiffon": (1.0, 0.980, 0.804),
    "LightBlue": (0.678, 0.847, 0.902),
    "LightCoral": (0.941, 0.502, 0.502),
    "LightCyan": (0.878, 1.0, 1.0),
    "LightGoldenrodYellow": (0.980, 0.980, 0.824),
    "LightGray": (0.827, 0.827, 0.827),
    "LightGreen": (0.565, 0.933, 0.565),
    "LightGrey": (0.827, 0.827, 0.827),
    "LightPink": (1.0, 0.714, 0.757),
    "LightSalmon": (1.0, 0.627, 0.478),
    "LightSeaGreen": (0.125, 0.698, 0.667),
    "LightSkyBlue": (0.529, 0.808, 0.980),
    "LightSlateGray": (0.467, 0.533, 0.600),
    "LightSlateGrey": (0.467, 0.533, 0.600),
    "LightSteelBlue": (0.690, 0.769, 0.871),
    "LightYellow": (1.0, 1.0, 0.878),
    "Lime": (0.0, 1.0, 0.0),
    "LimeGreen": (0.196, 0.804, 0.196),
    "Linen": (0.980, 0.941, 0.902),
    "Magenta": (1.0, 0.0, 1.0),
    "Maroon": (0.502, 0.0, 0.0),
    "MediumAquamarine": (0.400, 0.804, 0.667),
    "MediumBlue": (0.0, 0.0, 0.804),
    "MediumOrchid": (0.729, 0.333, 0.827),
    "MediumPurple": (0.576, 0.439, 0.859),
    "MediumSeaGreen": (0.235, 0.702, 0.443),
    "MediumSlateBlue": (0.482, 0.408, 0.933),
    "MediumSpringGreen": (0.0, 0.980, 0.604),
    "MediumTurquoise": (0.282, 0.820, 0.800),
    "MediumVioletRed": (0.780, 0.082, 0.522),
    "Melon": (0.890, 0.659, 0.412),
    "MidnightBlue": (0.098, 0.098, 0.439),
    "Mint": (0.741, 0.988, 0.788),
    "MintCream": (0.961, 1.0, 0.980),
    "MistyRose": (1.0, 0.894, 0.882),
    "Moccasin": (1.0, 0.894, 0.710),
    "NavajoWhite": (1.0, 0.871, 0.678),
    "Navy": (0.0, 0.0, 0.502),
    "OldLace": (0.992, 0.961, 0.902),
    "Olive": (0.502, 0.502, 0.0),
    "OliveDrab": (0.420, 0.557, 0.137),
    "Orange": (1.0, 0.647, 0.0),
    "OrangeRed": (1.0, 0.271, 0.0),
    "Orchid": (0.855, 0.439, 0.839),
    "PaleGoldenrod": (0.933, 0.910, 0.667),
    "PaleGreen": (0.596, 0.984, 0.596),
    "PaleTurquoise": (0.686, 0.933, 0.933),
    "PaleVioletRed": (0.859, 0.439, 0.576),
    "PapayaWhip": (1.0, 0.937, 0.835),
    "PeachPuff": (1.0, 0.855, 0.725),
    "Peru": (0.804, 0.522, 0.247),
    "Pink": (1.0, 0.753, 0.796),
    "Plum": (0.867, 0.627, 0.867),
    "PowderBlue": (0.690, 0.878, 0.902),
    "Purple": (0.502, 0.0, 0.502),
    "Raspberry": (0.502, 0.0, 0.251),
    "RawSienna": (0.780, 0.380, 0.082),
    "Red": (1.0, 0.0, 0.0),
    "RosyBrown": (0.737, 0.561, 0.561),
    "RoyalBlue": (0.255, 0.412, 0.882),
    "SaddleBrown": (0.545, 0.271, 0.075),
    "Salmon": (0.980, 0.502, 0.447),
    "SandyBrown": (0.957, 0.643, 0.376),
    "SeaGreen": (0.180, 0.545, 0.341),
    "Seashell": (1.0, 0.961, 0.933),
    "Sienna": (0.627, 0.322, 0.176),
    "Silver": (0.753, 0.753, 0.753),
    "SkyBlue": (0.529, 0.808, 0.922),
    "SlateBlue": (0.416, 0.353, 0.804),
    "SlateGray": (0.439, 0.502, 0.565),
    "SlateGrey": (0.439, 0.502, 0.565),
    "Snow": (1.0, 0.980, 0.980),
    "SpringGreen": (0.0, 1.0, 0.498),
    "SteelBlue": (0.275, 0.510, 0.706),
    "Tan": (0.824, 0.706, 0.549),
    "Teal": (0.0, 0.502, 0.502),
    "Thistle": (0.847, 0.749, 0.847),
    "Tomato": (1.0, 0.388, 0.278),
    "Turquoise": (0.251, 0.878, 0.816),
    "Violet": (0.933, 0.510, 0.933),
    "VioletRed": (0.816, 0.125, 0.565),
    "WarmGrey": (0.502, 0.502, 0.412),
    "Wheat": (0.961, 0.871, 0.702),
    "White": (1.0, 1.0, 1.0),
    "WhiteSmoke": (0.961, 0.961, 0.961),
    "Yellow": (1.0, 1.0, 0.0),
    "YellowGreen": (0.604, 0.804, 0.196),
}


def remove_named_colors(py_path):
    """Remove vtkNamedColors from a single .py file.

    Returns True if the file was modified.
    """
    text = py_path.read_text()

    # Skip if no vtkNamedColors usage
    if "vtkNamedColors" not in text:
        return False

    # Step 1: Find all color names used via GetColor3d/GetColor4d
    color_names = set()
    for m in re.finditer(r'\.GetColor[34]d\(["\'](\w+)["\']\)', text):
        color_names.add(m.group(1))

    # Step 2: Build variable name -> RGB tuple mapping
    # Use snake_case variable names
    color_vars = {}
    for name in sorted(color_names):
        if name not in NAMED_COLORS:
            print(f"  WARNING: Unknown color '{name}' in {py_path}", file=sys.stderr)
            # Use a placeholder
            color_vars[name] = (0.5, 0.5, 0.5)
        else:
            color_vars[name] = NAMED_COLORS[name]

    # Build snake_case var names
    def to_snake(name):
        s = re.sub(r'([a-z])([A-Z])', r'\1_\2', name)
        return s.lower() + "_rgb"

    var_map = {name: to_snake(name) for name in color_names}

    # Step 3: Replace `colors.GetColor3d("Name")` with the variable name
    def replace_color(m):
        prefix = m.group(1)  # GetColor3d or GetColor4d
        name = m.group(2)
        return var_map[name]

    new_text = re.sub(
        r'colors\.GetColor([34]d)\(["\'](\w+)["\']\)',
        replace_color,
        text,
    )

    # Step 4: Remove the `colors = vtkNamedColors()` line
    new_text = re.sub(r'^colors\s*=\s*vtkNamedColors\(\)\s*\n', '', new_text, flags=re.MULTILINE)

    # Step 5: Remove the import line for vtkNamedColors
    # Handle "from vtkmodules.vtkCommonColor import vtkNamedColors\n"
    new_text = re.sub(
        r'^from\s+vtkmodules\.vtkCommonColor\s+import\s+vtkNamedColors\s*\n',
        '',
        new_text,
        flags=re.MULTILINE,
    )
    # Handle multi-import: "from vtkmodules.vtkCommonColor import (\n    vtkNamedColors,\n)"
    # This is more complex; for now handle single-import case which covers all 99 files

    # Step 6: Replace the "# Colors (normalized RGB)" comment with actual color definitions
    color_defs = []
    for name in sorted(color_names):
        r, g, b = color_vars[name]
        color_defs.append(f"{var_map[name]} = ({r}, {g}, {b})")

    color_block = "\n".join(color_defs)

    # Replace the comment + blank line after removed colors = ... line
    if "# Colors (normalized RGB)" in new_text:
        new_text = re.sub(
            r'# Colors \(normalized RGB\)\s*\n',
            f"# Colors (normalized RGB)\n{color_block}\n",
            new_text,
        )
    else:
        # If no standard comment, insert before first use
        # Find first line that uses a color var
        lines = new_text.splitlines()
        insert_idx = None
        for i, line in enumerate(lines):
            if any(var_map[n] in line for n in color_names):
                insert_idx = i
                break
        if insert_idx is not None:
            lines.insert(insert_idx, "# Colors (normalized RGB)")
            for j, cd in enumerate(color_defs):
                lines.insert(insert_idx + 1 + j, cd)
            lines.insert(insert_idx + 1 + len(color_defs), "")
            new_text = "\n".join(lines) + "\n"

    # Step 7: Clean up any double blank lines left from removals
    new_text = re.sub(r'\n{3,}', '\n\n', new_text)

    if new_text != text:
        py_path.write_text(new_text)
        return True
    return False


def main():
    src = Path("src/Python")
    if not src.exists():
        print("Run from the project root", file=sys.stderr)
        sys.exit(1)

    dry_run = "--dry" in sys.argv

    count = 0
    for py in sorted(src.rglob("*.py")):
        if "vtkNamedColors" not in py.read_text():
            continue
        if dry_run:
            print(f"  Would fix: {py}")
            count += 1
        else:
            if remove_named_colors(py):
                print(f"  Fixed: {py}")
                count += 1

    print(f"\n{'Would fix' if dry_run else 'Fixed'} {count} files")


if __name__ == "__main__":
    main()
