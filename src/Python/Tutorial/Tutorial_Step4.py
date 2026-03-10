#!/usr/bin/env python

# Tutorial Step 4: multiple actors with different properties and transformations.

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
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
cornflower_blue_rgb = (0.392, 0.584, 0.929)

# Source: create a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor 1: modify surface properties directly via GetProperty().
# By default, an actor is created with a vtkProperty so GetProperty()
# can be used immediately to set color, diffuse, and specular values.
cone_actor1 = vtkActor()
cone_actor1.SetMapper(cone_mapper)
cone_actor1.GetProperty().SetColor(0.2, 0.63, 0.79)
cone_actor1.GetProperty().SetDiffuse(0.7)
cone_actor1.GetProperty().SetSpecular(0.4)
cone_actor1.GetProperty().SetSpecularPower(20)

# Property: create a standalone vtkProperty and assign it to a second actor.
# A single property can be shared among many actors. Here we create one
# independently, configure it, and assign it with SetProperty().
cone_property = vtkProperty()
cone_property.SetColor(tomato_rgb)
cone_property.SetDiffuse(0.7)
cone_property.SetSpecular(0.4)
cone_property.SetSpecularPower(20)

# Actor 2: reuses the same mapper (avoiding geometry duplication) but has
# a different property and is translated to a different position.
cone_actor2 = vtkActor()
cone_actor2.SetMapper(cone_mapper)
cone_actor2.SetProperty(cone_property)
cone_actor2.SetPosition(0, 2, 0)

# Renderer: assemble the scene with both actors
renderer = vtkRenderer()
renderer.AddActor(cone_actor1)
renderer.AddActor(cone_actor2)
renderer.SetBackground(cornflower_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Tutorial_Step4")

# Animation: rotate the camera 360 degrees around both cones
for i in range(360):
    render_window.Render()
    renderer.GetActiveCamera().Azimuth(1)
