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
source1 = vtkImageSinusoidSource()
source1.SetWholeExtent(0, 255, 0, 255, 0, 0)
source1.SetDirection(1.0, 0.0, 0.0)
source1.SetPeriod(64.0)
source1.SetAmplitude(127.0)
source1.Update()

# Source 2: vertical sinusoid pattern
source2 = vtkImageSinusoidSource()
source2.SetWholeExtent(0, 255, 0, 255, 0, 0)
source2.SetDirection(0.0, 1.0, 0.0)
source2.SetPeriod(48.0)
source2.SetAmplitude(127.0)
source2.Update()

# Filter: multiply the two images to create an interference pattern
math_filter = vtkImageMathematics()
math_filter.SetOperationToMultiply()
math_filter.SetInput1Data(source1.GetOutput())
math_filter.SetInput2Data(source2.GetOutput())

# Cast: convert to unsigned char for display
cast_input1 = vtkImageCast()
cast_input1.SetInputConnection(source1.GetOutputPort())
cast_input1.SetOutputScalarTypeToUnsignedChar()
cast_input1.ClampOverflowOn()

cast_input2 = vtkImageCast()
cast_input2.SetInputConnection(source2.GetOutputPort())
cast_input2.SetOutputScalarTypeToUnsignedChar()
cast_input2.ClampOverflowOn()

cast_result = vtkImageCast()
cast_result.SetInputConnection(math_filter.GetOutputPort())
cast_result.SetOutputScalarTypeToUnsignedChar()
cast_result.ClampOverflowOn()

# Actor 1: display the horizontal sinusoid
actor1 = vtkImageActor()
actor1.GetMapper().SetInputConnection(cast_input1.GetOutputPort())

# Actor 2: display the vertical sinusoid
actor2 = vtkImageActor()
actor2.GetMapper().SetInputConnection(cast_input2.GetOutputPort())

# Actor 3: display the product image
actor3 = vtkImageActor()
actor3.GetMapper().SetInputConnection(cast_result.GetOutputPort())

# Renderer 1: left viewport — horizontal sinusoid
renderer1 = vtkRenderer()
renderer1.AddActor(actor1)
renderer1.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer1.SetBackground(slate_gray_background_rgb)
renderer1.ResetCamera()

# Renderer 2: center viewport — vertical sinusoid
renderer2 = vtkRenderer()
renderer2.AddActor(actor2)
renderer2.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer2.SetBackground(slate_gray_background_rgb)
renderer2.ResetCamera()

# Renderer 3: right viewport — product (interference pattern)
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
render_window.SetWindowName("ImageMath")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
