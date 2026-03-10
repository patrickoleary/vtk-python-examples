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
source1 = vtkImageSinusoidSource()
source1.SetWholeExtent(0, 255, 0, 255, 0, 0)
source1.SetDirection(1.0, 0.5, 0.0)
source1.SetPeriod(80.0)
source1.SetAmplitude(200.0)
source1.Update()

# Source 2: a canvas with geometric shapes
source2 = vtkImageCanvasSource2D()
source2.SetScalarTypeToDouble()
source2.SetExtent(0, 255, 0, 255, 0, 0)
source2.SetDrawColor(0)
source2.FillBox(0, 255, 0, 255)
source2.SetDrawColor(200)
source2.FillBox(50, 200, 50, 200)
source2.SetDrawColor(100)
source2.DrawCircle(128, 128, 80)
source2.Update()

# Filter: compute the weighted sum of the two images (0.6 × source1 + 0.4 × source2)
weighted_sum = vtkImageWeightedSum()
weighted_sum.AddInputConnection(source1.GetOutputPort())
weighted_sum.AddInputConnection(source2.GetOutputPort())
weighted_sum.SetWeight(0, 0.6)
weighted_sum.SetWeight(1, 0.4)

# Cast: convert all outputs to unsigned char for display
cast1 = vtkImageCast()
cast1.SetInputConnection(source1.GetOutputPort())
cast1.SetOutputScalarTypeToUnsignedChar()
cast1.ClampOverflowOn()

cast2 = vtkImageCast()
cast2.SetInputConnection(source2.GetOutputPort())
cast2.SetOutputScalarTypeToUnsignedChar()
cast2.ClampOverflowOn()

cast_sum = vtkImageCast()
cast_sum.SetInputConnection(weighted_sum.GetOutputPort())
cast_sum.SetOutputScalarTypeToUnsignedChar()
cast_sum.ClampOverflowOn()

# Actor 1: display the sinusoidal image
actor1 = vtkImageActor()
actor1.GetMapper().SetInputConnection(cast1.GetOutputPort())

# Actor 2: display the canvas image
actor2 = vtkImageActor()
actor2.GetMapper().SetInputConnection(cast2.GetOutputPort())

# Actor 3: display the weighted sum
actor3 = vtkImageActor()
actor3.GetMapper().SetInputConnection(cast_sum.GetOutputPort())

# Renderer 1: left viewport — sinusoidal input
renderer1 = vtkRenderer()
renderer1.AddActor(actor1)
renderer1.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer1.SetBackground(slate_gray_background_rgb)
renderer1.ResetCamera()

# Renderer 2: center viewport — canvas input
renderer2 = vtkRenderer()
renderer2.AddActor(actor2)
renderer2.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer2.SetBackground(slate_gray_background_rgb)
renderer2.ResetCamera()

# Renderer 3: right viewport — weighted sum result
renderer3 = vtkRenderer()
renderer3.AddActor(actor3)
renderer3.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer3.SetBackground(slate_gray_background_rgb)
renderer3.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer1)
render_window.AddRenderer(renderer2)
render_window.AddRenderer(renderer3)
render_window.SetSize(900, 300)
render_window.SetWindowName("SumVTKImages")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
