#!/usr/bin/env python

# Read a PNG file via vtkFileResourceStream and display with vtkImageActor.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Open file via stream
file_stream = vtkFileResourceStream()
file_stream.Open(os.path.join(data_dir, "vtk.png"))

# Read PNG from stream
png_reader = vtkPNGReader()
png_reader.SetStream(file_stream)
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
render_window.SetWindowName("png reader read from stream")
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
