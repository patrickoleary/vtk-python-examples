#!/usr/bin/env python

# Apply morphological opening and closing to a binary image using
# vtkImageOpenClose3D and display original, opened, and closed
# images in a 3-viewport layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingMorphological import vtkImageOpenClose3D
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

# Source: 256x256 binary canvas with features that respond to open/close
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(1)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(255)
# Large rectangle with small holes (closing will fill these)
canvas.FillBox(20, 120, 140, 240)
canvas.SetDrawColor(0)
canvas.FillBox(50, 56, 170, 176)
canvas.FillBox(80, 86, 200, 206)
canvas.FillBox(40, 44, 210, 214)
canvas.SetDrawColor(255)
# Small bright dots (opening will remove these)
canvas.FillBox(150, 156, 220, 226)
canvas.FillBox(180, 184, 200, 204)
canvas.FillBox(210, 214, 230, 234)
# Thin horizontal bridge (opening will break it)
canvas.FillBox(20, 230, 95, 99)
# Two large blocks connected by a thin vertical bridge (opening breaks bridge)
canvas.FillBox(20, 80, 10, 70)
canvas.FillBox(20, 80, 110, 130)
canvas.FillBox(45, 55, 70, 110)
canvas.Update()

# Open: erode then dilate — removes small bright features and thin bridges
open_filter = vtkImageOpenClose3D()
open_filter.SetInputConnection(canvas.GetOutputPort())
open_filter.SetKernelSize(9, 9, 1)
open_filter.SetOpenValue(255)
open_filter.SetCloseValue(0)

# Close: dilate then erode — fills small dark holes
close_filter = vtkImageOpenClose3D()
close_filter.SetInputConnection(canvas.GetOutputPort())
close_filter.SetKernelSize(9, 9, 1)
close_filter.SetOpenValue(0)
close_filter.SetCloseValue(255)

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(canvas.GetOutputPort())

# Actor 2: opened image (center viewport)
actor_opened = vtkImageActor()
actor_opened.GetMapper().SetInputConnection(open_filter.GetOutputPort())

# Actor 3: closed image (right viewport)
actor_closed = vtkImageActor()
actor_closed.GetMapper().SetInputConnection(close_filter.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: center viewport — opened
renderer_center = vtkRenderer()
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.AddActor(actor_opened)
renderer_center.SetBackground(black_rgb)
renderer_center.SetActiveCamera(renderer_left.GetActiveCamera())

# Renderer 3: right viewport — closed
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_closed)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_center)
render_window.AddRenderer(renderer_right)
render_window.SetSize(900, 300)
render_window.SetWindowName("ImageOpenClose3D")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
