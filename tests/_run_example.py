"""Subprocess helper: run a VTK example offscreen and capture a screenshot.

Usage (called by test harness, not directly):
    python tests/_run_example.py <script_path> <output_image> <render_window_var>
"""

import os
import re
import sys
import types
from pathlib import Path

os.environ["VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN"] = "1"

import vtkmodules.vtkInteractionStyle  # noqa: F401, E402
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401, E402
from vtkmodules.vtkIOImage import vtkPNGWriter  # noqa: E402
from vtkmodules.vtkRenderingCore import (  # noqa: E402
    vtkRenderWindowInteractor,
    vtkWindowToImageFilter,
)


class _NonBlockingInteractor(vtkRenderWindowInteractor):
    """Interactor that skips Initialize and Start to prevent blocking."""

    def Initialize(self):
        pass

    def Start(self):
        pass


# Patch the rendering core module
import vtkmodules.vtkRenderingCore as _real_module  # noqa: E402

_fake = types.ModuleType("vtkmodules.vtkRenderingCore")
for _attr in dir(_real_module):
    setattr(_fake, _attr, getattr(_real_module, _attr))
_fake.vtkRenderWindowInteractor = _NonBlockingInteractor
sys.modules["vtkmodules.vtkRenderingCore"] = _fake

# Parse args
script_path = sys.argv[1]
output_image = sys.argv[2]
render_window_var = sys.argv[3]

# Read and patch the source
source = Path(script_path).read_text()
source = re.sub(r"^([^\n#]*[Ii]nteractor\w*)\.Initialize\(\)\s*$", "pass", source, flags=re.MULTILINE)
source = re.sub(r"^[^\n#]*\.Start\(\)\s*$", "pass", source, flags=re.MULTILINE)

# Qt-specific patches: prevent app.exec() from blocking
source = re.sub(r"sys\.exit\(app\.exec\(\)\)", "pass", source)
source = re.sub(r"app\.exec\(\)", "pass", source)

# Execute
ns = {"__file__": script_path, "__name__": "__main__"}
exec(compile(source, script_path, "exec"), ns)

# Capture screenshot
rw = ns.get(render_window_var)
if rw is None:
    print(f"ERROR: '{render_window_var}' not found in namespace", file=sys.stderr)
    sys.exit(1)

rw.Render()
w2i = vtkWindowToImageFilter()
w2i.SetInput(rw)
w2i.Update()

writer = vtkPNGWriter()
writer.SetFileName(output_image)
writer.SetInputConnection(w2i.GetOutputPort())
writer.Write()
