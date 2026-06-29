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
canvas_0 = vtkImageCanvasSource2D()
canvas_0.SetExtent(0, 255, 0, 255, 0, 0)
canvas_0.SetScalarTypeToFloat()
canvas_0.SetNumberOfScalarComponents(3)
canvas_0.SetDrawColor(0, 0, 0)
canvas_0.FillBox(0, 255, 0, 255)
canvas_0.SetDrawColor(255, 255, 0)
canvas_0.FillBox(10, 245, 90, 165)
canvas_0.Update()

# Source 2: 256x256 RGB image with a tall vertical cyan bar
canvas_1 = vtkImageCanvasSource2D()
canvas_1.SetExtent(0, 255, 0, 255, 0, 0)
canvas_1.SetScalarTypeToFloat()
canvas_1.SetNumberOfScalarComponents(3)
canvas_1.SetDrawColor(0, 0, 0)
canvas_1.FillBox(0, 255, 0, 255)
canvas_1.SetDrawColor(0, 255, 255)
canvas_1.FillBox(90, 165, 10, 245)
canvas_1.Update()

# DotProduct: compute dot product of the two 3-component images
dot_product = vtkImageDotProduct()
dot_product.SetInput1Data(canvas_0.GetOutput())
dot_product.SetInput2Data(canvas_1.GetOutput())
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
cast_0 = vtkImageCast()
cast_0.SetInputConnection(canvas_0.GetOutputPort())
cast_0.SetOutputScalarTypeToUnsignedChar()
cast_0.ClampOverflowOn()

cast_1 = vtkImageCast()
cast_1.SetInputConnection(canvas_1.GetOutputPort())
cast_1.SetOutputScalarTypeToUnsignedChar()
cast_1.ClampOverflowOn()

# Actor 1: first image (left viewport)
actor_0 = vtkImageActor()
actor_0.GetMapper().SetInputConnection(cast_0.GetOutputPort())

# Actor 2: second image (center viewport)
actor_1 = vtkImageActor()
actor_1.GetMapper().SetInputConnection(cast_1.GetOutputPort())

# Actor 3: dot product result (right viewport)
actor_dot = vtkImageActor()
actor_dot.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer 1: left viewport — image 1 (yellow box)
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.AddActor(actor_0)
renderer_left.SetBackground(black_rgb)

# Renderer 2: center viewport — image 2 (cyan box)
renderer_center = vtkRenderer()
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.AddActor(actor_1)
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
render_window.SetWindowName("dot product")
render_window.SetMultiSamples(0)
render_window.SetSize(900, 300)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
interactor_style_image = vtkInteractorStyleImage()
render_window_interactor.SetInteractorStyle(interactor_style_image)
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure parallel projection for 2D image viewing
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

render_window_interactor.Initialize()
render_window_interactor.Start()
