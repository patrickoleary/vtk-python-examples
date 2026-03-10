#!/usr/bin/env python

# Extract the connected region containing a seed point from a binary
# image using vtkImageSeedConnectivity.  The left viewport shows the
# full binary input with multiple white shapes; the right shows only
# the shape connected to the seed — all other shapes are removed.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingMorphological import vtkImageSeedConnectivity
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

# Source: create a 256x256 binary canvas with several disconnected shapes
canvas = vtkImageCanvasSource2D()
canvas.SetExtent(0, 255, 0, 255, 0, 0)
canvas.SetScalarTypeToUnsignedChar()
canvas.SetNumberOfScalarComponents(1)
canvas.SetDrawColor(0)
canvas.FillBox(0, 255, 0, 255)
canvas.SetDrawColor(255)
canvas.FillBox(10, 60, 190, 240)
canvas.FillBox(100, 160, 190, 240)
canvas.FillBox(190, 245, 190, 245)
canvas.FillBox(10, 70, 10, 70)
canvas.FillBox(110, 170, 10, 70)
canvas.FillBox(200, 245, 80, 140)
canvas.Update()

# SeedConnectivity: extract only the region connected to seed (30, 30)
connectivity = vtkImageSeedConnectivity()
connectivity.SetInputConnection(canvas.GetOutputPort())
connectivity.AddSeed(30, 30, 0)
connectivity.SetInputConnectValue(255)
connectivity.SetOutputConnectedValue(255)
connectivity.SetOutputUnconnectedValue(0)
connectivity.SetDimensionality(2)

# Actor 1: full binary input (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(canvas.GetOutputPort())

# Actor 2: seed-connected region only (right viewport)
actor_connected = vtkImageActor()
actor_connected.GetMapper().SetInputConnection(connectivity.GetOutputPort())

# Renderer 1: left viewport — all shapes
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — only the seed-connected region
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_connected)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageConnectivity")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
