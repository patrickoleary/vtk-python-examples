#!/usr/bin/env python

# Import a VRML file and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImport import vtkVRMLImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vrml importer")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Import VRML
vrml_importer = vtkVRMLImporter()
vrml_importer.SetRenderWindow(render_window)
vrml_importer.SetFileName(os.path.join(data_dir, "bot2.wrl"))
vrml_importer.Update()

# Get the renderer created by the importer
ren_collection = render_window.GetRenderers()
ren_collection.InitTraversal()
vrml_renderer = ren_collection.GetNextItem()

# Scene
vrml_importer.GetRenderer().SetBackground(0.1, 0.2, 0.4)
vrml_renderer.GetActiveCamera().SetPosition(-3.25303, 3.46205, 3.15906)
vrml_renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
vrml_renderer.GetActiveCamera().SetViewUp(0.564063, 0.825024, -0.0341876)
vrml_renderer.ResetCamera()
vrml_renderer.GetActiveCamera().Dolly(1.75)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
