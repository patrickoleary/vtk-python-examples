#!/usr/bin/env python

# Import a glTF GLB file (WaterBottle) via vtkFileResourceStream with PBR and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImport import vtkGLTFImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Open stream
file_stream = vtkFileResourceStream()
file_stream.Open(os.path.join(data_dir, "glTF", "WaterBottle", "WaterBottle.glb"))

# Import glTF via stream
gltf_importer = vtkGLTFImporter()
gltf_importer.SetStream(file_stream)
gltf_importer.StreamIsBinaryOn()
gltf_importer.ImportArmatureOn()
gltf_importer.SetCamera(-1)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.2, 0.3, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("gltf importer pbr stream")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

gltf_importer.SetRenderWindow(render_window)
gltf_importer.Update()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
