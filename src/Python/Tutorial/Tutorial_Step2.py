#!/usr/bin/env python

# Tutorial Step 2: add an observer callback that prints camera position.

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
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Source: create a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(midnight_blue_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Tutorial_Step2")


# Observer: VTK uses a command/observer design pattern. Any vtkObject can
# invoke events, and observers can watch for those events. Here we observe
# the renderer's "StartEvent" which fires at the beginning of each render.
class CameraPositionCallback:
    def __init__(self, ren):
        self.renderer = ren

    def __call__(self, caller, event):
        position = self.renderer.GetActiveCamera().GetPosition()
        print(f"({position[0]:5.2f}, {position[1]:5.2f}, {position[2]:5.2f})")


callback = CameraPositionCallback(renderer)
renderer.AddObserver("StartEvent", callback)

# Animation: rotate the camera 360 degrees around the cone
for i in range(360):
    render_window.Render()
    renderer.GetActiveCamera().Azimuth(1)
