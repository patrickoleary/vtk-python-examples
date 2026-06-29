#!/usr/bin/env python

# Round-trip RGB to YIQ and back to RGB conversion on a canvas image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingColor import (
    vtkImageRGBToYIQ,
    vtkImageYIQToRGB,
)
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Draw colored boxes on a canvas
image_canvas = vtkImageCanvasSource2D()
image_canvas.SetNumberOfScalarComponents(3)
image_canvas.SetScalarTypeToUnsignedChar()
image_canvas.SetExtent(0, 320, 0, 320, 0, 0)
image_canvas.SetDrawColor(0, 0, 0)
image_canvas.FillBox(0, 511, 0, 511)
# Hue scale
image_canvas.SetDrawColor(255, 0, 0)
image_canvas.FillBox(0, 50, 0, 100)
image_canvas.SetDrawColor(128, 128, 0)
image_canvas.FillBox(50, 100, 0, 100)
image_canvas.SetDrawColor(0, 255, 0)
image_canvas.FillBox(100, 150, 0, 100)
image_canvas.SetDrawColor(0, 128, 128)
image_canvas.FillBox(150, 200, 0, 100)
image_canvas.SetDrawColor(0, 0, 255)
image_canvas.FillBox(200, 250, 0, 100)
image_canvas.SetDrawColor(128, 0, 128)
image_canvas.FillBox(250, 300, 0, 100)
# Intensity scale
image_canvas.SetDrawColor(5, 5, 5)
image_canvas.FillBox(0, 50, 110, 210)
image_canvas.SetDrawColor(55, 55, 55)
image_canvas.FillBox(50, 100, 110, 210)
image_canvas.SetDrawColor(105, 105, 105)
image_canvas.FillBox(100, 150, 110, 210)
image_canvas.SetDrawColor(155, 155, 155)
image_canvas.FillBox(150, 200, 110, 210)
image_canvas.SetDrawColor(205, 205, 205)
image_canvas.FillBox(200, 250, 110, 210)
image_canvas.SetDrawColor(255, 255, 255)
image_canvas.FillBox(250, 300, 110, 210)
# Saturation scale
image_canvas.SetDrawColor(245, 0, 0)
image_canvas.FillBox(0, 50, 220, 320)
image_canvas.SetDrawColor(213, 16, 16)
image_canvas.FillBox(50, 100, 220, 320)
image_canvas.SetDrawColor(181, 32, 32)
image_canvas.FillBox(100, 150, 220, 320)
image_canvas.SetDrawColor(149, 48, 48)
image_canvas.FillBox(150, 200, 220, 320)
image_canvas.SetDrawColor(117, 64, 64)
image_canvas.FillBox(200, 250, 220, 320)
image_canvas.SetDrawColor(85, 80, 80)
image_canvas.FillBox(250, 300, 220, 320)

# Cast to float for YIQ conversion (YIQ is signed)
cast_1 = vtkImageCast()
cast_1.SetInputConnection(image_canvas.GetOutputPort())
cast_1.SetOutputScalarTypeToFloat()

# RGB -> YIQ -> RGB round trip
convert = vtkImageRGBToYIQ()
convert.SetInputConnection(cast_1.GetOutputPort())

convert_back = vtkImageYIQToRGB()
convert_back.SetInputConnection(convert.GetOutputPort())

# Cast back to unsigned char for display
cast_2 = vtkImageCast()
cast_2.SetInputConnection(convert_back.GetOutputPort())
cast_2.SetOutputScalarTypeToUnsignedChar()
cast_2.ClampOverflowOn()
cast_2.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(cast_2.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(320, 320)
render_window.SetWindowName("yiq to rgb")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
