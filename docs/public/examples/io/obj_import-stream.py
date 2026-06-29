#!/usr/bin/env python

# Import OBJ via vtkFileResourceStream and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImport import vtkOBJImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
input_dir = os.path.join(data_dir, "Input")

# Open streams
obj_stream = vtkFileResourceStream()
obj_stream.Open(os.path.join(input_dir, "cube-scene.obj"))

mtl_stream = vtkFileResourceStream()
mtl_stream.Open(os.path.join(input_dir, "cube-scene.mtl"))

# Import OBJ via streams
obj_importer = vtkOBJImporter()
obj_importer.SetStream(obj_stream)
obj_importer.SetMTLStream(mtl_stream)
obj_importer.SetTexturePath(input_dir)

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("obj import-stream")
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
