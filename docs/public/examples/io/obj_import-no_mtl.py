#!/usr/bin/env python

# Import OBJ with no MTL file and render.

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
obj_importer.SetFileName(os.path.join(input_dir, "boxes_3_no_mtl.obj"))
obj_importer.SetFileNameMTL(os.path.join(input_dir, "boxes_2.obj.mtl"))
obj_importer.SetTexturePath(input_dir)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("obj import-no mtl")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

obj_importer.SetRenderWindow(render_window)
obj_importer.Update()

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
