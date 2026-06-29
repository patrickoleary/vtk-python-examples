#!/usr/bin/env python

# Import a 3DS file via vtkFileResourceStream and render.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImport import vtk3DSImporter
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Open stream
file_stream = vtkFileResourceStream()
file_stream.Open(os.path.join(data_dir, "iflamigm.3ds"))

# Import 3DS via stream
ds_importer = vtk3DSImporter()
ds_importer.SetStream(file_stream)

# Renderer
renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("3ds import-stream")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

ds_importer.SetRenderWindow(render_window)
ds_importer.Update()

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(10, 10, -10)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
