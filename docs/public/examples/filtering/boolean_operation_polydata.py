#!/usr/bin/env python

# Demonstrate vtkBooleanOperationPolyDataFilter by performing union,
# intersection, and difference operations on pairs of overlapping spheres.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkBooleanOperationPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

center_separation = 0.15

# Union (left)
sphere_u1 = vtkSphereSource()
sphere_u1.SetCenter(-center_separation - 2.0, 0.0, 0.0)
sphere_u2 = vtkSphereSource()
sphere_u2.SetCenter(center_separation - 2.0, 0.0, 0.0)

bool_union = vtkBooleanOperationPolyDataFilter()
bool_union.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_UNION)
bool_union.SetInputConnection(0, sphere_u1.GetOutputPort())
bool_union.SetInputConnection(1, sphere_u2.GetOutputPort())

union_mapper = vtkPolyDataMapper()
union_mapper.SetInputConnection(bool_union.GetOutputPort())
union_mapper.ScalarVisibilityOff()

union_actor = vtkActor()
union_actor.SetMapper(union_mapper)

# Intersection (center)
sphere_i1 = vtkSphereSource()
sphere_i1.SetCenter(-center_separation, 0.0, 0.0)
sphere_i2 = vtkSphereSource()
sphere_i2.SetCenter(center_separation, 0.0, 0.0)

bool_intersection = vtkBooleanOperationPolyDataFilter()
bool_intersection.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_INTERSECTION)
bool_intersection.SetInputConnection(0, sphere_i1.GetOutputPort())
bool_intersection.SetInputConnection(1, sphere_i2.GetOutputPort())

intersection_mapper = vtkPolyDataMapper()
intersection_mapper.SetInputConnection(bool_intersection.GetOutputPort())
intersection_mapper.ScalarVisibilityOff()

intersection_actor = vtkActor()
intersection_actor.SetMapper(intersection_mapper)

# Difference (right)
sphere_d1 = vtkSphereSource()
sphere_d1.SetCenter(-center_separation + 2.0, 0.0, 0.0)
sphere_d2 = vtkSphereSource()
sphere_d2.SetCenter(center_separation + 2.0, 0.0, 0.0)

bool_difference = vtkBooleanOperationPolyDataFilter()
bool_difference.SetOperation(vtkBooleanOperationPolyDataFilter.VTK_DIFFERENCE)
bool_difference.SetInputConnection(0, sphere_d1.GetOutputPort())
bool_difference.SetInputConnection(1, sphere_d2.GetOutputPort())

difference_mapper = vtkPolyDataMapper()
difference_mapper.SetInputConnection(bool_difference.GetOutputPort())
difference_mapper.ScalarVisibilityOff()

difference_actor = vtkActor()
difference_actor.SetMapper(difference_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(union_actor)
renderer.AddActor(intersection_actor)
renderer.AddActor(difference_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("boolean operation polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
