#!/usr/bin/env python

# Compute the cross-correlation of two images using vtkImageCorrelation
# and display the correlation map.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageCorrelation
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

# Source 1: create a 128x128 image with a bright square
canvas1 = vtkImageCanvasSource2D()
canvas1.SetExtent(0, 127, 0, 127, 0, 0)
canvas1.SetScalarTypeToFloat()
canvas1.SetNumberOfScalarComponents(1)
canvas1.SetDrawColor(0)
canvas1.FillBox(0, 127, 0, 127)
canvas1.SetDrawColor(255)
canvas1.FillBox(40, 90, 40, 90)
canvas1.Update()

# Source 2: create a small 21x21 template (bright square)
canvas2 = vtkImageCanvasSource2D()
canvas2.SetExtent(0, 20, 0, 20, 0, 0)
canvas2.SetScalarTypeToFloat()
canvas2.SetNumberOfScalarComponents(1)
canvas2.SetDrawColor(0)
canvas2.FillBox(0, 20, 0, 20)
canvas2.SetDrawColor(255)
canvas2.FillBox(5, 15, 5, 15)
canvas2.Update()

# Correlation: compute cross-correlation of image with template
correlation = vtkImageCorrelation()
correlation.SetDimensionality(2)
correlation.SetInput1Data(canvas1.GetOutput())
correlation.SetInput2Data(canvas2.GetOutput())
correlation.Update()

# ShiftScale: normalize correlation values to [0, 255] for display
corr_range = correlation.GetOutput().GetScalarRange()
shift = -corr_range[0]
scale = 255.0 / max(corr_range[1] - corr_range[0], 1.0)
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(correlation.GetOutputPort())
shift_scale.SetShift(shift)
shift_scale.SetScale(scale)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Cast original to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(canvas1.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())

# Actor 2: correlation map (right viewport)
actor_corr = vtkImageActor()
actor_corr.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer 1: left viewport — original image with bright square
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — correlation map
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_corr)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageCorrelation")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
