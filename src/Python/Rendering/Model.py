#!/usr/bin/env python

# Display a cone, sphere, and cube in three viewports within a single
# render window, each with a different background colour.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock = (0.200, 0.631, 0.788)
salmon = (0.980, 0.502, 0.447)
melon = (0.890, 0.655, 0.584)
light_gray = (0.902, 0.902, 0.902)
linen = (0.980, 0.941, 0.902)
honeydew = (0.941, 1.0, 0.941)

# Source: cone
cone = vtkConeSource()
cone.SetResolution(8)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(peacock)

# Source: sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(16)
sphere.SetPhiResolution(16)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(melon)

# Source: cube
cube = vtkCubeSource()

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(salmon)

# Renderer: left third — cone
renderer_left = vtkRenderer()
renderer_left.AddActor(cone_actor)
renderer_left.SetBackground(light_gray)
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)

# Renderer: centre third — sphere
renderer_centre = vtkRenderer()
renderer_centre.AddActor(sphere_actor)
renderer_centre.SetBackground(linen)
renderer_centre.SetViewport(0.333, 0.0, 0.666, 1.0)

# Renderer: right third — cube
renderer_right = vtkRenderer()
renderer_right.AddActor(cube_actor)
renderer_right.SetBackground(honeydew)
renderer_right.SetViewport(0.666, 0.0, 1.0, 1.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_centre)
render_window.AddRenderer(renderer_right)
render_window.SetSize(900, 300)
render_window.SetWindowName("Model")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
