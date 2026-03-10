#!/usr/bin/env python

# Draw 2D shapes (box, triangle, circle) on a procedural image canvas
# using vtkImageCanvasSource2D.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
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

# Source: create a 256x256 RGB canvas
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(3)

# Fill the background with dark gray
canvas.SetDrawColor(64, 64, 64)
canvas.FillBox(0, 255, 0, 255)

# Draw a red filled box
canvas.SetDrawColor(255, 50, 50)
canvas.FillBox(20, 100, 20, 100)

# Draw a green filled triangle
canvas.SetDrawColor(50, 255, 50)
canvas.FillTriangle(150, 20, 240, 20, 195, 100)

# Draw a blue filled circle
canvas.SetDrawColor(50, 100, 255)
canvas.DrawCircle(128, 190, 50)

canvas.Update()

# Actor: display the canvas image
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(canvas.GetOutputPort())

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
render_window.SetWindowName("ImageCanvasSource2D")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
