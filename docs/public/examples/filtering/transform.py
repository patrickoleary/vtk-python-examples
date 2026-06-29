#!/usr/bin/env python

# Demonstrate vtkTransformFilter by creating a sphere, applying a random
# affine transform, and rendering the original and transformed meshes
# side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
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
sphere.SetPhiResolution(16)
sphere.SetThetaResolution(16)

# Create a transform (rotation + scale)
transform = vtkTransform()
transform.RotateX(45)
transform.RotateZ(30)
transform.Scale(1.5, 0.8, 1.2)

# Apply the transform
transform_filter = vtkTransformFilter()
transform_filter.SetTransformAllInputVectors(True)
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(sphere.GetOutputPort())

# Left viewport: original sphere
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere.GetOutputPort())

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(0.8, 0.8, 0.8)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(original_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

# Right viewport: transformed sphere
transformed_mapper = vtkPolyDataMapper()
transformed_mapper.SetInputConnection(transform_filter.GetOutputPort())

transformed_actor = vtkActor()
transformed_actor.SetMapper(transformed_mapper)
transformed_actor.GetProperty().SetColor(1.0, 0.4, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddActor(transformed_actor)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(800, 400)
render_window.SetWindowName("transform")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
