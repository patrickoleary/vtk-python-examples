#!/usr/bin/env python

# Visualize the closest point on a line segment to a given point.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingFreeType import vtkVectorText

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
lime_green_rgb = (0.196, 0.804, 0.196)
steel_blue_rgb = (0.275, 0.510, 0.706)
yellow_rgb = (1.0, 1.0, 0.0)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Define the line segment endpoints and the query point
line_p0 = (0.0, 0.0, 0.0)
line_p1 = (5.0, 0.0, 0.0)
query_point = (2.0, 3.0, 0.0)

# ClosestPoint: find the closest point on the line segment.
# vtkLine.DistanceToLine (3-arg) returns the squared distance.
dist_squared = vtkLine.DistanceToLine(query_point, line_p0, line_p1)
dist = math.sqrt(dist_squared)

# Compute the closest point using the parametric line equation.
# t = dot(query - p0, p1 - p0) / dot(p1 - p0, p1 - p0), clamped to [0, 1]
d = [line_p1[i] - line_p0[i] for i in range(3)]
v = [query_point[i] - line_p0[i] for i in range(3)]
t = max(0.0, min(1.0, sum(v[i] * d[i] for i in range(3)) / sum(d[i] * d[i] for i in range(3))))
closest = [line_p0[i] + t * d[i] for i in range(3)]

# Source: sphere at the query point (red)
sphere_query = vtkSphereSource()
sphere_query.SetCenter(query_point)
sphere_query.SetRadius(0.12)
sphere_query.SetPhiResolution(16)
sphere_query.SetThetaResolution(16)

query_mapper = vtkPolyDataMapper()
query_mapper.SetInputConnection(sphere_query.GetOutputPort())

query_actor = vtkActor()
query_actor.SetMapper(query_mapper)
query_actor.GetProperty().SetColor(tomato_rgb)

# Source: sphere at the closest point (green)
sphere_closest = vtkSphereSource()
sphere_closest.SetCenter(closest)
sphere_closest.SetRadius(0.12)
sphere_closest.SetPhiResolution(16)
sphere_closest.SetThetaResolution(16)

closest_mapper = vtkPolyDataMapper()
closest_mapper.SetInputConnection(sphere_closest.GetOutputPort())

closest_actor = vtkActor()
closest_actor.SetMapper(closest_mapper)
closest_actor.GetProperty().SetColor(lime_green_rgb)

# Source: spheres at the line segment endpoints (blue)
sphere_lp0 = vtkSphereSource()
sphere_lp0.SetCenter(line_p0)
sphere_lp0.SetRadius(0.10)
sphere_lp0.SetPhiResolution(16)
sphere_lp0.SetThetaResolution(16)

lp0_mapper = vtkPolyDataMapper()
lp0_mapper.SetInputConnection(sphere_lp0.GetOutputPort())

lp0_actor = vtkActor()
lp0_actor.SetMapper(lp0_mapper)
lp0_actor.GetProperty().SetColor(steel_blue_rgb)

sphere_lp1 = vtkSphereSource()
sphere_lp1.SetCenter(line_p1)
sphere_lp1.SetRadius(0.10)
sphere_lp1.SetPhiResolution(16)
sphere_lp1.SetThetaResolution(16)

lp1_mapper = vtkPolyDataMapper()
lp1_mapper.SetInputConnection(sphere_lp1.GetOutputPort())

lp1_actor = vtkActor()
lp1_actor.SetMapper(lp1_mapper)
lp1_actor.GetProperty().SetColor(steel_blue_rgb)

# Line: the line segment
seg_points = vtkPoints()
seg_points.InsertNextPoint(line_p0)
seg_points.InsertNextPoint(line_p1)

seg_cells = vtkCellArray()
seg_cells.InsertNextCell(2)
seg_cells.InsertCellPoint(0)
seg_cells.InsertCellPoint(1)

seg_poly = vtkPolyData()
seg_poly.SetPoints(seg_points)
seg_poly.SetLines(seg_cells)

seg_mapper = vtkPolyDataMapper()
seg_mapper.SetInputData(seg_poly)

seg_actor = vtkActor()
seg_actor.SetMapper(seg_mapper)
seg_actor.GetProperty().SetColor(steel_blue_rgb)
seg_actor.GetProperty().SetLineWidth(3.0)

# Line: perpendicular from query point to closest point
perp_points = vtkPoints()
perp_points.InsertNextPoint(query_point)
perp_points.InsertNextPoint(closest)

perp_cells = vtkCellArray()
perp_cells.InsertNextCell(2)
perp_cells.InsertCellPoint(0)
perp_cells.InsertCellPoint(1)

perp_poly = vtkPolyData()
perp_poly.SetPoints(perp_points)
perp_poly.SetLines(perp_cells)

perp_mapper = vtkPolyDataMapper()
perp_mapper.SetInputData(perp_poly)

perp_actor = vtkActor()
perp_actor.SetMapper(perp_mapper)
perp_actor.GetProperty().SetColor(yellow_rgb)
perp_actor.GetProperty().SetLineWidth(2.0)

# Label: distance
dist_label = vtkVectorText()
dist_label.SetText(f"d = {dist:.2f}")

dist_label_mapper = vtkPolyDataMapper()
dist_label_mapper.SetInputConnection(dist_label.GetOutputPort())

dist_label_actor = vtkActor()
dist_label_actor.SetMapper(dist_label_mapper)
dist_label_actor.SetScale(0.2, 0.2, 0.2)
mid = ((query_point[0] + closest[0]) / 2.0 + 0.15,
       (query_point[1] + closest[1]) / 2.0 + 0.1,
       0.0)
dist_label_actor.SetPosition(mid)
dist_label_actor.GetProperty().SetColor(yellow_rgb)

# Label: query point
q_label = vtkVectorText()
q_label.SetText(f"Q ({query_point[0]:.0f},{query_point[1]:.0f},{query_point[2]:.0f})")

q_label_mapper = vtkPolyDataMapper()
q_label_mapper.SetInputConnection(q_label.GetOutputPort())

q_label_actor = vtkActor()
q_label_actor.SetMapper(q_label_mapper)
q_label_actor.SetScale(0.18, 0.18, 0.18)
q_label_actor.SetPosition(query_point[0] + 0.2, query_point[1] + 0.15, 0.0)
q_label_actor.GetProperty().SetColor(tomato_rgb)

# Label: closest point
c_label = vtkVectorText()
c_label.SetText(f"C ({closest[0]:.1f},{closest[1]:.1f},{closest[2]:.1f})")

c_label_mapper = vtkPolyDataMapper()
c_label_mapper.SetInputConnection(c_label.GetOutputPort())

c_label_actor = vtkActor()
c_label_actor.SetMapper(c_label_mapper)
c_label_actor.SetScale(0.18, 0.18, 0.18)
c_label_actor.SetPosition(closest[0] - 0.3, closest[1] - 0.4, 0.0)
c_label_actor.GetProperty().SetColor(lime_green_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(query_actor)
renderer.AddActor(closest_actor)
renderer.AddActor(lp0_actor)
renderer.AddActor(lp1_actor)
renderer.AddActor(seg_actor)
renderer.AddActor(perp_actor)
renderer.AddActor(dist_label_actor)
renderer.AddActor(q_label_actor)
renderer.AddActor(c_label_actor)
renderer.SetBackground(dark_slate_gray_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.3)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClosestPointOnLine")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
