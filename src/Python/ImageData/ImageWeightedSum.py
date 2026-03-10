#!/usr/bin/env python

# Compute a weighted sum of a Mandelbrot fractal image and a sinusoidal
# image using vtkImageWeightedSum and display all three side by side.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingMath import vtkImageWeightedSum
from vtkmodules.vtkImagingSources import (
    vtkImageMandelbrotSource,
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

# Source 1: Mandelbrot fractal image
source1 = vtkImageMandelbrotSource()
source1.SetWholeExtent(0, 255, 0, 255, 0, 0)
source1.Update()

# Cast: Mandelbrot output is float — convert to double for weighted sum
cast_to_double = vtkImageCast()
cast_to_double.SetInputConnection(source1.GetOutputPort())
cast_to_double.SetOutputScalarTypeToDouble()

# Source 2: sinusoidal image (already double)
source2 = vtkImageSinusoidSource()
source2.SetWholeExtent(0, 255, 0, 255, 0, 0)
source2.Update()

# Filter: compute the weighted sum (0.8 × Mandelbrot + 0.2 × sinusoid)
weighted_sum = vtkImageWeightedSum()
weighted_sum.AddInputConnection(cast_to_double.GetOutputPort())
weighted_sum.AddInputConnection(source2.GetOutputPort())
weighted_sum.SetWeight(0, 0.8)
weighted_sum.SetWeight(1, 0.2)

# Cast: convert all outputs to unsigned char for display
cast_source1 = vtkImageCast()
cast_source1.SetInputConnection(source1.GetOutputPort())
cast_source1.SetOutputScalarTypeToUnsignedChar()
cast_source1.ClampOverflowOn()

cast_source2 = vtkImageCast()
cast_source2.SetInputConnection(source2.GetOutputPort())
cast_source2.SetOutputScalarTypeToUnsignedChar()
cast_source2.ClampOverflowOn()

cast_sum = vtkImageCast()
cast_sum.SetInputConnection(weighted_sum.GetOutputPort())
cast_sum.SetOutputScalarTypeToUnsignedChar()
cast_sum.ClampOverflowOn()

# Actor 1: display the Mandelbrot image
actor1 = vtkImageActor()
actor1.GetMapper().SetInputConnection(cast_source1.GetOutputPort())

# Actor 2: display the sinusoidal image
actor2 = vtkImageActor()
actor2.GetMapper().SetInputConnection(cast_source2.GetOutputPort())

# Actor 3: display the weighted sum
actor3 = vtkImageActor()
actor3.GetMapper().SetInputConnection(cast_sum.GetOutputPort())

# Renderer 1: left viewport — Mandelbrot input
renderer1 = vtkRenderer()
renderer1.AddActor(actor1)
renderer1.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer1.SetBackground(slate_gray_background_rgb)
renderer1.ResetCamera()

# Renderer 2: center viewport — sinusoidal input
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
render_window.SetWindowName("ImageWeightedSum")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
