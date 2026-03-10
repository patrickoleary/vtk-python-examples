"""
Shared utilities for testing VTK Python examples.

Provides offscreen rendering and image capture for examples that use
the standard VTK pipeline pattern with a render_window variable.
"""

import os
import re
import sys
import types

# Force offscreen rendering before any VTK imports
os.environ["VTK_DEFAULT_RENDER_WINDOW_OFFSCREEN"] = "1"

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindowInteractor,
    vtkWindowToImageFilter,
)


class _NonBlockingInteractor(vtkRenderWindowInteractor):
    """A vtkRenderWindowInteractor subclass that skips Initialize and Start."""

    def Initialize(self):
        pass

    def Start(self):
        pass


def _make_patched_rendering_core():
    """Create a fake vtkmodules.vtkRenderingCore module with the non-blocking interactor."""
    import vtkmodules.vtkRenderingCore as real_module

    fake = types.ModuleType("vtkmodules.vtkRenderingCore")
    for attr in dir(real_module):
        setattr(fake, attr, getattr(real_module, attr))
    fake.vtkRenderWindowInteractor = _NonBlockingInteractor
    return fake


class _SysExitCalled(Exception):
    """Raised instead of actually exiting when sys.exit is patched."""

    pass


def run_example_offscreen(script_path):
    """Execute an example script offscreen with a non-blocking interactor.

    Returns the script's global namespace dict after execution.
    """
    fake_module = _make_patched_rendering_core()

    original = sys.modules.get("vtkmodules.vtkRenderingCore")
    sys.modules["vtkmodules.vtkRenderingCore"] = fake_module

    # Patch sys.exit so examples that call sys.exit() don't kill the test
    original_exit = sys.exit
    sys.exit = lambda *args: None

    # Patch QApplication.exec so PyQt examples don't block on the event loop
    _qapp_exec_patched = False
    _original_qapp_exec = None
    try:
        from PyQt6.QtWidgets import QApplication as _QApp

        _original_qapp_exec = _QApp.exec
        _QApp.exec = lambda self=None: 0
        _qapp_exec_patched = True
    except ImportError:
        pass

    try:
        source = script_path.read_text()
        # Strip .Initialize() and .Start() calls so that interactors
        # created internally by C++ view classes (e.g. vtkGraphLayoutView)
        # do not block.  The module-swap above handles examples that
        # construct vtkRenderWindowInteractor explicitly, but view classes
        # create their own C++ interactor instances that cannot be
        # monkey-patched at the class level.
        source = re.sub(r"^[^\n#]*\.Initialize\(\)\s*$", "pass", source, flags=re.MULTILINE)
        source = re.sub(r"^[^\n#]*\.Start\(\)\s*$", "pass", source, flags=re.MULTILINE)
        namespace = {"__file__": str(script_path), "__name__": "__main__"}
        exec(compile(source, str(script_path), "exec"), namespace)
    finally:
        sys.exit = original_exit
        if _qapp_exec_patched:
            _QApp.exec = _original_qapp_exec
        if original is not None:
            sys.modules["vtkmodules.vtkRenderingCore"] = original
        else:
            sys.modules.pop("vtkmodules.vtkRenderingCore", None)

    return namespace


def capture_image(render_window, output_path):
    """Render the window and save a PNG screenshot."""
    render_window.Render()

    window_to_image = vtkWindowToImageFilter()
    window_to_image.SetInput(render_window)
    window_to_image.Update()

    writer = vtkPNGWriter()
    writer.SetFileName(str(output_path))
    writer.SetInputConnection(window_to_image.GetOutputPort())
    writer.Write()
