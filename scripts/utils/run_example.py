"""Launch a VTK example interactively.

Usage:
    uv run vtkex data/examples/annotation/axis_actor2d.py
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def main():
    if len(sys.argv) < 2:
        print("Usage: vtkex <script.py> [args...]", file=sys.stderr)
        sys.exit(1)

    script = Path(sys.argv[1])
    if not script.is_absolute():
        script = (Path.cwd() / script).resolve()

    if not script.exists():
        # Try resolving relative to docs/public/examples/
        alt = PROJECT_ROOT / "docs" / "public" / "examples" / sys.argv[1]
        if alt.exists():
            script = alt.resolve()
        else:
            print(f"Script not found: {script}", file=sys.stderr)
            sys.exit(1)

    # Set VPE_DATA_DIR if not already set
    if "VPE_DATA_DIR" not in os.environ:
        data_dir = PROJECT_ROOT / "docs" / "public" / "examples" / "data"
        os.environ["VPE_DATA_DIR"] = str(data_dir)

    # Run the script
    sys.argv = sys.argv[1:]
    namespace = {"__file__": str(script), "__name__": "__main__"}
    exec(compile(script.read_text(), str(script), "exec"), namespace)


if __name__ == "__main__":
    main()
