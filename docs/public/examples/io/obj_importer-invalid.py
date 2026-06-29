#!/usr/bin/env python

# Import an invalid OBJ file to test error handling.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImport import vtkOBJImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(data_dir, "Input")

# Import invalid OBJ
obj_importer = vtkOBJImporter()
obj_importer.SetFileName(os.path.join(input_dir, "world_invalid.obj"))

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("obj importer-invalid")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

obj_importer.SetRenderWindow(render_window)
obj_importer.Update()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
