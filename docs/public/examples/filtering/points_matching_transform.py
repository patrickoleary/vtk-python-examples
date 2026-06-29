#!/usr/bin/env python

# Demonstrate vtkPointsMatchingTransformFilter by applying various
# point-matching transforms (identity, scale, translation, rotation)
# to a sphere and rendering the original and transformed results.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkPointsMatchingTransformFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere = vtkSphereSource()
sphere.Update()

# Original sphere (left viewport)
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

# Apply scale transform: source points at half distance => 2x scale
transform_filter = vtkPointsMatchingTransformFilter()
transform_filter.SetInputConnection(sphere.GetOutputPort())
transform_filter.SetSourcePoint2(0.5, 0.0, 0.0)
transform_filter.SetSourcePoint3(0.0, 0.5, 0.0)
transform_filter.SetSourcePoint4(0.0, 0.0, 0.5)
transform_filter.Update()

scaled_mapper = vtkPolyDataMapper()
scaled_mapper.SetInputConnection(transform_filter.GetOutputPort())
scaled_mapper.ScalarVisibilityOff()

scaled_actor = vtkActor()
scaled_actor.SetMapper(scaled_mapper)
scaled_actor.GetProperty().SetColor(1.0, 0.3, 0.3)

# Apply translation transform
transform_translate = vtkPointsMatchingTransformFilter()
transform_translate.SetInputConnection(sphere.GetOutputPort())
transform_translate.SetTargetPoint1(0.5, 0.5, 0.5)
transform_translate.SetTargetPoint2(1.0, 0.5, 0.5)
transform_translate.SetTargetPoint3(0.5, 1.0, 0.5)
transform_translate.SetTargetPoint4(0.5, 0.5, 1.0)
transform_translate.Update()

translated_mapper = vtkPolyDataMapper()
translated_mapper.SetInputConnection(transform_translate.GetOutputPort())
translated_mapper.ScalarVisibilityOff()

translated_actor = vtkActor()
translated_actor.SetMapper(translated_mapper)
translated_actor.GetProperty().SetColor(0.3, 1.0, 0.3)

# Apply rotation transform (90 deg on zx plane)
transform_rotate = vtkPointsMatchingTransformFilter()
transform_rotate.SetInputConnection(sphere.GetOutputPort())
transform_rotate.SetTargetPoint1(0.0, 0.0, 0.0)
transform_rotate.SetTargetPoint2(0.5, 0.0, 0.0)
transform_rotate.SetTargetPoint3(0.0, 0.0, 0.5)
transform_rotate.SetTargetPoint4(0.0, -0.5, 0.0)
transform_rotate.Update()

rotated_mapper = vtkPolyDataMapper()
rotated_mapper.SetInputConnection(transform_rotate.GetOutputPort())
rotated_mapper.ScalarVisibilityOff()

rotated_actor = vtkActor()
rotated_actor.SetMapper(rotated_mapper)
rotated_actor.GetProperty().SetColor(0.3, 0.3, 1.0)

# Renderer with all transforms visible
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(scaled_actor)
renderer.AddActor(translated_actor)
renderer.AddActor(rotated_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetWindowName("points matching transform")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
