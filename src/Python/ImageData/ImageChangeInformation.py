#!/usr/bin/env python

# Modify the spacing, origin, and extent of a procedural image using
# vtkImageChangeInformation and display original vs modified side by side.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageChangeInformation
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: create a 128x128 canvas with a colored box
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 127, 0, 127, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetDrawColor(40, 40, 40)
canvas.FillBox(0, 127, 0, 127)
canvas.SetDrawColor(255, 200, 50)
canvas.FillBox(30, 100, 30, 100)
canvas.Update()

# ChangeInformation: modify spacing and origin
change_info = vtkImageChangeInformation()
change_info.SetInputConnection(canvas.GetOutputPort())
change_info.SetOutputSpacing(2.0, 2.0, 1.0)
change_info.SetOutputOrigin(10.0, 20.0, 0.0)
change_info.Update()

# Read metadata for the labels
orig_img = canvas.GetOutput()
mod_img = change_info.GetOutput()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(canvas.GetOutputPort())

# Actor 2: modified image (right viewport)
actor_modified = vtkImageActor()
actor_modified.GetMapper().SetInputConnection(change_info.GetOutputPort())

# Text label 1: show original metadata
label_original = vtkTextActor()
label_original.SetInput(
    f"Original:\n"
    f"  Spacing: {orig_img.GetSpacing()}\n"
    f"  Origin:  {orig_img.GetOrigin()}"
)
label_original.GetTextProperty().SetFontSize(16)
label_original.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_original.SetPosition(10, 10)

# Text label 2: show modified metadata
label_modified = vtkTextActor()
label_modified.SetInput(
    f"Modified:\n"
    f"  Spacing: {mod_img.GetSpacing()}\n"
    f"  Origin:  {mod_img.GetOrigin()}"
)
label_modified.GetTextProperty().SetFontSize(16)
label_modified.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_modified.SetPosition(10, 10)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.AddViewProp(label_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — modified spacing/origin
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_modified)
renderer_right.AddViewProp(label_modified)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()
renderer_right.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageChangeInformation")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
