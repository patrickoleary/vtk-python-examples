#!/usr/bin/env python

# Smooth an impulse function with a 5x5 convolution kernel.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingGeneral import vtkImageConvolve
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Canvas with a bright box on dark background
canvas = vtkImageCanvasSource2D()
canvas.SetScalarTypeToFloat()
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(1.0)
canvas.FillBox(75, 175, 75, 175)

# Convolve with 5x5 kernel
convolve = vtkImageConvolve()
convolve.SetInputConnection(canvas.GetOutputPort())
convolve.SetKernel5x5([1, 1, 1, 1, 1, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 5, 4, 3, 2, 1, 1, 1, 1, 1, 1])
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
render_window.SetWindowName("convolve")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
