#!/usr/bin/env python

# Render two cones with different material properties (one using
# GetProperty(), the other via an explicit vtkProperty), then animate
# 60 frames of azimuth rotation before entering interactive mode.

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
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock = (0.200, 0.631, 0.788)
tomato = (1.0, 0.388, 0.278)
light_slate_gray = (0.467, 0.533, 0.600)

# Source: generate a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map cone polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor 1: blue-green cone with specular highlights
actor1 = vtkActor()
actor1.SetMapper(mapper)
actor1.GetProperty().SetColor(peacock)
actor1.GetProperty().SetDiffuse(0.7)
actor1.GetProperty().SetSpecular(0.4)
actor1.GetProperty().SetSpecularPower(20)

# Property: explicit property for the second cone
prop2 = vtkProperty()
prop2.SetColor(tomato)
prop2.SetDiffuse(0.7)
prop2.SetSpecular(0.4)
prop2.SetSpecularPower(20)

# Actor 2: red cone offset upward, sharing the same mapper
actor2 = vtkActor()
actor2.SetMapper(mapper)
actor2.SetProperty(prop2)
actor2.SetPosition(0, 2, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor1)
renderer.AddActor(actor2)
renderer.SetBackground(light_slate_gray)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Cone4")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Animation: rotate the camera 60° over 60 frames
for _ in range(60):
    time.sleep(0.03)
    render_window.Render()
    renderer.GetActiveCamera().Azimuth(1)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
