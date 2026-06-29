#!/usr/bin/env python

# Read a BMP file via vtkFileResourceStream with lookup table mapping and display.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOCore import vtkFileResourceStream
from vtkmodules.vtkIOImage import vtkBMPReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
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
file_stream.Open(os.path.join(data_dir, "masonry.bmp"))

# Read BMP from stream
bmp_reader = vtkBMPReader()
bmp_reader.SetStream(file_stream)
bmp_reader.Allow8BitBMPOn()
bmp_reader.Update()

# Map through lookup table
map_colors = vtkImageMapToColors()
map_colors.SetInputConnection(bmp_reader.GetOutputPort())
map_colors.SetLookupTable(bmp_reader.GetLookupTable())
map_colors.SetOutputFormatToRGB()

# Display with image actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(map_colors.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("bmp reader stream")
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
