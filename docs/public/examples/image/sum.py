#!/usr/bin/env python

# Compute a weighted sum of two procedural images using
# vtkImageWeightedSum and display the inputs alongside the result.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingMath import vtkImageWeightedSum
from vtkmodules.vtkImagingSources import (
    vtkImageCanvasSource2D,
    vtkImageSinusoidSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source 1: a sinusoidal pattern
source_0 = vtkImageSinusoidSource()
source_0.SetWholeExtent(0, 255, 0, 255, 0, 0)
source_0.SetDirection(1.0, 0.5, 0.0)
source_0.SetPeriod(80.0)
source_0.SetAmplitude(200.0)
source_0.Update()

# Source 2: a canvas with geometric shapes
source_1 = vtkImageCanvasSource2D()
source_1.SetScalarTypeToDouble()
source_1.SetExtent(0, 255, 0, 255, 0, 0)
source_1.SetDrawColor(0)
source_1.FillBox(0, 255, 0, 255)
source_1.SetDrawColor(200)
source_1.FillBox(50, 200, 50, 200)
source_1.SetDrawColor(100)
source_1.DrawCircle(128, 128, 80)
source_1.Update()

# Filter: compute the weighted sum of the two images (0.6 × source_0 + 0.4 × source_1)
weighted_sum = vtkImageWeightedSum()
weighted_sum.AddInputConnection(source_0.GetOutputPort())
weighted_sum.AddInputConnection(source_1.GetOutputPort())
weighted_sum.SetWeight(0, 0.6)
weighted_sum.SetWeight(1, 0.4)

# Cast: convert all outputs to unsigned char for display
cast_0 = vtkImageCast()
cast_0.SetInputConnection(source_0.GetOutputPort())
cast_0.SetOutputScalarTypeToUnsignedChar()
cast_0.ClampOverflowOn()

cast_1 = vtkImageCast()
cast_1.SetInputConnection(source_1.GetOutputPort())
cast_1.SetOutputScalarTypeToUnsignedChar()
cast_1.ClampOverflowOn()

cast_sum = vtkImageCast()
cast_sum.SetInputConnection(weighted_sum.GetOutputPort())
cast_sum.SetOutputScalarTypeToUnsignedChar()
cast_sum.ClampOverflowOn()

# Actor 1: display the sinusoidal image
actor_0 = vtkImageActor()
actor_0.GetMapper().SetInputConnection(cast_0.GetOutputPort())

# Actor 2: display the canvas image
actor_1 = vtkImageActor()
actor_1.GetMapper().SetInputConnection(cast_1.GetOutputPort())

# Actor 3: display the weighted sum
actor_2 = vtkImageActor()
actor_2.GetMapper().SetInputConnection(cast_sum.GetOutputPort())

# Renderer 1: left viewport — sinusoidal input
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_0.SetBackground(slate_gray_background_rgb)
renderer_0.ResetCamera()

# Renderer 2: center viewport — canvas input
renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_1.SetBackground(slate_gray_background_rgb)
renderer_1.ResetCamera()

# Renderer 3: right viewport — weighted sum result
renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_2.SetBackground(slate_gray_background_rgb)
renderer_2.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetWindowName("sum")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
