#!/usr/bin/env python

# Tutorial Step 3: use multiple renderers within a single render window.

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
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.0, 0.894, 0.882)
royal_blue_rgb = (0.255, 0.412, 0.882)
dodger_blue_rgb = (0.118, 0.565, 1.0)

# Source: create a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry (shared between both renderers)
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer 1: left viewport — the same actor can be added to multiple
# renderers. Each renderer is like a viewport: it is part or all of a
# window and is responsible for drawing the actors it has.
renderer_left = vtkRenderer()
renderer_left.AddActor(cone_actor)
renderer_left.SetBackground(royal_blue_rgb)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)

# Renderer 2: right viewport with a different background color
renderer_right = vtkRenderer()
renderer_right.AddActor(cone_actor)
renderer_right.SetBackground(dodger_blue_rgb)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(600, 300)
render_window.SetWindowName("Tutorial_Step3")

# Camera: set the left view 90 degrees from the right
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().Azimuth(90)

# Animation: rotate both cameras 360 degrees
for i in range(360):
    render_window.Render()
    renderer_left.GetActiveCamera().Azimuth(1)
    renderer_right.GetActiveCamera().Azimuth(1)
