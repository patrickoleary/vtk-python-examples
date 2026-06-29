#!/usr/bin/env python
# Demonstrate vtkCellLocator with IntersectWithLine, FindClosestPoint, and FindClosestPointWithinRadius.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import reference
from vtkmodules.vtkCommonDataModel import vtkCellLocator
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Main sphere.
sphere = vtkSphereSource()
sphere.SetThetaResolution(8)
sphere.SetPhiResolution(8)
sphere.SetRadius(1.0)
sphere.Update()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Spot glyph for marking intersection/closest points.
spot = vtkSphereSource()
spot.SetPhiResolution(6)
spot.SetThetaResolution(6)
spot.SetRadius(0.1)
spot_mapper = vtkPolyDataMapper()
spot_mapper.SetInputConnection(spot.GetOutputPort())

# Build a cell locator.
cell_locator = vtkCellLocator()
cell_locator.SetDataSet(sphere.GetOutput())
cell_locator.BuildLocator()

# IntersectWithLine.
p1 = [2.0, 1.0, 3.0]
p2 = [0.0, 0.0, 0.0]
t_val = reference(0.0)
pt_line = [0.0, 0.0, 0.0]
pcoords = [0.0, 0.0, 0.0]
sub_id = reference(0)
cell_id = reference(0)
cell_locator.IntersectWithLine(p1, p2, 0.001, t_val, pt_line, pcoords, sub_id, cell_id)

intersect_actor = vtkActor()
intersect_actor.SetMapper(spot_mapper)
intersect_actor.SetPosition(pt_line[0], pt_line[1], pt_line[2])
intersect_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# FindClosestPoint.
cell_id_c = reference(0)
dist = reference(0.0)
p1_close = [-2.4, -0.9, 0.0]
pt_close = [0.0, 0.0, 0.0]
sub_id_c = reference(0)
cell_locator.FindClosestPoint(p1_close, pt_close, cell_id_c, sub_id_c, dist)

closest_actor = vtkActor()
closest_actor.SetMapper(spot_mapper)
closest_actor.SetPosition(pt_close[0], pt_close[1], pt_close[2])
closest_actor.GetProperty().SetColor(0.0, 1.0, 0.0)

# FindClosestPointWithinRadius.
radius = 5.0
p1_radius = [0.2, 1.0, 1.0]
pt_radius = [0.0, 0.0, 0.0]
cell_id_r = reference(0)
sub_id_r = reference(0)
dist_r = reference(0.0)
cell_locator.FindClosestPointWithinRadius(p1_radius, radius, pt_radius, cell_id_r, sub_id_r, dist_r)

closest_actor_2 = vtkActor()
closest_actor_2.SetMapper(spot_mapper)
closest_actor_2.SetPosition(pt_radius[0], pt_radius[1], pt_radius[2])
closest_actor_2.GetProperty().SetColor(0.0, 1.0, 0.0)

renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(intersect_actor)
renderer.AddActor(closest_actor)
renderer.AddActor(closest_actor_2)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cell locator")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
