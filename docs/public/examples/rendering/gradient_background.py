#!/usr/bin/env python

# Demonstrate the four gradient background modes available in VTK:
# vertical, horizontal, radial farthest-side, and radial farthest-corner.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkViewport,
)

# Colors (normalized RGB)
honeydew = (0.941, 1.0, 0.941)
gold = (1.0, 0.843, 0.0)
orange_red = (1.0, 0.271, 0.0)

# Source: generate a cone used in all four viewports
cone = vtkConeSource()
cone.SetResolution(25)
cone.SetDirection(0, 1, 0)
cone.SetHeight(1)

# Mapper: map cone polygon data
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: shared cone geometry with a light specular highlight
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(honeydew)
actor.GetProperty().SetSpecular(0.3)
actor.GetProperty().SetSpecularPower(60.0)

# Renderer 0: vertical gradient
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor)
renderer_0.GradientBackgroundOn()
renderer_0.SetGradientMode(vtkViewport.GradientModes.VTK_GRADIENT_VERTICAL)
renderer_0.SetBackground(gold)
renderer_0.SetBackground2(orange_red)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# Renderer 1: horizontal gradient
renderer_1 = vtkRenderer()
renderer_1.AddActor(actor)
renderer_1.GradientBackgroundOn()
renderer_1.SetGradientMode(vtkViewport.GradientModes.VTK_GRADIENT_HORIZONTAL)
renderer_1.SetBackground(gold)
renderer_1.SetBackground2(orange_red)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# Renderer 2: radial farthest side gradient
renderer_2 = vtkRenderer()
renderer_2.AddActor(actor)
renderer_2.GradientBackgroundOn()
renderer_2.SetGradientMode(vtkViewport.GradientModes.VTK_GRADIENT_RADIAL_VIEWPORT_FARTHEST_SIDE)
renderer_2.SetBackground(gold)
renderer_2.SetBackground2(orange_red)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# Renderer 3: radial farthest corner gradient
renderer_3 = vtkRenderer()
renderer_3.AddActor(actor)
renderer_3.GradientBackgroundOn()
renderer_3.SetGradientMode(vtkViewport.GradientModes.VTK_GRADIENT_RADIAL_VIEWPORT_FARTHEST_CORNER)
renderer_3.SetBackground(gold)
renderer_3.SetBackground2(orange_red)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("gradient background")
render_window.SetMultiSamples(0)
render_window.SetSize(1024, 1024)

# Scene: configure cameras
renderer_0.GetActiveCamera().Azimuth(20)
renderer_0.GetActiveCamera().Elevation(30)
renderer_0.ResetCamera()
renderer_1.GetActiveCamera().Azimuth(20)
renderer_1.GetActiveCamera().Elevation(30)
renderer_1.ResetCamera()
renderer_2.GetActiveCamera().Azimuth(20)
renderer_2.GetActiveCamera().Elevation(30)
renderer_2.ResetCamera()
renderer_3.GetActiveCamera().Azimuth(20)
renderer_3.GetActiveCamera().Elevation(30)
renderer_3.ResetCamera()

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
