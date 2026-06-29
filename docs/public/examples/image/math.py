#!/usr/bin/env python

# Demonstrate arithmetic operations on images using vtkImageMathematics.
# Two procedural sinusoid images are created and multiplied together.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source 1: horizontal sinusoid pattern
source_0 = vtkImageSinusoidSource()
source_0.SetWholeExtent(0, 255, 0, 255, 0, 0)
source_0.SetDirection(1.0, 0.0, 0.0)
source_0.SetPeriod(64.0)
source_0.SetAmplitude(127.0)
source_0.Update()

# Source 2: vertical sinusoid pattern
source_1 = vtkImageSinusoidSource()
source_1.SetWholeExtent(0, 255, 0, 255, 0, 0)
source_1.SetDirection(0.0, 1.0, 0.0)
source_1.SetPeriod(48.0)
source_1.SetAmplitude(127.0)
source_1.Update()

# Filter: multiply the two images to create an interference pattern
math_filter = vtkImageMathematics()
math_filter.SetOperationToMultiply()
math_filter.SetInput1Data(source_0.GetOutput())
math_filter.SetInput2Data(source_1.GetOutput())

# Cast: convert to unsigned char for display
cast_input_0 = vtkImageCast()
cast_input_0.SetInputConnection(source_0.GetOutputPort())
cast_input_0.SetOutputScalarTypeToUnsignedChar()
cast_input_0.ClampOverflowOn()

cast_input_1 = vtkImageCast()
cast_input_1.SetInputConnection(source_1.GetOutputPort())
cast_input_1.SetOutputScalarTypeToUnsignedChar()
cast_input_1.ClampOverflowOn()

cast_result = vtkImageCast()
cast_result.SetInputConnection(math_filter.GetOutputPort())
cast_result.SetOutputScalarTypeToUnsignedChar()
cast_result.ClampOverflowOn()

# Actor 1: display the horizontal sinusoid
actor_0 = vtkImageActor()
actor_0.GetMapper().SetInputConnection(cast_input_0.GetOutputPort())

# Actor 2: display the vertical sinusoid
actor_1 = vtkImageActor()
actor_1.GetMapper().SetInputConnection(cast_input_1.GetOutputPort())

# Actor 3: display the product image
actor_2 = vtkImageActor()
actor_2.GetMapper().SetInputConnection(cast_result.GetOutputPort())

# Renderer 1: left viewport — horizontal sinusoid
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_0.SetBackground(slate_gray_background_rgb)
renderer_0.ResetCamera()

# Renderer 2: center viewport — vertical sinusoid
renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_1.SetBackground(slate_gray_background_rgb)
renderer_1.ResetCamera()

# Renderer 3: right viewport — product (interference pattern)
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
render_window.SetWindowName("math")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
