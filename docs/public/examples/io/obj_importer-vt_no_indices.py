#!/usr/bin/env python

# Import OBJ with vertex texture coordinates but no indices and render.

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

# Import OBJ
obj_importer = vtkOBJImporter()
obj_importer.SetFileName(os.path.join(input_dir, "TestOBJImporter-VtNoIndices.obj"))
obj_importer.SetFileNameMTL(os.path.join(input_dir, "TestOBJImporter-VtNoIndices.mtl"))
obj_importer.SetTexturePath(input_dir)

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("obj importer-vt no indices")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

obj_importer.SetRenderWindow(render_window)
obj_importer.Update()

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(10, 10, -10)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
