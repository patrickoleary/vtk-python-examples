#!/usr/bin/env python

# Apply boolean logic operations (AND, OR, XOR) to two binary images
# using vtkImageLogic and display all five images in a multi-viewport layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingMath import vtkImageLogic
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

# Source 1: white circle on black background
source_0 = vtkImageCanvasSource2D()
source_0.SetScalarTypeToUnsignedChar()
source_0.SetNumberOfScalarComponents(1)
source_0.SetExtent(0, 255, 0, 255, 0, 0)
source_0.SetDrawColor(0)
source_0.FillBox(0, 255, 0, 255)
source_0.SetDrawColor(255)
source_0.DrawCircle(100, 128, 80)
source_0.Update()

# Source 2: white rectangle on black background
source_1 = vtkImageCanvasSource2D()
source_1.SetScalarTypeToUnsignedChar()
source_1.SetNumberOfScalarComponents(1)
source_1.SetExtent(0, 255, 0, 255, 0, 0)
source_1.SetDrawColor(0)
source_1.FillBox(0, 255, 0, 255)
source_1.SetDrawColor(255)
source_1.FillBox(80, 200, 60, 200)
source_1.Update()

# Filter: boolean AND — only pixels white in both inputs
logic_and = vtkImageLogic()
logic_and.SetInputConnection(0, source_0.GetOutputPort())
logic_and.SetInputConnection(1, source_1.GetOutputPort())
logic_and.SetOperationToAnd()
logic_and.SetOutputTrueValue(255)

# Filter: boolean OR — pixels white in either input
logic_or = vtkImageLogic()
logic_or.SetInputConnection(0, source_0.GetOutputPort())
logic_or.SetInputConnection(1, source_1.GetOutputPort())
logic_or.SetOperationToOr()
logic_or.SetOutputTrueValue(255)

# Filter: boolean XOR — pixels white in exactly one input
logic_xor = vtkImageLogic()
logic_xor.SetInputConnection(0, source_0.GetOutputPort())
logic_xor.SetInputConnection(1, source_1.GetOutputPort())
logic_xor.SetOperationToXor()
logic_xor.SetOutputTrueValue(255)

# Actor 1: source 1 (leftmost viewport)
actor_0 = vtkImageActor()
actor_0.GetMapper().SetInputConnection(source_0.GetOutputPort())

# Actor 2: source 2
actor_1 = vtkImageActor()
actor_1.GetMapper().SetInputConnection(source_1.GetOutputPort())

# Actor 3: AND result
actor_and = vtkImageActor()
actor_and.GetMapper().SetInputConnection(logic_and.GetOutputPort())

# Actor 4: OR result
actor_or = vtkImageActor()
actor_or.GetMapper().SetInputConnection(logic_or.GetOutputPort())

# Actor 5: XOR result
actor_xor = vtkImageActor()
actor_xor.GetMapper().SetInputConnection(logic_xor.GetOutputPort())

# Renderer 1: source 1
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.2, 1.0)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(black_rgb)

# Renderer 2: source 2
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.2, 0.0, 0.4, 1.0)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(black_rgb)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 3: AND
renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.4, 0.0, 0.6, 1.0)
renderer_2.AddActor(actor_and)
renderer_2.SetBackground(black_rgb)
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 4: OR
renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.6, 0.0, 0.8, 1.0)
renderer_3.AddActor(actor_or)
renderer_3.SetBackground(black_rgb)
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())

# Renderer 5: XOR
renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.8, 0.0, 1.0, 1.0)
renderer_4.AddActor(actor_xor)
renderer_4.SetBackground(black_rgb)
renderer_4.SetActiveCamera(renderer_0.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.SetWindowName("logic")
render_window.SetMultiSamples(0)
render_window.SetSize(1280, 256)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
interactor_style_image = vtkInteractorStyleImage()
render_window_interactor.SetInteractorStyle(interactor_style_image)
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure parallel projection for 2D image viewing
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().ParallelProjectionOn()

render_window_interactor.Initialize()
render_window_interactor.Start()
