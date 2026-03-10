#!/usr/bin/env python

# Normalize an RGB image so that each pixel's color vector has unit
# magnitude using vtkImageNormalize.  The left viewport shows the
# original image with varying brightness; the right shows the
# normalized result where every pixel has uniform brightness but
# the color direction (hue) is preserved.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageNormalize
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: create a 256x256 RGB canvas with regions of varying color
# and brightness so normalization has a visible effect
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetDrawColor(20, 10, 5)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(200, 50, 30)
canvas.FillBox(10, 120, 140, 245)
canvas.SetDrawColor(30, 180, 40)
canvas.FillBox(135, 245, 140, 245)
canvas.SetDrawColor(40, 50, 200)
canvas.FillBox(10, 120, 10, 125)
canvas.SetDrawColor(100, 25, 15)
canvas.FillBox(135, 245, 10, 125)
canvas.Update()

# Cast to float so vtkImageNormalize can produce fractional results
cast_to_float = vtkImageCast()
cast_to_float.SetInputConnection(canvas.GetOutputPort())
cast_to_float.SetOutputScalarTypeToFloat()

# Normalize: scale each pixel's RGB vector to unit magnitude
normalize = vtkImageNormalize()
normalize.SetInputConnection(cast_to_float.GetOutputPort())

# Scale normalized [0..1] back to [0..255] for display
scale = vtkImageMathematics()
scale.SetOperationToMultiplyByK()
scale.SetConstantK(255.0)
scale.SetInputConnection(normalize.GetOutputPort())

# Cast: convert scaled result to unsigned char for display
cast_normalized = vtkImageCast()
cast_normalized.SetInputConnection(scale.GetOutputPort())
cast_normalized.SetOutputScalarTypeToUnsignedChar()
cast_normalized.ClampOverflowOn()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(canvas.GetOutputPort())

# Actor 2: normalized image (right viewport)
actor_normalized = vtkImageActor()
actor_normalized.GetMapper().SetInputConnection(cast_normalized.GetOutputPort())

# Renderer 1: left viewport — original with varying brightness
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — normalized to uniform brightness
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_normalized)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageNormalize")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
