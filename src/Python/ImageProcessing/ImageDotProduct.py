#!/usr/bin/env python

# Compute the dot product of two vector images using vtkImageDotProduct
# and display the result.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShiftScale
from vtkmodules.vtkImagingMath import vtkImageDotProduct
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source 1: 256x256 RGB image with a wide horizontal yellow bar
canvas1 = vtkImageCanvasSource2D()
canvas1.SetExtent(0, 255, 0, 255, 0, 0)
canvas1.SetScalarTypeToFloat()
canvas1.SetNumberOfScalarComponents(3)
canvas1.SetDrawColor(0, 0, 0)
canvas1.FillBox(0, 255, 0, 255)
canvas1.SetDrawColor(255, 255, 0)
canvas1.FillBox(10, 245, 90, 165)
canvas1.Update()

# Source 2: 256x256 RGB image with a tall vertical cyan bar
canvas2 = vtkImageCanvasSource2D()
canvas2.SetExtent(0, 255, 0, 255, 0, 0)
canvas2.SetScalarTypeToFloat()
canvas2.SetNumberOfScalarComponents(3)
canvas2.SetDrawColor(0, 0, 0)
canvas2.FillBox(0, 255, 0, 255)
canvas2.SetDrawColor(0, 255, 255)
canvas2.FillBox(90, 165, 10, 245)
canvas2.Update()

# DotProduct: compute dot product of the two 3-component images
dot_product = vtkImageDotProduct()
dot_product.SetInput1Data(canvas1.GetOutput())
dot_product.SetInput2Data(canvas2.GetOutput())
dot_product.Update()

# ShiftScale: normalize dot product to [0, 255] for display
dot_range = dot_product.GetOutput().GetScalarRange()
scale_factor = 255.0 / max(dot_range[1], 1.0)
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(dot_product.GetOutputPort())
shift_scale.SetScale(scale_factor)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Cast originals to unsigned char for display
cast1 = vtkImageCast()
cast1.SetInputConnection(canvas1.GetOutputPort())
cast1.SetOutputScalarTypeToUnsignedChar()
cast1.ClampOverflowOn()

cast2 = vtkImageCast()
cast2.SetInputConnection(canvas2.GetOutputPort())
cast2.SetOutputScalarTypeToUnsignedChar()
cast2.ClampOverflowOn()

# Actor 1: first image (left viewport)
actor1 = vtkImageActor()
actor1.GetMapper().SetInputConnection(cast1.GetOutputPort())

# Actor 2: second image (center viewport)
actor2 = vtkImageActor()
actor2.GetMapper().SetInputConnection(cast2.GetOutputPort())

# Actor 3: dot product result (right viewport)
actor_dot = vtkImageActor()
actor_dot.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer 1: left viewport — image 1 (yellow box)
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.AddActor(actor1)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: center viewport — image 2 (cyan box)
renderer_center = vtkRenderer()
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.AddActor(actor2)
renderer_center.SetBackground(black_rgb)
renderer_center.SetActiveCamera(renderer_left.GetActiveCamera())

# Renderer 3: right viewport — dot product
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_dot)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_center)
render_window.AddRenderer(renderer_right)
render_window.SetSize(900, 300)
render_window.SetWindowName("ImageDotProduct")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
