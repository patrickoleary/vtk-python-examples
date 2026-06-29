#!/usr/bin/env python
# Demonstrate Lagrange wedge interpolation, intersection, and clipping for orders 1-7.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import reference, vtkDoubleArray, vtkMinimalStandardRandomSequence, vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLagrangeWedge,
    vtkPolyData,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data generation: compute intersection and clip results for each order.
center = [0.25, 0.25, 0.5]

# Order 1 (6 points).
cell_order_1 = vtkLagrangeWedge()
cell_order_1.GetPointIds().SetNumberOfIds(6)
cell_order_1.GetPoints().SetNumberOfPoints(6)
cell_order_1.SetOrder(1, 1, 1, 6)
cell_order_1.Initialize()
coords_1 = cell_order_1.GetParametricCoords()
for i in range(6):
    cell_order_1.GetPointIds().SetId(i, i)
    cell_order_1.GetPoints().SetPoint(i, coords_1[3 * i], coords_1[3 * i + 1], coords_1[3 * i + 2])

sequence_1 = vtkMinimalStandardRandomSequence()
sequence_1.SetSeed(1)
hit_points_1 = vtkPoints()
hit_verts_1 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_1.GetValue()
        sequence_1.Next()
        phi = math.pi * sequence_1.GetValue()
        sequence_1.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_1.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_1.InsertNextPoint(x)
        hit_verts_1.InsertNextCell(1, [pid])

hit_pd_1 = vtkPolyData()
hit_pd_1.SetPoints(hit_points_1)
hit_pd_1.SetVerts(hit_verts_1)

ug_1 = vtkUnstructuredGrid()
ug_1.SetPoints(cell_order_1.GetPoints())
cell_array_1 = vtkCellArray()
cell_array_1.InsertNextCell(cell_order_1)
ug_1.SetCells(cell_order_1.GetCellType(), cell_array_1)
radiant_1 = vtkDoubleArray()
radiant_1.SetName("Distance from Origin")
radiant_1.SetNumberOfTuples(6)
max_dist_1 = 0.0
for i in range(6):
    xyz = cell_order_1.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_1.SetValue(i, dist)
    max_dist_1 = max(dist, max_dist_1)
ug_1.GetPointData().AddArray(radiant_1)
ug_1.GetPointData().SetScalars(radiant_1)

clip_1 = vtkClipDataSet()
clip_1.SetValue(max_dist_1 * 0.5)
clip_1.SetInputData(ug_1)
surface_filter_1 = vtkDataSetSurfaceFilter()
surface_filter_1.SetInputConnection(clip_1.GetOutputPort())
surface_filter_1.Update()
clip_pd_1 = vtkPolyData()
clip_pd_1.DeepCopy(surface_filter_1.GetOutput())

# Order 2 (18 points).
cell_order_2 = vtkLagrangeWedge()
cell_order_2.GetPointIds().SetNumberOfIds(18)
cell_order_2.GetPoints().SetNumberOfPoints(18)
cell_order_2.SetOrder(2, 2, 2, 18)
cell_order_2.Initialize()
coords_2 = cell_order_2.GetParametricCoords()
for i in range(18):
    cell_order_2.GetPointIds().SetId(i, i)
    cell_order_2.GetPoints().SetPoint(i, coords_2[3 * i], coords_2[3 * i + 1], coords_2[3 * i + 2])

sequence_2 = vtkMinimalStandardRandomSequence()
sequence_2.SetSeed(1)
hit_points_2 = vtkPoints()
hit_verts_2 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_2.GetValue()
        sequence_2.Next()
        phi = math.pi * sequence_2.GetValue()
        sequence_2.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_2.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_2.InsertNextPoint(x)
        hit_verts_2.InsertNextCell(1, [pid])

hit_pd_2 = vtkPolyData()
hit_pd_2.SetPoints(hit_points_2)
hit_pd_2.SetVerts(hit_verts_2)

ug_2 = vtkUnstructuredGrid()
ug_2.SetPoints(cell_order_2.GetPoints())
cell_array_2 = vtkCellArray()
cell_array_2.InsertNextCell(cell_order_2)
ug_2.SetCells(cell_order_2.GetCellType(), cell_array_2)
radiant_2 = vtkDoubleArray()
radiant_2.SetName("Distance from Origin")
radiant_2.SetNumberOfTuples(18)
max_dist_2 = 0.0
for i in range(18):
    xyz = cell_order_2.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_2.SetValue(i, dist)
    max_dist_2 = max(dist, max_dist_2)
ug_2.GetPointData().AddArray(radiant_2)
ug_2.GetPointData().SetScalars(radiant_2)

clip_2 = vtkClipDataSet()
clip_2.SetValue(max_dist_2 * 0.5)
clip_2.SetInputData(ug_2)
surface_filter_2 = vtkDataSetSurfaceFilter()
surface_filter_2.SetInputConnection(clip_2.GetOutputPort())
surface_filter_2.Update()
clip_pd_2 = vtkPolyData()
clip_pd_2.DeepCopy(surface_filter_2.GetOutput())

# Order 3 (40 points).
cell_order_3 = vtkLagrangeWedge()
cell_order_3.GetPointIds().SetNumberOfIds(40)
cell_order_3.GetPoints().SetNumberOfPoints(40)
cell_order_3.SetOrder(3, 3, 3, 40)
cell_order_3.Initialize()
coords_3 = cell_order_3.GetParametricCoords()
for i in range(40):
    cell_order_3.GetPointIds().SetId(i, i)
    cell_order_3.GetPoints().SetPoint(i, coords_3[3 * i], coords_3[3 * i + 1], coords_3[3 * i + 2])

sequence_3 = vtkMinimalStandardRandomSequence()
sequence_3.SetSeed(1)
hit_points_3 = vtkPoints()
hit_verts_3 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_3.GetValue()
        sequence_3.Next()
        phi = math.pi * sequence_3.GetValue()
        sequence_3.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_3.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_3.InsertNextPoint(x)
        hit_verts_3.InsertNextCell(1, [pid])

hit_pd_3 = vtkPolyData()
hit_pd_3.SetPoints(hit_points_3)
hit_pd_3.SetVerts(hit_verts_3)

ug_3 = vtkUnstructuredGrid()
ug_3.SetPoints(cell_order_3.GetPoints())
cell_array_3 = vtkCellArray()
cell_array_3.InsertNextCell(cell_order_3)
ug_3.SetCells(cell_order_3.GetCellType(), cell_array_3)
radiant_3 = vtkDoubleArray()
radiant_3.SetName("Distance from Origin")
radiant_3.SetNumberOfTuples(40)
max_dist_3 = 0.0
for i in range(40):
    xyz = cell_order_3.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_3.SetValue(i, dist)
    max_dist_3 = max(dist, max_dist_3)
ug_3.GetPointData().AddArray(radiant_3)
ug_3.GetPointData().SetScalars(radiant_3)

clip_3 = vtkClipDataSet()
clip_3.SetValue(max_dist_3 * 0.5)
clip_3.SetInputData(ug_3)
surface_filter_3 = vtkDataSetSurfaceFilter()
surface_filter_3.SetInputConnection(clip_3.GetOutputPort())
surface_filter_3.Update()
clip_pd_3 = vtkPolyData()
clip_pd_3.DeepCopy(surface_filter_3.GetOutput())

# Order 4 (75 points).
cell_order_4 = vtkLagrangeWedge()
cell_order_4.GetPointIds().SetNumberOfIds(75)
cell_order_4.GetPoints().SetNumberOfPoints(75)
cell_order_4.SetOrder(4, 4, 4, 75)
cell_order_4.Initialize()
coords_4 = cell_order_4.GetParametricCoords()
for i in range(75):
    cell_order_4.GetPointIds().SetId(i, i)
    cell_order_4.GetPoints().SetPoint(i, coords_4[3 * i], coords_4[3 * i + 1], coords_4[3 * i + 2])

sequence_4 = vtkMinimalStandardRandomSequence()
sequence_4.SetSeed(1)
hit_points_4 = vtkPoints()
hit_verts_4 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_4.GetValue()
        sequence_4.Next()
        phi = math.pi * sequence_4.GetValue()
        sequence_4.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_4.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_4.InsertNextPoint(x)
        hit_verts_4.InsertNextCell(1, [pid])

hit_pd_4 = vtkPolyData()
hit_pd_4.SetPoints(hit_points_4)
hit_pd_4.SetVerts(hit_verts_4)

ug_4 = vtkUnstructuredGrid()
ug_4.SetPoints(cell_order_4.GetPoints())
cell_array_4 = vtkCellArray()
cell_array_4.InsertNextCell(cell_order_4)
ug_4.SetCells(cell_order_4.GetCellType(), cell_array_4)
radiant_4 = vtkDoubleArray()
radiant_4.SetName("Distance from Origin")
radiant_4.SetNumberOfTuples(75)
max_dist_4 = 0.0
for i in range(75):
    xyz = cell_order_4.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_4.SetValue(i, dist)
    max_dist_4 = max(dist, max_dist_4)
ug_4.GetPointData().AddArray(radiant_4)
ug_4.GetPointData().SetScalars(radiant_4)

clip_4 = vtkClipDataSet()
clip_4.SetValue(max_dist_4 * 0.5)
clip_4.SetInputData(ug_4)
surface_filter_4 = vtkDataSetSurfaceFilter()
surface_filter_4.SetInputConnection(clip_4.GetOutputPort())
surface_filter_4.Update()
clip_pd_4 = vtkPolyData()
clip_pd_4.DeepCopy(surface_filter_4.GetOutput())

# Order 5 (126 points).
cell_order_5 = vtkLagrangeWedge()
cell_order_5.GetPointIds().SetNumberOfIds(126)
cell_order_5.GetPoints().SetNumberOfPoints(126)
cell_order_5.SetOrder(5, 5, 5, 126)
cell_order_5.Initialize()
coords_5 = cell_order_5.GetParametricCoords()
for i in range(126):
    cell_order_5.GetPointIds().SetId(i, i)
    cell_order_5.GetPoints().SetPoint(i, coords_5[3 * i], coords_5[3 * i + 1], coords_5[3 * i + 2])

sequence_5 = vtkMinimalStandardRandomSequence()
sequence_5.SetSeed(1)
hit_points_5 = vtkPoints()
hit_verts_5 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_5.GetValue()
        sequence_5.Next()
        phi = math.pi * sequence_5.GetValue()
        sequence_5.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_5.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_5.InsertNextPoint(x)
        hit_verts_5.InsertNextCell(1, [pid])

hit_pd_5 = vtkPolyData()
hit_pd_5.SetPoints(hit_points_5)
hit_pd_5.SetVerts(hit_verts_5)

ug_5 = vtkUnstructuredGrid()
ug_5.SetPoints(cell_order_5.GetPoints())
cell_array_5 = vtkCellArray()
cell_array_5.InsertNextCell(cell_order_5)
ug_5.SetCells(cell_order_5.GetCellType(), cell_array_5)
radiant_5 = vtkDoubleArray()
radiant_5.SetName("Distance from Origin")
radiant_5.SetNumberOfTuples(126)
max_dist_5 = 0.0
for i in range(126):
    xyz = cell_order_5.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_5.SetValue(i, dist)
    max_dist_5 = max(dist, max_dist_5)
ug_5.GetPointData().AddArray(radiant_5)
ug_5.GetPointData().SetScalars(radiant_5)

clip_5 = vtkClipDataSet()
clip_5.SetValue(max_dist_5 * 0.5)
clip_5.SetInputData(ug_5)
surface_filter_5 = vtkDataSetSurfaceFilter()
surface_filter_5.SetInputConnection(clip_5.GetOutputPort())
surface_filter_5.Update()
clip_pd_5 = vtkPolyData()
clip_pd_5.DeepCopy(surface_filter_5.GetOutput())

# Order 6 (196 points).
cell_order_6 = vtkLagrangeWedge()
cell_order_6.GetPointIds().SetNumberOfIds(196)
cell_order_6.GetPoints().SetNumberOfPoints(196)
cell_order_6.SetOrder(6, 6, 6, 196)
cell_order_6.Initialize()
coords_6 = cell_order_6.GetParametricCoords()
for i in range(196):
    cell_order_6.GetPointIds().SetId(i, i)
    cell_order_6.GetPoints().SetPoint(i, coords_6[3 * i], coords_6[3 * i + 1], coords_6[3 * i + 2])

sequence_6 = vtkMinimalStandardRandomSequence()
sequence_6.SetSeed(1)
hit_points_6 = vtkPoints()
hit_verts_6 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_6.GetValue()
        sequence_6.Next()
        phi = math.pi * sequence_6.GetValue()
        sequence_6.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_6.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_6.InsertNextPoint(x)
        hit_verts_6.InsertNextCell(1, [pid])

hit_pd_6 = vtkPolyData()
hit_pd_6.SetPoints(hit_points_6)
hit_pd_6.SetVerts(hit_verts_6)

ug_6 = vtkUnstructuredGrid()
ug_6.SetPoints(cell_order_6.GetPoints())
cell_array_6 = vtkCellArray()
cell_array_6.InsertNextCell(cell_order_6)
ug_6.SetCells(cell_order_6.GetCellType(), cell_array_6)
radiant_6 = vtkDoubleArray()
radiant_6.SetName("Distance from Origin")
radiant_6.SetNumberOfTuples(196)
max_dist_6 = 0.0
for i in range(196):
    xyz = cell_order_6.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_6.SetValue(i, dist)
    max_dist_6 = max(dist, max_dist_6)
ug_6.GetPointData().AddArray(radiant_6)
ug_6.GetPointData().SetScalars(radiant_6)

clip_6 = vtkClipDataSet()
clip_6.SetValue(max_dist_6 * 0.5)
clip_6.SetInputData(ug_6)
surface_filter_6 = vtkDataSetSurfaceFilter()
surface_filter_6.SetInputConnection(clip_6.GetOutputPort())
surface_filter_6.Update()
clip_pd_6 = vtkPolyData()
clip_pd_6.DeepCopy(surface_filter_6.GetOutput())

# Order 7 (288 points).
cell_order_7 = vtkLagrangeWedge()
cell_order_7.GetPointIds().SetNumberOfIds(288)
cell_order_7.GetPoints().SetNumberOfPoints(288)
cell_order_7.SetOrder(7, 7, 7, 288)
cell_order_7.Initialize()
coords_7 = cell_order_7.GetParametricCoords()
for i in range(288):
    cell_order_7.GetPointIds().SetId(i, i)
    cell_order_7.GetPoints().SetPoint(i, coords_7[3 * i], coords_7[3 * i + 1], coords_7[3 * i + 2])

sequence_7 = vtkMinimalStandardRandomSequence()
sequence_7.SetSeed(1)
hit_points_7 = vtkPoints()
hit_verts_7 = vtkCellArray()
for i in range(500):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence_7.GetValue()
        sequence_7.Next()
        phi = math.pi * sequence_7.GetValue()
        sequence_7.Next()
        pt[0] = 1.5 * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = 1.5 * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = 1.5 * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = cell_order_7.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_7.InsertNextPoint(x)
        hit_verts_7.InsertNextCell(1, [pid])

hit_pd_7 = vtkPolyData()
hit_pd_7.SetPoints(hit_points_7)
hit_pd_7.SetVerts(hit_verts_7)

ug_7 = vtkUnstructuredGrid()
ug_7.SetPoints(cell_order_7.GetPoints())
cell_array_7 = vtkCellArray()
cell_array_7.InsertNextCell(cell_order_7)
ug_7.SetCells(cell_order_7.GetCellType(), cell_array_7)
radiant_7 = vtkDoubleArray()
radiant_7.SetName("Distance from Origin")
radiant_7.SetNumberOfTuples(288)
max_dist_7 = 0.0
for i in range(288):
    xyz = cell_order_7.GetPoints().GetPoint(i)
    dist = math.sqrt(xyz[0] ** 2 + xyz[1] ** 2 + xyz[2] ** 2)
    radiant_7.SetValue(i, dist)
    max_dist_7 = max(dist, max_dist_7)
ug_7.GetPointData().AddArray(radiant_7)
ug_7.GetPointData().SetScalars(radiant_7)

clip_7 = vtkClipDataSet()
clip_7.SetValue(max_dist_7 * 0.5)
clip_7.SetInputData(ug_7)
surface_filter_7 = vtkDataSetSurfaceFilter()
surface_filter_7.SetInputConnection(clip_7.GetOutputPort())
surface_filter_7.Update()
clip_pd_7 = vtkPolyData()
clip_pd_7.DeepCopy(surface_filter_7.GetOutput())

# Mappers, actors, renderers for each viewport.
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(hit_pd_1)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.25, 0.25)
renderer_0.AddActor(actor_0)
renderer_0.ResetCamera()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(clip_pd_1)
mapper_1.SetScalarRange(max_dist_1 * 0.5, max_dist_1)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.25, 0.0, 0.5, 0.25)
renderer_1.AddActor(actor_1)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputData(hit_pd_2)
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.5, 0.0, 0.75, 0.25)
renderer_2.AddActor(actor_2)
renderer_2.ResetCamera()

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputData(clip_pd_2)
mapper_3.SetScalarRange(max_dist_2 * 0.5, max_dist_2)
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.75, 0.0, 1.0, 0.25)
renderer_3.AddActor(actor_3)

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputData(hit_pd_3)
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.0, 0.25, 0.25, 0.5)
renderer_4.AddActor(actor_4)
renderer_4.ResetCamera()

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputData(clip_pd_3)
mapper_5.SetScalarRange(max_dist_3 * 0.5, max_dist_3)
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.25, 0.25, 0.5, 0.5)
renderer_5.AddActor(actor_5)

mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputData(hit_pd_4)
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)

renderer_6 = vtkRenderer()
renderer_6.SetViewport(0.5, 0.25, 0.75, 0.5)
renderer_6.AddActor(actor_6)
renderer_6.ResetCamera()

mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputData(clip_pd_4)
mapper_7.SetScalarRange(max_dist_4 * 0.5, max_dist_4)
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)

renderer_7 = vtkRenderer()
renderer_7.SetViewport(0.75, 0.25, 1.0, 0.5)
renderer_7.AddActor(actor_7)

mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputData(hit_pd_5)
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)

renderer_8 = vtkRenderer()
renderer_8.SetViewport(0.0, 0.5, 0.25, 0.75)
renderer_8.AddActor(actor_8)
renderer_8.ResetCamera()

mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputData(clip_pd_5)
mapper_9.SetScalarRange(max_dist_5 * 0.5, max_dist_5)
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)

renderer_9 = vtkRenderer()
renderer_9.SetViewport(0.25, 0.5, 0.5, 0.75)
renderer_9.AddActor(actor_9)

mapper_10 = vtkPolyDataMapper()
mapper_10.SetInputData(hit_pd_6)
actor_10 = vtkActor()
actor_10.SetMapper(mapper_10)

renderer_10 = vtkRenderer()
renderer_10.SetViewport(0.5, 0.5, 0.75, 0.75)
renderer_10.AddActor(actor_10)
renderer_10.ResetCamera()

mapper_11 = vtkPolyDataMapper()
mapper_11.SetInputData(clip_pd_6)
mapper_11.SetScalarRange(max_dist_6 * 0.5, max_dist_6)
actor_11 = vtkActor()
actor_11.SetMapper(mapper_11)

renderer_11 = vtkRenderer()
renderer_11.SetViewport(0.75, 0.5, 1.0, 0.75)
renderer_11.AddActor(actor_11)

mapper_12 = vtkPolyDataMapper()
mapper_12.SetInputData(hit_pd_7)
actor_12 = vtkActor()
actor_12.SetMapper(mapper_12)

renderer_12 = vtkRenderer()
renderer_12.SetViewport(0.0, 0.75, 0.25, 1.0)
renderer_12.AddActor(actor_12)
renderer_12.ResetCamera()

mapper_13 = vtkPolyDataMapper()
mapper_13.SetInputData(clip_pd_7)
mapper_13.SetScalarRange(max_dist_7 * 0.5, max_dist_7)
actor_13 = vtkActor()
actor_13.SetMapper(mapper_13)

renderer_13 = vtkRenderer()
renderer_13.SetViewport(0.25, 0.75, 0.5, 1.0)
renderer_13.AddActor(actor_13)

renderer_14 = vtkRenderer()
renderer_14.SetViewport(0.5, 0.75, 0.75, 1.0)
renderer_14.SetBackground(0, 0, 0)

renderer_15 = vtkRenderer()
renderer_15.SetViewport(0.75, 0.75, 1.0, 1.0)
renderer_15.SetBackground(0, 0, 0)

render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.AddRenderer(renderer_8)
render_window.AddRenderer(renderer_9)
render_window.AddRenderer(renderer_10)
render_window.AddRenderer(renderer_11)
render_window.AddRenderer(renderer_12)
render_window.AddRenderer(renderer_13)
render_window.AddRenderer(renderer_14)
render_window.AddRenderer(renderer_15)
render_window.SetWindowName("lagrange wedge")

# Scene: set camera for intersection viewports.
renderer_0.GetActiveCamera().SetPosition(2, 2, 2)
renderer_0.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_2.GetActiveCamera().SetPosition(2, 2, 2)
renderer_2.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_4.GetActiveCamera().SetPosition(2, 2, 2)
renderer_4.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_6.GetActiveCamera().SetPosition(2, 2, 2)
renderer_6.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_8.GetActiveCamera().SetPosition(2, 2, 2)
renderer_8.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_10.GetActiveCamera().SetPosition(2, 2, 2)
renderer_10.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_12.GetActiveCamera().SetPosition(2, 2, 2)
renderer_12.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])

# Scene: set camera for clip viewports.
renderer_1.GetActiveCamera().SetPosition(-2.0 * max_dist_1, -2.0 * max_dist_1, -2.0 * max_dist_1)
renderer_1.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_3.GetActiveCamera().SetPosition(-2.0 * max_dist_2, -2.0 * max_dist_2, -2.0 * max_dist_2)
renderer_3.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_5.GetActiveCamera().SetPosition(-2.0 * max_dist_3, -2.0 * max_dist_3, -2.0 * max_dist_3)
renderer_5.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_7.GetActiveCamera().SetPosition(-2.0 * max_dist_4, -2.0 * max_dist_4, -2.0 * max_dist_4)
renderer_7.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_9.GetActiveCamera().SetPosition(-2.0 * max_dist_5, -2.0 * max_dist_5, -2.0 * max_dist_5)
renderer_9.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_11.GetActiveCamera().SetPosition(-2.0 * max_dist_6, -2.0 * max_dist_6, -2.0 * max_dist_6)
renderer_11.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer_13.GetActiveCamera().SetPosition(-2.0 * max_dist_7, -2.0 * max_dist_7, -2.0 * max_dist_7)
renderer_13.GetActiveCamera().SetFocalPoint(0, 0, 0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
