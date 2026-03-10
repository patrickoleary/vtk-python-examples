#!/usr/bin/env python

# Tutorial Step 1: create a cone and render it rotating 360 degrees.

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

# Source: create a cone with specified height, radius, and resolution.
# vtkConeSource is a source process object that produces vtkPolyData.
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map the polygonal data into graphics primitives.
# Intermediate filters such as vtkShrinkPolyData could be inserted
# between the source and the mapper.
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: orchestrate rendering of the mapper's graphics primitives.
# An actor also refers to properties via a vtkProperty instance and
# includes an internal transformation matrix.
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer: a viewport responsible for drawing its actors.
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Tutorial_Step1")

# Animation: rotate the camera 360 degrees around the cone
for i in range(360):
    render_window.Render()
    renderer.GetActiveCamera().Azimuth(1)
