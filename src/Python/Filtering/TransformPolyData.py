#!/usr/bin/env python

# Display a sphere at the origin (blue) and its translated copy (red)
# using vtkTransformPolyDataFilter with a vtkTransform translation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
blue_rgb = (0.0, 0.0, 1.0)
red_rgb = (1.0, 0.0, 0.0)
green_rgb = (0.0, 0.5, 0.0)

# Source: generate a sphere at the origin
sphere_source = vtkSphereSource()

# Mapper: map the original sphere to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the original sphere (blue)
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(blue_rgb)

# Transform: translate (1, 2, 3)
translation = vtkTransform()
translation.Translate(1.0, 2.0, 3.0)

# Filter: apply the transform to the sphere polydata
transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(sphere_source.GetOutputPort())
transform_filter.SetTransform(translation)

# Mapper: map the transformed sphere to graphics primitives
transformed_mapper = vtkPolyDataMapper()
transformed_mapper.SetInputConnection(transform_filter.GetOutputPort())

# Actor: assign the transformed sphere (red)
transformed_actor = vtkActor()
transformed_actor.SetMapper(transformed_mapper)
transformed_actor.GetProperty().SetColor(red_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(transformed_actor)
renderer.SetBackground(green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TransformPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
