#!/usr/bin/env python

# Apply boolean logic operations (AND, OR, XOR) to two binary images
# using vtkImageLogic and display all five images in a multi-viewport layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
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
source1 = vtkImageCanvasSource2D()
source1.SetScalarTypeToUnsignedChar()
source1.SetNumberOfScalarComponents(1)
source1.SetExtent(0, 255, 0, 255, 0, 0)
source1.SetDrawColor(0)
source1.FillBox(0, 255, 0, 255)
source1.SetDrawColor(255)
source1.DrawCircle(100, 128, 80)
source1.Update()

# Source 2: white rectangle on black background
source2 = vtkImageCanvasSource2D()
source2.SetScalarTypeToUnsignedChar()
source2.SetNumberOfScalarComponents(1)
source2.SetExtent(0, 255, 0, 255, 0, 0)
source2.SetDrawColor(0)
source2.FillBox(0, 255, 0, 255)
source2.SetDrawColor(255)
source2.FillBox(80, 200, 60, 200)
source2.Update()

# Filter: boolean AND — only pixels white in both inputs
logic_and = vtkImageLogic()
logic_and.SetInputConnection(0, source1.GetOutputPort())
logic_and.SetInputConnection(1, source2.GetOutputPort())
logic_and.SetOperationToAnd()
logic_and.SetOutputTrueValue(255)

# Filter: boolean OR — pixels white in either input
logic_or = vtkImageLogic()
logic_or.SetInputConnection(0, source1.GetOutputPort())
logic_or.SetInputConnection(1, source2.GetOutputPort())
logic_or.SetOperationToOr()
logic_or.SetOutputTrueValue(255)

# Filter: boolean XOR — pixels white in exactly one input
logic_xor = vtkImageLogic()
logic_xor.SetInputConnection(0, source1.GetOutputPort())
logic_xor.SetInputConnection(1, source2.GetOutputPort())
logic_xor.SetOperationToXor()
logic_xor.SetOutputTrueValue(255)

# Actor 1: source 1 (leftmost viewport)
actor1 = vtkImageActor()
actor1.GetMapper().SetInputConnection(source1.GetOutputPort())

# Actor 2: source 2
actor2 = vtkImageActor()
actor2.GetMapper().SetInputConnection(source2.GetOutputPort())

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
renderer1 = vtkRenderer()
renderer1.SetViewport(0.0, 0.0, 0.2, 1.0)
renderer1.AddActor(actor1)
renderer1.SetBackground(black_rgb)
renderer1.ResetCamera()
renderer1.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: source 2
renderer2 = vtkRenderer()
renderer2.SetViewport(0.2, 0.0, 0.4, 1.0)
renderer2.AddActor(actor2)
renderer2.SetBackground(black_rgb)
renderer2.SetActiveCamera(renderer1.GetActiveCamera())

# Renderer 3: AND
renderer3 = vtkRenderer()
renderer3.SetViewport(0.4, 0.0, 0.6, 1.0)
renderer3.AddActor(actor_and)
renderer3.SetBackground(black_rgb)
renderer3.SetActiveCamera(renderer1.GetActiveCamera())

# Renderer 4: OR
renderer4 = vtkRenderer()
renderer4.SetViewport(0.6, 0.0, 0.8, 1.0)
renderer4.AddActor(actor_or)
renderer4.SetBackground(black_rgb)
renderer4.SetActiveCamera(renderer1.GetActiveCamera())

# Renderer 5: XOR
renderer5 = vtkRenderer()
renderer5.SetViewport(0.8, 0.0, 1.0, 1.0)
renderer5.AddActor(actor_xor)
renderer5.SetBackground(black_rgb)
renderer5.SetActiveCamera(renderer1.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer1)
render_window.AddRenderer(renderer2)
render_window.AddRenderer(renderer3)
render_window.AddRenderer(renderer4)
render_window.AddRenderer(renderer5)
render_window.SetSize(1280, 256)
render_window.SetWindowName("ImageLogic")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
