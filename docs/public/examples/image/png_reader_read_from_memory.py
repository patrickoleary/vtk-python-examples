#!/usr/bin/env python

# Read a PNG file from memory buffer and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Load PNG file into memory
png_file = os.path.join(data_dir, "vtk.png")
with open(png_file, "rb") as f:
    buffer = f.read()

# Read PNG from memory
png_reader = vtkPNGReader()
png_reader.SetMemoryBuffer(buffer)
png_reader.SetMemoryBufferLength(len(buffer))
png_reader.Update()

# Display with image actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(png_reader.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("png reader read from memory")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
