#!/usr/bin/env python

# Shift the extent of an image using vtkImageTranslateExtent and display
# original and translated images side by side with text labels showing
# the extent values so the metadata shift is clearly visible.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageTranslateExtent
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

# Source: create a 100x100 canvas with a bright orange box
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 99, 0, 99, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)
canvas.SetDrawColor(40, 40, 40)
canvas.FillBox(0, 99, 0, 99)
canvas.SetDrawColor(255, 140, 50)
canvas.FillBox(10, 90, 10, 90)
canvas.Update()

# Translate: shift the image extent by (+60, +40) in world coords
translate = vtkImageTranslateExtent()
translate.SetInputConnection(canvas.GetOutputPort())
translate.SetTranslation(60, 40, 0)
translate.Update()

# Read extents for the labels
original_extent = canvas.GetOutput().GetExtent()
translated_extent = translate.GetOutput().GetExtent()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(canvas.GetOutputPort())

# Actor 2: translated image (right viewport)
actor_translated = vtkImageActor()
actor_translated.GetMapper().SetInputConnection(translate.GetOutputPort())

# Text label 1: show original extent
label_original = vtkTextActor()
label_original.SetInput(
    f"Original extent:\n"
    f"  X: [{original_extent[0]}, {original_extent[1]}]\n"
    f"  Y: [{original_extent[2]}, {original_extent[3]}]"
)
label_original.GetTextProperty().SetFontSize(16)
label_original.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_original.SetPosition(10, 10)

# Text label 2: show translated extent
label_translated = vtkTextActor()
label_translated.SetInput(
    f"Translated extent (+60, +40):\n"
    f"  X: [{translated_extent[0]}, {translated_extent[1]}]\n"
    f"  Y: [{translated_extent[2]}, {translated_extent[3]}]"
)
label_translated.GetTextProperty().SetFontSize(16)
label_translated.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_translated.SetPosition(10, 10)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.AddViewProp(label_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — translated
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_translated)
renderer_right.AddViewProp(label_translated)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()
renderer_right.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageTranslateExtent")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
