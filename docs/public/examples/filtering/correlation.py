#!/usr/bin/env python

# Compute spatial correlation between two canvas images.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingGeneral import vtkImageCorrelation
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Large canvas with triangle
canvas_1 = vtkImageCanvasSource2D()
canvas_1.SetScalarTypeToFloat()
canvas_1.SetExtent(0, 255, 0, 255, 0, 0)
canvas_1.SetDrawColor(0)
canvas_1.FillBox(0, 255, 0, 255)
canvas_1.SetDrawColor(2.0)
canvas_1.FillTriangle(10, 100, 190, 150, 40, 250)
canvas_1.Update()

# Small canvas with triangle
canvas_2 = vtkImageCanvasSource2D()
canvas_2.SetScalarTypeToFloat()
canvas_2.SetExtent(0, 31, 0, 31, 0, 0)
canvas_2.SetDrawColor(0.0)
canvas_2.FillBox(0, 31, 0, 31)
canvas_2.SetDrawColor(2.0)
canvas_2.FillTriangle(10, 1, 25, 10, 1, 5)
canvas_2.Update()

# Correlation
convolve = vtkImageCorrelation()
convolve.SetDimensionality(2)
convolve.SetInput1Data(canvas_1.GetOutput())
convolve.SetInput2Data(canvas_2.GetOutput())
convolve.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(convolve.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("correlation")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
