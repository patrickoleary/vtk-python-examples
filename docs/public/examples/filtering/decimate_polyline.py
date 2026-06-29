#!/usr/bin/env python

# Decimate polylines using distance, angle, and custom field strategies,
# shown in a 2x2 grid of viewports.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkDecimatePolylineFilter,
    vtkDecimatePolylineAngleStrategy,
    vtkDecimatePolylineCustomFieldStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

number_of_points_in_circle = 100
arc_pts = int(0.75 * number_of_points_in_circle)

# --- Top-left viewport: default distance strategy ---

points0 = vtkPoints()
points0.SetDataType(5)  # VTK_FLOAT
field_array_0 = vtkDoubleArray()
field_array_0.SetName("__custom__field__")
field_array_0.SetNumberOfComponents(2)
line_ids_0 = vtkIdList()
line_ids_0.SetNumberOfIds(int(1.75 * number_of_points_in_circle) + 1)
counter0 = 0
for i in range(number_of_points_in_circle):
    angle = 2.0 * math.pi * i / number_of_points_in_circle
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points0.InsertPoint(i, cos_a, sin_a, 0.0)
    field_array_0.InsertTuple2(i, cos_a, sin_a)
    line_ids_0.SetId(i, counter0)
    counter0 += 1
line_ids_0.SetId(number_of_points_in_circle, 0)
for i in range(arc_pts):
    idx = i + number_of_points_in_circle
    angle = 1.5 * math.pi * i / arc_pts
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points0.InsertPoint(idx, cos_a, sin_a, 1.0)
    field_array_0.InsertTuple2(idx, cos_a, sin_a)
    line_ids_0.SetId(idx + 1, counter0)
    counter0 += 1
lines0 = vtkCellArray()
ids0a = [line_ids_0.GetId(j) for j in range(number_of_points_in_circle + 1)]
lines0.InsertNextCell(number_of_points_in_circle + 1, ids0a)
ids0b = [line_ids_0.GetId(number_of_points_in_circle + 1 + j) for j in range(arc_pts)]
lines0.InsertNextCell(arc_pts, ids0b)
cell_doubles_0 = vtkDoubleArray()
cell_doubles_0.SetName("cellDoubles")
cell_doubles_0.InsertNextValue(1.0)
cell_doubles_0.InsertNextValue(2.0)
circles0 = vtkPolyData()
circles0.SetPoints(points0)
circles0.SetLines(lines0)
circles0.GetCellData().AddArray(cell_doubles_0)
circles0.GetPointData().AddArray(field_array_0)

circle_mapper_0 = vtkPolyDataMapper()
circle_mapper_0.SetInputData(circles0)
circle_actor_0 = vtkActor()
circle_actor_0.SetMapper(circle_mapper_0)

decimate_filter_0 = vtkDecimatePolylineFilter()
decimate_filter_0.SetInputData(circles0)
decimate_filter_0.SetTargetReduction(0.9)
decimate_filter_0.Update()
decimated_mapper_0 = vtkPolyDataMapper()
decimated_mapper_0.SetInputConnection(decimate_filter_0.GetOutputPort())
decimated_actor_0 = vtkActor()
decimated_actor_0.SetMapper(decimated_mapper_0)
decimated_actor_0.GetProperty().SetColor(1.0, 0.0, 0.0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_0.AddActor(circle_actor_0)
renderer_0.AddActor(decimated_actor_0)

# --- Top-right viewport: angle strategy ---

points1 = vtkPoints()
points1.SetDataType(5)
field_array_1 = vtkDoubleArray()
field_array_1.SetName("__custom__field__")
field_array_1.SetNumberOfComponents(2)
line_ids_1 = vtkIdList()
line_ids_1.SetNumberOfIds(int(1.75 * number_of_points_in_circle) + 1)
counter1 = 0
for i in range(number_of_points_in_circle):
    angle = 2.0 * math.pi * i / number_of_points_in_circle
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points1.InsertPoint(i, cos_a, sin_a, 0.0)
    field_array_1.InsertTuple2(i, cos_a, sin_a)
    line_ids_1.SetId(i, counter1)
    counter1 += 1
line_ids_1.SetId(number_of_points_in_circle, 0)
for i in range(arc_pts):
    idx = i + number_of_points_in_circle
    angle = 1.5 * math.pi * i / arc_pts
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points1.InsertPoint(idx, cos_a, sin_a, 1.0)
    field_array_1.InsertTuple2(idx, cos_a, sin_a)
    line_ids_1.SetId(idx + 1, counter1)
    counter1 += 1
lines1 = vtkCellArray()
ids1a = [line_ids_1.GetId(j) for j in range(number_of_points_in_circle + 1)]
lines1.InsertNextCell(number_of_points_in_circle + 1, ids1a)
ids1b = [line_ids_1.GetId(number_of_points_in_circle + 1 + j) for j in range(arc_pts)]
lines1.InsertNextCell(arc_pts, ids1b)
cell_doubles_1 = vtkDoubleArray()
cell_doubles_1.SetName("cellDoubles")
cell_doubles_1.InsertNextValue(1.0)
cell_doubles_1.InsertNextValue(2.0)
circles1 = vtkPolyData()
circles1.SetPoints(points1)
circles1.SetLines(lines1)
circles1.GetCellData().AddArray(cell_doubles_1)
circles1.GetPointData().AddArray(field_array_1)

circle_mapper_1 = vtkPolyDataMapper()
circle_mapper_1.SetInputData(circles1)
circle_actor_1 = vtkActor()
circle_actor_1.SetMapper(circle_mapper_1)

angle_strategy = vtkDecimatePolylineAngleStrategy()
decimate_filter_1 = vtkDecimatePolylineFilter()
decimate_filter_1.SetDecimationStrategy(angle_strategy)
decimate_filter_1.SetInputData(circles1)
decimate_filter_1.SetTargetReduction(0.9)
decimate_filter_1.Update()
decimated_mapper_1 = vtkPolyDataMapper()
decimated_mapper_1.SetInputConnection(decimate_filter_1.GetOutputPort())
decimated_actor_1 = vtkActor()
decimated_actor_1.SetMapper(decimated_mapper_1)
decimated_actor_1.GetProperty().SetColor(1.0, 0.0, 0.0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_1.AddActor(circle_actor_1)
renderer_1.AddActor(decimated_actor_1)

# --- Bottom-left viewport: custom field strategy ---

points2 = vtkPoints()
points2.SetDataType(5)
field_array_2 = vtkDoubleArray()
field_array_2.SetName("__custom__field__")
field_array_2.SetNumberOfComponents(2)
line_ids_2 = vtkIdList()
line_ids_2.SetNumberOfIds(int(1.75 * number_of_points_in_circle) + 1)
counter2 = 0
for i in range(number_of_points_in_circle):
    angle = 2.0 * math.pi * i / number_of_points_in_circle
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points2.InsertPoint(i, cos_a, sin_a, 0.0)
    field_array_2.InsertTuple2(i, cos_a, sin_a)
    line_ids_2.SetId(i, counter2)
    counter2 += 1
line_ids_2.SetId(number_of_points_in_circle, 0)
for i in range(arc_pts):
    idx = i + number_of_points_in_circle
    angle = 1.5 * math.pi * i / arc_pts
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points2.InsertPoint(idx, cos_a, sin_a, 1.0)
    field_array_2.InsertTuple2(idx, cos_a, sin_a)
    line_ids_2.SetId(idx + 1, counter2)
    counter2 += 1
lines2 = vtkCellArray()
ids2a = [line_ids_2.GetId(j) for j in range(number_of_points_in_circle + 1)]
lines2.InsertNextCell(number_of_points_in_circle + 1, ids2a)
ids2b = [line_ids_2.GetId(number_of_points_in_circle + 1 + j) for j in range(arc_pts)]
lines2.InsertNextCell(arc_pts, ids2b)
cell_doubles_2 = vtkDoubleArray()
cell_doubles_2.SetName("cellDoubles")
cell_doubles_2.InsertNextValue(1.0)
cell_doubles_2.InsertNextValue(2.0)
circles2 = vtkPolyData()
circles2.SetPoints(points2)
circles2.SetLines(lines2)
circles2.GetCellData().AddArray(cell_doubles_2)
circles2.GetPointData().AddArray(field_array_2)

circle_mapper_2 = vtkPolyDataMapper()
circle_mapper_2.SetInputData(circles2)
circle_actor_2 = vtkActor()
circle_actor_2.SetMapper(circle_mapper_2)

field_strategy = vtkDecimatePolylineCustomFieldStrategy()
field_strategy.SetFieldName("__custom__field__")
decimate_filter_2 = vtkDecimatePolylineFilter()
decimate_filter_2.SetDecimationStrategy(field_strategy)
decimate_filter_2.SetInputData(circles2)
decimate_filter_2.SetTargetReduction(0.9)
decimate_filter_2.Update()
decimated_mapper_2 = vtkPolyDataMapper()
decimated_mapper_2.SetInputConnection(decimate_filter_2.GetOutputPort())
decimated_actor_2 = vtkActor()
decimated_actor_2.SetMapper(decimated_mapper_2)
decimated_actor_2.GetProperty().SetColor(1.0, 0.0, 0.0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_2.AddActor(circle_actor_2)
renderer_2.AddActor(decimated_actor_2)

# --- Bottom-right viewport: custom field strategy (second copy) ---

points3 = vtkPoints()
points3.SetDataType(5)
field_array_3 = vtkDoubleArray()
field_array_3.SetName("__custom__field__")
field_array_3.SetNumberOfComponents(2)
line_ids_3 = vtkIdList()
line_ids_3.SetNumberOfIds(int(1.75 * number_of_points_in_circle) + 1)
counter3 = 0
for i in range(number_of_points_in_circle):
    angle = 2.0 * math.pi * i / number_of_points_in_circle
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points3.InsertPoint(i, cos_a, sin_a, 0.0)
    field_array_3.InsertTuple2(i, cos_a, sin_a)
    line_ids_3.SetId(i, counter3)
    counter3 += 1
line_ids_3.SetId(number_of_points_in_circle, 0)
for i in range(arc_pts):
    idx = i + number_of_points_in_circle
    angle = 1.5 * math.pi * i / arc_pts
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)
    points3.InsertPoint(idx, cos_a, sin_a, 1.0)
    field_array_3.InsertTuple2(idx, cos_a, sin_a)
    line_ids_3.SetId(idx + 1, counter3)
    counter3 += 1
lines3 = vtkCellArray()
ids3a = [line_ids_3.GetId(j) for j in range(number_of_points_in_circle + 1)]
lines3.InsertNextCell(number_of_points_in_circle + 1, ids3a)
ids3b = [line_ids_3.GetId(number_of_points_in_circle + 1 + j) for j in range(arc_pts)]
lines3.InsertNextCell(arc_pts, ids3b)
cell_doubles_3 = vtkDoubleArray()
cell_doubles_3.SetName("cellDoubles")
cell_doubles_3.InsertNextValue(1.0)
cell_doubles_3.InsertNextValue(2.0)
circles3 = vtkPolyData()
circles3.SetPoints(points3)
circles3.SetLines(lines3)
circles3.GetCellData().AddArray(cell_doubles_3)
circles3.GetPointData().AddArray(field_array_3)

circle_mapper_3 = vtkPolyDataMapper()
circle_mapper_3.SetInputData(circles3)
circle_actor_3 = vtkActor()
circle_actor_3.SetMapper(circle_mapper_3)

field_strategy_2 = vtkDecimatePolylineCustomFieldStrategy()
field_strategy_2.SetFieldName("__custom__field__")
decimate_filter_3 = vtkDecimatePolylineFilter()
decimate_filter_3.SetDecimationStrategy(field_strategy_2)
decimate_filter_3.SetInputData(circles3)
decimate_filter_3.SetTargetReduction(0.9)
decimate_filter_3.Update()
decimated_mapper_3 = vtkPolyDataMapper()
decimated_mapper_3.SetInputConnection(decimate_filter_3.GetOutputPort())
decimated_actor_3 = vtkActor()
decimated_actor_3.SetMapper(decimated_mapper_3)
decimated_actor_3.GetProperty().SetColor(1.0, 0.0, 0.0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_3.AddActor(circle_actor_3)
renderer_3.AddActor(decimated_actor_3)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("decimate polyline")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
