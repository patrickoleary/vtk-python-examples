#!/usr/bin/env python

# Import a glTF file with KHR_lights_punctual extension and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Import glTF
gltf_importer = vtkGLTFImporter()
gltf_importer.SetFileName(os.path.join(data_dir, "glTF", "Lights", "lights.gltf"))
gltf_importer.ImportArmatureOn()
gltf_importer.SetCamera(0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf importer khr lights punctual")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

interactor.Initialize()
interactor.Start()
