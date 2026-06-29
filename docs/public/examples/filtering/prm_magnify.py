#!/usr/bin/env python
# Demonstrate image magnification comparable to vtkParallelRenderManager.
#
# The C++ PrmMagnify test subclasses vtkParallelRenderManager to generate
# a Mandelbrot image at reduced resolution and then magnify it into four
# quadrants using nearest-neighbor (top-left, bottom-left) and linear
# (top-right, bottom-right) interpolation in both RGBA and RGB modes.
#
# vtkParallelRenderManager and vtkDummyController are not available in the
# Python VTK wheel, so this example replicates the visual concept: a
# reduced-resolution Mandelbrot fractal is magnified to full resolution
# using nearest-neighbor and linear interpolation displayed side by side
# in four viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import (
    vtkImageMagnify,
    vtkImageShiftScale,
)
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate a small Mandelbrot image (reduced resolution, as the PRM would)
mandelbrot = vtkImageMandelbrotSource()
mandelbrot.SetWholeExtent(0, 31, 0, 31, 0, 0)
mandelbrot.SetMaximumNumberOfIterations(255)

# Convert to unsigned char for display
char_image = vtkImageShiftScale()
char_image.SetInputConnection(mandelbrot.GetOutputPort())
char_image.SetShift(0)
char_image.SetScale(1)
char_image.SetOutputScalarTypeToUnsignedChar()

# Magnify with nearest-neighbor interpolation (8x, like reduction factor 8)
magnify_nearest = vtkImageMagnify()
magnify_nearest.SetInputConnection(char_image.GetOutputPort())
magnify_nearest.SetMagnificationFactors(8, 8, 1)
magnify_nearest.InterpolateOff()

# Magnify with linear interpolation (8x)
magnify_linear = vtkImageMagnify()
magnify_linear.SetInputConnection(char_image.GetOutputPort())
magnify_linear.SetMagnificationFactors(8, 8, 1)
magnify_linear.InterpolateOn()

# Bottom-left: nearest (RGBA-like)
actor_0 = vtkImageActor()
actor_0.GetMapper().SetInputConnection(magnify_nearest.GetOutputPort())
actor_0.InterpolateOff()

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_0.SetBackground(1, 0, 0)
renderer_0.AddActor(actor_0)

# Bottom-right: linear (RGBA-like)
actor_1 = vtkImageActor()
actor_1.GetMapper().SetInputConnection(magnify_linear.GetOutputPort())
actor_1.InterpolateOff()

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_1.SetBackground(1, 0, 0)
renderer_1.AddActor(actor_1)

# Top-left: nearest (RGB-like)
actor_2 = vtkImageActor()
actor_2.GetMapper().SetInputConnection(magnify_nearest.GetOutputPort())
actor_2.InterpolateOff()

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.SetBackground(1, 0, 0)
renderer_2.AddActor(actor_2)

# Top-right: linear (RGB-like)
actor_3 = vtkImageActor()
actor_3.GetMapper().SetInputConnection(magnify_linear.GetOutputPort())
actor_3.InterpolateOff()

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.SetBackground(1, 0, 0)
renderer_3.AddActor(actor_3)

render_window = vtkRenderWindow()
render_window.SetSize(256, 256)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("prm magnify")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()
renderer_3.ResetCamera()

interactor.Initialize()
interactor.Start()
