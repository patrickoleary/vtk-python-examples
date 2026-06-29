#!/usr/bin/env python

# Demonstrate vtkIntersectionPolyDataFilter by computing the intersection
# curve between two overlapping spheres and rendering the spheres
# (transparent) alongside the intersection line.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkIntersectionPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create two overlapping spheres
sphere_0 = vtkSphereSource()
sphere_0.SetCenter(0.0, 0.0, 0.0)
sphere_0.SetRadius(2.0)
sphere_0.SetPhiResolution(11)
sphere_0.SetThetaResolution(21)
sphere_0.Update()

sphere_mapper_0 = vtkPolyDataMapper()
sphere_mapper_0.SetInputConnection(sphere_0.GetOutputPort())
sphere_mapper_0.ScalarVisibilityOff()

sphere_actor_0 = vtkActor()
sphere_actor_0.SetMapper(sphere_mapper_0)
sphere_actor_0.GetProperty().SetOpacity(0.3)
sphere_actor_0.GetProperty().SetColor(1, 0, 0)
sphere_actor_0.GetProperty().SetInterpolationToFlat()

sphere_1 = vtkSphereSource()
sphere_1.SetCenter(1.0, 0.0, 0.0)
sphere_1.SetRadius(2.0)

sphere_mapper_1 = vtkPolyDataMapper()
sphere_mapper_1.SetInputConnection(sphere_1.GetOutputPort())
sphere_mapper_1.ScalarVisibilityOff()

sphere_actor_1 = vtkActor()
sphere_actor_1.SetMapper(sphere_mapper_1)
sphere_actor_1.GetProperty().SetOpacity(0.3)
sphere_actor_1.GetProperty().SetColor(0, 1, 0)
sphere_actor_1.GetProperty().SetInterpolationToFlat()

# Compute intersection
intersection = vtkIntersectionPolyDataFilter()
intersection.SetInputConnection(0, sphere_0.GetOutputPort())
intersection.SetInputConnection(1, sphere_1.GetOutputPort())
intersection.Update()

intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(sphere_actor_0)
renderer.AddViewProp(sphere_actor_1)
renderer.AddViewProp(intersection_actor)
renderer.SetBackground(0.1, 0.2, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("intersection polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
