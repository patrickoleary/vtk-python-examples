#!/usr/bin/env python

# Combine separate grayscale images into a single multi-component
# (RGB) image using vtkImageAppendComponents.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageAppendComponents
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

# Source 1: red channel — bright square on dark background
canvas_r = vtkImageCanvasSource2D()
canvas_r.SetExtent(0, 127, 0, 127, 0, 0)
canvas_r.SetScalarTypeToUnsignedChar()
canvas_r.SetNumberOfScalarComponents(1)
canvas_r.SetDrawColor(0)
canvas_r.FillBox(0, 127, 0, 127)
canvas_r.SetDrawColor(200)
canvas_r.FillBox(20, 80, 20, 80)
canvas_r.Update()

# Source 2: green channel — bright square offset from red
canvas_g = vtkImageCanvasSource2D()
canvas_g.SetExtent(0, 127, 0, 127, 0, 0)
canvas_g.SetScalarTypeToUnsignedChar()
canvas_g.SetNumberOfScalarComponents(1)
canvas_g.SetDrawColor(0)
canvas_g.FillBox(0, 127, 0, 127)
canvas_g.SetDrawColor(200)
canvas_g.FillBox(50, 110, 50, 110)
canvas_g.Update()

# Source 3: blue channel — uniform low intensity
canvas_b = vtkImageCanvasSource2D()
canvas_b.SetExtent(0, 127, 0, 127, 0, 0)
canvas_b.SetScalarTypeToUnsignedChar()
canvas_b.SetNumberOfScalarComponents(1)
canvas_b.SetDrawColor(50)
canvas_b.FillBox(0, 127, 0, 127)
canvas_b.Update()

# AppendComponents: combine three single-component images into RGB
append = vtkImageAppendComponents()
append.AddInputConnection(canvas_r.GetOutputPort())
append.AddInputConnection(canvas_g.GetOutputPort())
append.AddInputConnection(canvas_b.GetOutputPort())

# Actor: display the combined RGB image
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(append.GetOutputPort())

# Renderer: assemble the scene with parallel projection for 2D viewing
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("ImageAppendComponents")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
