#!/usr/bin/env python

# Demonstrate vtkImageCanvasSource2D drawing a JPEG image onto a canvas.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Canvas
image_canvas = vtkImageCanvasSource2D()
image_canvas.SetScalarTypeToUnsignedChar()
image_canvas.SetNumberOfScalarComponents(3)
image_canvas.SetExtent(0, 300, 0, 300, 0, 0)
image_canvas.SetDrawColor(0)
image_canvas.FillBox(0, 511, 0, 511)

# Read JPEG image
jpeg_reader = vtkJPEGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

jpeg_reader.SetFileName(os.path.join(data_dir, "beach.jpg"))
jpeg_reader.Update()

# Draw JPEG onto canvas at various positions
image_canvas.DrawImage(100, 100, jpeg_reader.GetOutput(), 0, 0, 300, 300)
image_canvas.DrawImage(0, 100, jpeg_reader.GetOutput())
image_canvas.DrawImage(100, 0, jpeg_reader.GetOutput(), 0, 0, 300, 300)
image_canvas.DrawImage(0, 0, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(10, 10, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(20, 20, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(30, 30, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(40, 40, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(50, 50, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(60, 60, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.DrawImage(70, 70, jpeg_reader.GetOutput(), 50, 50, 100, 100)
image_canvas.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_canvas.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("image canvas")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
