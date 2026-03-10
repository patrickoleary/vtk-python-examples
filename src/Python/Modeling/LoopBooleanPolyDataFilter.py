#!/usr/bin/env python

# Demonstrate vtkLoopBooleanPolyDataFilter to compute the boolean
# intersection of two overlapping spheres.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersGeneral import vtkLoopBooleanPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
gold_rgb = (1.000, 0.843, 0.000)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: left sphere
sphere_a = vtkSphereSource()
sphere_a.SetCenter(-0.4, 0, 0)
sphere_a.SetPhiResolution(64)
sphere_a.SetThetaResolution(64)

# Source: right sphere
sphere_b = vtkSphereSource()
sphere_b.SetCenter(0.4, 0, 0)
sphere_b.SetPhiResolution(64)
sphere_b.SetThetaResolution(64)

# Filter: boolean intersection of the two spheres
boolean_filter = vtkLoopBooleanPolyDataFilter()
boolean_filter.SetInputConnection(0, sphere_a.GetOutputPort())
boolean_filter.SetInputConnection(1, sphere_b.GetOutputPort())
boolean_filter.SetOperationToIntersection()

# Mapper: map the boolean result to graphics primitives
bool_mapper = vtkPolyDataMapper()
bool_mapper.SetInputConnection(boolean_filter.GetOutputPort())
bool_mapper.ScalarVisibilityOff()

# Actor: assign the boolean result geometry
bool_actor = vtkActor()
bool_actor.SetMapper(bool_mapper)
bool_actor.GetProperty().SetColor(gold_rgb)

# Mapper/Actor: translucent left sphere for context
mapper_a = vtkPolyDataMapper()
mapper_a.SetInputConnection(sphere_a.GetOutputPort())

actor_a = vtkActor()
actor_a.SetMapper(mapper_a)
actor_a.GetProperty().SetColor(tomato_rgb)
actor_a.GetProperty().SetOpacity(0.2)

# Mapper/Actor: translucent right sphere for context
mapper_b = vtkPolyDataMapper()
mapper_b.SetInputConnection(sphere_b.GetOutputPort())

actor_b = vtkActor()
actor_b.SetMapper(mapper_b)
actor_b.GetProperty().SetColor(cornflower_blue_rgb)
actor_b.GetProperty().SetOpacity(0.2)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor_a)
renderer.AddActor(actor_b)
renderer.AddActor(bool_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("LoopBooleanPolyDataFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
