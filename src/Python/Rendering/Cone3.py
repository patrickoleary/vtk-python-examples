#!/usr/bin/env python

# Render a cone in two side-by-side viewports with independent cameras,
# then animate 60 frames of azimuth rotation before entering interactive mode.

import time

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
)

# Colors (normalized RGB)
slate_gray = (0.439, 0.502, 0.565)
light_slate_gray = (0.467, 0.533, 0.600)

# Source: generate a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map cone polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: shared cone geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: left viewport (starts with 90° azimuth offset)
renderer_left = vtkRenderer()
renderer_left.AddActor(actor)
renderer_left.SetBackground(slate_gray)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().Azimuth(90)

# Renderer: right viewport
renderer_right = vtkRenderer()
renderer_right.AddActor(actor)
renderer_right.SetBackground(light_slate_gray)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(640, 480)
render_window.SetWindowName("Cone3")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Animation: rotate both cameras 60° over 60 frames
for _ in range(60):
    time.sleep(0.03)
    render_window.Render()
    renderer_left.GetActiveCamera().Azimuth(1)
    renderer_right.GetActiveCamera().Azimuth(1)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
