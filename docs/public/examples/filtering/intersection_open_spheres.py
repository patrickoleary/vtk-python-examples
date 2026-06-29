#!/usr/bin/env python

# Demonstrate vtkIntersectionPolyDataFilter on two partially open spheres,
# exercising the edge case of non-enclosed surfaces. Renders both split
# surfaces with the intersection curve.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkIntersectionPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# First sphere: partial (open)
sphere_0 = vtkSphereSource()
sphere_0.SetStartTheta(0.0)
sphere_0.SetEndTheta(305.0)

tri_0 = vtkTriangleFilter()
tri_0.SetInputConnection(sphere_0.GetOutputPort())

# Second sphere: offset
sphere_1 = vtkSphereSource()
sphere_1.SetCenter(0.2, 0.0, 0.0)

tri_1 = vtkTriangleFilter()
tri_1.SetInputConnection(sphere_1.GetOutputPort())

# Compute intersection with splitting
intersection = vtkIntersectionPolyDataFilter()
intersection.SetInputConnection(0, tri_0.GetOutputPort())
intersection.SetInputConnection(1, tri_1.GetOutputPort())
intersection.SplitFirstOutputOn()
intersection.SplitSecondOutputOn()
intersection.Update()

# Intersection curve
intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)
intersection_actor.GetProperty().SetColor(1, 1, 0)
intersection_actor.GetProperty().SetLineWidth(3.0)

# First split output
split_mapper_0 = vtkPolyDataMapper()
split_mapper_0.SetInputConnection(intersection.GetOutputPort(1))
split_mapper_0.ScalarVisibilityOff()

split_actor_0 = vtkActor()
split_actor_0.SetMapper(split_mapper_0)
split_actor_0.GetProperty().SetOpacity(0.3)
split_actor_0.GetProperty().SetColor(1, 0, 0)

# Second split output
split_mapper_1 = vtkPolyDataMapper()
split_mapper_1.SetInputConnection(intersection.GetOutputPort(2))
split_mapper_1.ScalarVisibilityOff()

split_actor_1 = vtkActor()
split_actor_1.SetMapper(split_mapper_1)
split_actor_1.GetProperty().SetOpacity(0.3)
split_actor_1.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(intersection_actor)
renderer.AddActor(split_actor_0)
renderer.AddActor(split_actor_1)
renderer.SetBackground(0.1, 0.2, 0.3)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("intersection open spheres")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
