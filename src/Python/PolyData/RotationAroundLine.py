#!/usr/bin/env python

# Show an arrow rotated 45 degrees around the z-axis using vtkTransformPolyDataFilter.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkArrowSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_coral_rgb = (0.941, 0.502, 0.502)
pale_turquoise_rgb = (0.686, 0.933, 0.933)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: arrow
arrow_source = vtkArrowSource()

# Filter: rotate the arrow 45 degrees around the z-axis
transform = vtkTransform()
transform.RotateWXYZ(45, 0, 0, 1)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(arrow_source.GetOutputPort())

# Mapper & Actor: map original arrow to graphics primitives
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(arrow_source.GetOutputPort())

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(light_coral_rgb)

# Mapper & Actor: map rotated arrow to graphics primitives
rotated_mapper = vtkPolyDataMapper()
rotated_mapper.SetInputConnection(transform_filter.GetOutputPort())

rotated_actor = vtkActor()
rotated_actor.SetMapper(rotated_mapper)
rotated_actor.GetProperty().SetColor(pale_turquoise_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(rotated_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RotationAroundLine")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
