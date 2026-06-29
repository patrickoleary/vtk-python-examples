#!/usr/bin/env python
# Demonstrate quadratic cell IntersectWithLine methods for various cell types.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import reference, vtkMinimalStandardRandomSequence, vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkBiQuadraticQuad,
    vtkBiQuadraticQuadraticHexahedron,
    vtkBiQuadraticQuadraticWedge,
    vtkBiQuadraticTriangle,
    vtkCellArray,
    vtkCubicLine,
    vtkPolyData,
    vtkQuadraticEdge,
    vtkQuadraticHexahedron,
    vtkQuadraticLinearQuad,
    vtkQuadraticLinearWedge,
    vtkQuadraticPyramid,
    vtkQuadraticQuad,
    vtkQuadraticTetra,
    vtkQuadraticTriangle,
    vtkQuadraticWedge,
    vtkTriQuadraticHexahedron,
    vtkTriQuadraticPyramid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

sequence = vtkMinimalStandardRandomSequence()
sequence.SetSeed(1)
n_test = 10000
radius = 1.5
center = [0.5, 0.25, 0.0]

# vtkQuadraticEdge
edge = vtkQuadraticEdge()
for i in range(edge.GetNumberOfPoints()):
    edge.GetPointIds().SetId(i, i)
edge.GetPoints().SetPoint(0, 0, 0, 0)
edge.GetPoints().SetPoint(1, 1, 0, 0)
edge.GetPoints().SetPoint(2, 0.5, 0.25, 0)

# vtkQuadraticTriangle
tri = vtkQuadraticTriangle()
for i in range(tri.GetNumberOfPoints()):
    tri.GetPointIds().SetId(i, i)
tri.GetPoints().SetPoint(0, 0, 0, 0)
tri.GetPoints().SetPoint(1, 1, 0, 0)
tri.GetPoints().SetPoint(2, 0.5, 0.8, 0)
tri.GetPoints().SetPoint(3, 0.5, 0.0, 0)
tri.GetPoints().SetPoint(4, 0.75, 0.4, 0)
tri.GetPoints().SetPoint(5, 0.25, 0.4, 0)
center = [0.5, 0.5, 0.0]

# vtkQuadraticQuad
quad = vtkQuadraticQuad()
for i in range(quad.GetNumberOfPoints()):
    quad.GetPointIds().SetId(i, i)
quad.GetPoints().SetPoint(0, 0.0, 0.0, 0.0)
quad.GetPoints().SetPoint(1, 1.0, 0.0, 0.0)
quad.GetPoints().SetPoint(2, 1.0, 1.0, 0.0)
quad.GetPoints().SetPoint(3, 0.0, 1.0, 0.0)
quad.GetPoints().SetPoint(4, 0.5, 0.0, 0.0)
quad.GetPoints().SetPoint(5, 1.0, 0.5, 0.0)
quad.GetPoints().SetPoint(6, 0.5, 1.0, 0.0)
quad.GetPoints().SetPoint(7, 0.0, 0.5, 0.0)

# vtkQuadraticTetra
tetra = vtkQuadraticTetra()
for i in range(tetra.GetNumberOfPoints()):
    tetra.GetPointIds().SetId(i, i)
tetra.GetPoints().SetPoint(0, 0.0, 0.0, 0.0)
tetra.GetPoints().SetPoint(1, 1.0, 0.0, 0.0)
tetra.GetPoints().SetPoint(2, 0.5, 0.8, 0.0)
tetra.GetPoints().SetPoint(3, 0.5, 0.4, 1.0)
tetra.GetPoints().SetPoint(4, 0.5, 0.0, 0.0)
tetra.GetPoints().SetPoint(5, 0.75, 0.4, 0.0)
tetra.GetPoints().SetPoint(6, 0.25, 0.4, 0.0)
tetra.GetPoints().SetPoint(7, 0.25, 0.2, 0.5)
tetra.GetPoints().SetPoint(8, 0.75, 0.2, 0.5)
tetra.GetPoints().SetPoint(9, 0.50, 0.6, 0.5)

# vtkQuadraticHexahedron
hex_cell = vtkQuadraticHexahedron()
for i in range(hex_cell.GetNumberOfPoints()):
    hex_cell.GetPointIds().SetId(i, i)
hex_cell.GetPoints().SetPoint(0, 0, 0, 0)
hex_cell.GetPoints().SetPoint(1, 1, 0, 0)
hex_cell.GetPoints().SetPoint(2, 1, 1, 0)
hex_cell.GetPoints().SetPoint(3, 0, 1, 0)
hex_cell.GetPoints().SetPoint(4, 0, 0, 1)
hex_cell.GetPoints().SetPoint(5, 1, 0, 1)
hex_cell.GetPoints().SetPoint(6, 1, 1, 1)
hex_cell.GetPoints().SetPoint(7, 0, 1, 1)
hex_cell.GetPoints().SetPoint(8, 0.5, 0, 0)
hex_cell.GetPoints().SetPoint(9, 1, 0.5, 0)
hex_cell.GetPoints().SetPoint(10, 0.5, 1, 0)
hex_cell.GetPoints().SetPoint(11, 0, 0.5, 0)
hex_cell.GetPoints().SetPoint(12, 0.5, 0, 1)
hex_cell.GetPoints().SetPoint(13, 1, 0.5, 1)
hex_cell.GetPoints().SetPoint(14, 0.5, 1, 1)
hex_cell.GetPoints().SetPoint(15, 0, 0.5, 1)
hex_cell.GetPoints().SetPoint(16, 0, 0, 0.5)
hex_cell.GetPoints().SetPoint(17, 1, 0, 0.5)
hex_cell.GetPoints().SetPoint(18, 1, 1, 0.5)
hex_cell.GetPoints().SetPoint(19, 0, 1, 0.5)

# vtkQuadraticWedge
wedge = vtkQuadraticWedge()
pcoords = wedge.GetParametricCoords()
for i in range(wedge.GetNumberOfPoints()):
    wedge.GetPointIds().SetId(i, i)
    wedge.GetPoints().SetPoint(i, pcoords[3 * i], pcoords[3 * i + 1], pcoords[3 * i + 2])

# vtkQuadraticPyramid
pyra = vtkQuadraticPyramid()
for i in range(pyra.GetNumberOfPoints()):
    pyra.GetPointIds().SetId(i, i)
pyra.GetPoints().SetPoint(0, 0, 0, 0)
pyra.GetPoints().SetPoint(1, 1, 0, 0)
pyra.GetPoints().SetPoint(2, 1, 1, 0)
pyra.GetPoints().SetPoint(3, 0, 1, 0)
pyra.GetPoints().SetPoint(4, 0, 0, 1)
pyra.GetPoints().SetPoint(5, 0.5, 0, 0)
pyra.GetPoints().SetPoint(6, 1, 0.5, 0)
pyra.GetPoints().SetPoint(7, 0.5, 1, 0)
pyra.GetPoints().SetPoint(8, 0, 0.5, 0)
pyra.GetPoints().SetPoint(9, 0, 0, 0.5)
pyra.GetPoints().SetPoint(10, 0.5, 0, 0.5)
pyra.GetPoints().SetPoint(11, 0.5, 0.5, 0.5)
pyra.GetPoints().SetPoint(12, 0, 0.5, 0.5)

# vtkQuadraticLinearQuad
quadlin = vtkQuadraticLinearQuad()
ql_pcoords = quadlin.GetParametricCoords()
for i in range(quadlin.GetNumberOfPoints()):
    quadlin.GetPointIds().SetId(i, i)
    quadlin.GetPoints().SetPoint(i, ql_pcoords[3 * i], ql_pcoords[3 * i + 1], ql_pcoords[3 * i + 2])

# vtkBiQuadraticQuad
biquad = vtkBiQuadraticQuad()
bq_pcoords = biquad.GetParametricCoords()
for i in range(biquad.GetNumberOfPoints()):
    biquad.GetPointIds().SetId(i, i)
    biquad.GetPoints().SetPoint(i, bq_pcoords[3 * i], bq_pcoords[3 * i + 1], bq_pcoords[3 * i + 2])

# vtkQuadraticLinearWedge
wedgelin = vtkQuadraticLinearWedge()
wl_pcoords = wedgelin.GetParametricCoords()
for i in range(wedgelin.GetNumberOfPoints()):
    wedgelin.GetPointIds().SetId(i, i)
    wedgelin.GetPoints().SetPoint(i, wl_pcoords[3 * i], wl_pcoords[3 * i + 1], wl_pcoords[3 * i + 2])

# vtkBiQuadraticQuadraticWedge
biwedge = vtkBiQuadraticQuadraticWedge()
bw_pcoords = biwedge.GetParametricCoords()
for i in range(biwedge.GetNumberOfPoints()):
    biwedge.GetPointIds().SetId(i, i)
    biwedge.GetPoints().SetPoint(i, bw_pcoords[3 * i], bw_pcoords[3 * i + 1], bw_pcoords[3 * i + 2])

# vtkBiQuadraticQuadraticHexahedron
bihex = vtkBiQuadraticQuadraticHexahedron()
bh_pcoords = bihex.GetParametricCoords()
for i in range(bihex.GetNumberOfPoints()):
    bihex.GetPointIds().SetId(i, i)
    bihex.GetPoints().SetPoint(i, bh_pcoords[3 * i], bh_pcoords[3 * i + 1], bh_pcoords[3 * i + 2])

# vtkTriQuadraticHexahedron
trihex = vtkTriQuadraticHexahedron()
th_pcoords = trihex.GetParametricCoords()
for i in range(trihex.GetNumberOfPoints()):
    trihex.GetPointIds().SetId(i, i)
    trihex.GetPoints().SetPoint(i, th_pcoords[3 * i], th_pcoords[3 * i + 1], th_pcoords[3 * i + 2])

# vtkTriQuadraticPyramid
tq_pyra = vtkTriQuadraticPyramid()
for i in range(tq_pyra.GetNumberOfPoints()):
    tq_pyra.GetPointIds().SetId(i, i)
tq_pyra.GetPoints().SetPoint(0, 0, 0, 0)
tq_pyra.GetPoints().SetPoint(1, 1, 0, 0)
tq_pyra.GetPoints().SetPoint(2, 1, 1, 0)
tq_pyra.GetPoints().SetPoint(3, 0, 1, 0)
tq_pyra.GetPoints().SetPoint(4, 0, 0, 1)
tq_pyra.GetPoints().SetPoint(5, 0.5, 0, 0)
tq_pyra.GetPoints().SetPoint(6, 1, 0.5, 0)
tq_pyra.GetPoints().SetPoint(7, 0.5, 1, 0)
tq_pyra.GetPoints().SetPoint(8, 0, 0.5, 0)
tq_pyra.GetPoints().SetPoint(9, 0, 0, 0.5)
tq_pyra.GetPoints().SetPoint(10, 0.5, 0, 0.5)
tq_pyra.GetPoints().SetPoint(11, 0.5, 0.5, 0.5)
tq_pyra.GetPoints().SetPoint(12, 0, 0.5, 0.5)
tq_pyra.GetPoints().SetPoint(13, 0.5, 0.5, 0)
tq_pyra.GetPoints().SetPoint(14, 1.0 / 3.0, 0, 1.0 / 3.0)
tq_pyra.GetPoints().SetPoint(15, 2.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0)
tq_pyra.GetPoints().SetPoint(16, 1.0 / 3.0, 2.0 / 3.0, 1.0 / 3.0)
tq_pyra.GetPoints().SetPoint(17, 0, 1.0 / 3.0, 1.0 / 3.0)
tq_pyra.GetPoints().SetPoint(18, 0.4, 0.4, 0.2)

# vtkBiQuadraticTriangle
bitri = vtkBiQuadraticTriangle()
for i in range(bitri.GetNumberOfPoints()):
    bitri.GetPointIds().SetId(i, i)
bitri.GetPoints().SetPoint(0, 0, 0, 0)
bitri.GetPoints().SetPoint(1, 1, 0, 0)
bitri.GetPoints().SetPoint(2, 0.5, 0.8, 0)
bitri.GetPoints().SetPoint(3, 0.5, 0.0, 0)
bitri.GetPoints().SetPoint(4, 0.75, 0.4, 0)
bitri.GetPoints().SetPoint(5, 0.25, 0.4, 0)
bitri.GetPoints().SetPoint(6, 0.45, 0.24, 0)

# vtkCubicLine
culine = vtkCubicLine()
for i in range(culine.GetNumberOfPoints()):
    culine.GetPointIds().SetId(i, i)
culine.GetPoints().SetPoint(0, 0, 0, 0)
culine.GetPoints().SetPoint(1, 1, 0, 0)
culine.GetPoints().SetPoint(2, 1.0 / 3.0, -0.1, 0)
culine.GetPoints().SetPoint(3, 1.0 / 3.0, 0.1, 0)

# Cell test list: (cell, three_dimensional).
cell_tests = [
    (edge, False),
    (tri, True),
    (quad, True),
    (tetra, True),
    (hex_cell, True),
    (wedge, True),
    (pyra, True),
    (quadlin, True),
    (biquad, True),
    (wedgelin, True),
    (biwedge, True),
    (bihex, True),
    (trihex, True),
    (tq_pyra, True),
    (bitri, True),
    (culine, False),
]

# Perform intersection tests for each cell.
# 0: edge (2D)
hit_points_0 = vtkPoints()
hit_verts_0 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) + center[0]
        pt[1] = radius * math.sin(theta) + center[1]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = edge.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_0.InsertNextPoint(x)
        hit_verts_0.InsertNextCell(1, [pid])
pd_0 = vtkPolyData()
pd_0.SetPoints(hit_points_0)
pd_0.SetVerts(hit_verts_0)
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputData(pd_0)
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# 1: tri (3D)
hit_points_1 = vtkPoints()
hit_verts_1 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = tri.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_1.InsertNextPoint(x)
        hit_verts_1.InsertNextCell(1, [pid])
pd_1 = vtkPolyData()
pd_1.SetPoints(hit_points_1)
pd_1.SetVerts(hit_verts_1)
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputData(pd_1)
actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# 2: quad (3D)
hit_points_2 = vtkPoints()
hit_verts_2 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = quad.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_2.InsertNextPoint(x)
        hit_verts_2.InsertNextCell(1, [pid])
pd_2 = vtkPolyData()
pd_2.SetPoints(hit_points_2)
pd_2.SetVerts(hit_verts_2)
mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputData(pd_2)
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# 3: tetra (3D)
hit_points_3 = vtkPoints()
hit_verts_3 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = tetra.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_3.InsertNextPoint(x)
        hit_verts_3.InsertNextCell(1, [pid])
pd_3 = vtkPolyData()
pd_3.SetPoints(hit_points_3)
pd_3.SetVerts(hit_verts_3)
mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputData(pd_3)
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# 4: hex_cell (3D)
hit_points_4 = vtkPoints()
hit_verts_4 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = hex_cell.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_4.InsertNextPoint(x)
        hit_verts_4.InsertNextCell(1, [pid])
pd_4 = vtkPolyData()
pd_4.SetPoints(hit_points_4)
pd_4.SetVerts(hit_verts_4)
mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputData(pd_4)
actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)

# 5: wedge (3D)
hit_points_5 = vtkPoints()
hit_verts_5 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = wedge.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_5.InsertNextPoint(x)
        hit_verts_5.InsertNextCell(1, [pid])
pd_5 = vtkPolyData()
pd_5.SetPoints(hit_points_5)
pd_5.SetVerts(hit_verts_5)
mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputData(pd_5)
actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)

# 6: pyra (3D)
hit_points_6 = vtkPoints()
hit_verts_6 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = pyra.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_6.InsertNextPoint(x)
        hit_verts_6.InsertNextCell(1, [pid])
pd_6 = vtkPolyData()
pd_6.SetPoints(hit_points_6)
pd_6.SetVerts(hit_verts_6)
mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputData(pd_6)
actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)

# 7: quadlin (3D)
hit_points_7 = vtkPoints()
hit_verts_7 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = quadlin.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_7.InsertNextPoint(x)
        hit_verts_7.InsertNextCell(1, [pid])
pd_7 = vtkPolyData()
pd_7.SetPoints(hit_points_7)
pd_7.SetVerts(hit_verts_7)
mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputData(pd_7)
actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)

# 8: biquad (3D)
hit_points_8 = vtkPoints()
hit_verts_8 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = biquad.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_8.InsertNextPoint(x)
        hit_verts_8.InsertNextCell(1, [pid])
pd_8 = vtkPolyData()
pd_8.SetPoints(hit_points_8)
pd_8.SetVerts(hit_verts_8)
mapper_8 = vtkPolyDataMapper()
mapper_8.SetInputData(pd_8)
actor_8 = vtkActor()
actor_8.SetMapper(mapper_8)

# 9: wedgelin (3D)
hit_points_9 = vtkPoints()
hit_verts_9 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = wedgelin.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_9.InsertNextPoint(x)
        hit_verts_9.InsertNextCell(1, [pid])
pd_9 = vtkPolyData()
pd_9.SetPoints(hit_points_9)
pd_9.SetVerts(hit_verts_9)
mapper_9 = vtkPolyDataMapper()
mapper_9.SetInputData(pd_9)
actor_9 = vtkActor()
actor_9.SetMapper(mapper_9)

# 10: biwedge (3D)
hit_points_10 = vtkPoints()
hit_verts_10 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = biwedge.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_10.InsertNextPoint(x)
        hit_verts_10.InsertNextCell(1, [pid])
pd_10 = vtkPolyData()
pd_10.SetPoints(hit_points_10)
pd_10.SetVerts(hit_verts_10)
mapper_10 = vtkPolyDataMapper()
mapper_10.SetInputData(pd_10)
actor_10 = vtkActor()
actor_10.SetMapper(mapper_10)

# 11: bihex (3D)
hit_points_11 = vtkPoints()
hit_verts_11 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = bihex.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_11.InsertNextPoint(x)
        hit_verts_11.InsertNextCell(1, [pid])
pd_11 = vtkPolyData()
pd_11.SetPoints(hit_points_11)
pd_11.SetVerts(hit_verts_11)
mapper_11 = vtkPolyDataMapper()
mapper_11.SetInputData(pd_11)
actor_11 = vtkActor()
actor_11.SetMapper(mapper_11)

# 12: trihex (3D)
hit_points_12 = vtkPoints()
hit_verts_12 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = trihex.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_12.InsertNextPoint(x)
        hit_verts_12.InsertNextCell(1, [pid])
pd_12 = vtkPolyData()
pd_12.SetPoints(hit_points_12)
pd_12.SetVerts(hit_verts_12)
mapper_12 = vtkPolyDataMapper()
mapper_12.SetInputData(pd_12)
actor_12 = vtkActor()
actor_12.SetMapper(mapper_12)

# 13: tq_pyra (3D)
hit_points_13 = vtkPoints()
hit_verts_13 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = tq_pyra.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_13.InsertNextPoint(x)
        hit_verts_13.InsertNextCell(1, [pid])
pd_13 = vtkPolyData()
pd_13.SetPoints(hit_points_13)
pd_13.SetVerts(hit_verts_13)
mapper_13 = vtkPolyDataMapper()
mapper_13.SetInputData(pd_13)
actor_13 = vtkActor()
actor_13.SetMapper(mapper_13)

# 14: bitri (3D)
hit_points_14 = vtkPoints()
hit_verts_14 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        phi = math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) * math.sin(phi) + center[0]
        pt[1] = radius * math.sin(theta) * math.sin(phi) + center[1]
        pt[2] = radius * math.cos(phi) + center[2]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = bitri.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_14.InsertNextPoint(x)
        hit_verts_14.InsertNextCell(1, [pid])
pd_14 = vtkPolyData()
pd_14.SetPoints(hit_points_14)
pd_14.SetVerts(hit_verts_14)
mapper_14 = vtkPolyDataMapper()
mapper_14.SetInputData(pd_14)
actor_14 = vtkActor()
actor_14.SetMapper(mapper_14)

# 15: culine (2D)
hit_points_15 = vtkPoints()
hit_verts_15 = vtkCellArray()
for _ in range(n_test):
    p0 = [0.0, 0.0, 0.0]
    p1 = [0.0, 0.0, 0.0]
    for pt in [p0, p1]:
        theta = 2.0 * math.pi * sequence.GetValue()
        sequence.Next()
        pt[0] = radius * math.cos(theta) + center[0]
        pt[1] = radius * math.sin(theta) + center[1]
    t_val = reference(0.0)
    x = [0.0, 0.0, 0.0]
    pcoords = [0.0, 0.0, 0.0]
    sub_id = reference(0)
    result = culine.IntersectWithLine(p0, p1, 1.0e-7, t_val, x, pcoords, sub_id)
    if result:
        pid = hit_points_15.InsertNextPoint(x)
        hit_verts_15.InsertNextCell(1, [pid])
pd_15 = vtkPolyData()
pd_15.SetPoints(hit_points_15)
pd_15.SetVerts(hit_verts_15)
mapper_15 = vtkPolyDataMapper()
mapper_15.SetInputData(pd_15)
actor_15 = vtkActor()
actor_15.SetMapper(mapper_15)

# Renderers.
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.25, 0.25)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetViewport(0.25, 0.0, 0.5, 0.25)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.SetViewport(0.5, 0.0, 0.75, 0.25)

renderer_3 = vtkRenderer()
renderer_3.AddActor(actor_3)
renderer_3.SetViewport(0.75, 0.0, 1.0, 0.25)

renderer_4 = vtkRenderer()
renderer_4.AddActor(actor_4)
renderer_4.SetViewport(0.0, 0.25, 0.25, 0.5)

renderer_5 = vtkRenderer()
renderer_5.AddActor(actor_5)
renderer_5.SetViewport(0.25, 0.25, 0.5, 0.5)

renderer_6 = vtkRenderer()
renderer_6.AddActor(actor_6)
renderer_6.SetViewport(0.5, 0.25, 0.75, 0.5)

renderer_7 = vtkRenderer()
renderer_7.AddActor(actor_7)
renderer_7.SetViewport(0.75, 0.25, 1.0, 0.5)

renderer_8 = vtkRenderer()
renderer_8.AddActor(actor_8)
renderer_8.SetViewport(0.0, 0.5, 0.25, 0.75)

renderer_9 = vtkRenderer()
renderer_9.AddActor(actor_9)
renderer_9.SetViewport(0.25, 0.5, 0.5, 0.75)

renderer_10 = vtkRenderer()
renderer_10.AddActor(actor_10)
renderer_10.SetViewport(0.5, 0.5, 0.75, 0.75)

renderer_11 = vtkRenderer()
renderer_11.AddActor(actor_11)
renderer_11.SetViewport(0.75, 0.5, 1.0, 0.75)

renderer_12 = vtkRenderer()
renderer_12.AddActor(actor_12)
renderer_12.SetViewport(0.0, 0.75, 0.25, 1.0)

renderer_13 = vtkRenderer()
renderer_13.AddActor(actor_13)
renderer_13.SetViewport(0.25, 0.75, 0.5, 1.0)

renderer_14 = vtkRenderer()
renderer_14.AddActor(actor_14)
renderer_14.SetViewport(0.5, 0.75, 0.75, 1.0)

renderer_15 = vtkRenderer()
renderer_15.AddActor(actor_15)
renderer_15.SetViewport(0.75, 0.75, 1.0, 1.0)

# Render window.
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)
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
render_window.SetWindowName("quadratic intersection")

# Scene.
renderer_0.GetActiveCamera().SetPosition(2, 2, 2)
renderer_0.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_0.ResetCamera()
renderer_1.GetActiveCamera().SetPosition(2, 2, 2)
renderer_1.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_1.ResetCamera()
renderer_2.GetActiveCamera().SetPosition(2, 2, 2)
renderer_2.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_2.ResetCamera()
renderer_3.GetActiveCamera().SetPosition(2, 2, 2)
renderer_3.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_3.ResetCamera()
renderer_4.GetActiveCamera().SetPosition(2, 2, 2)
renderer_4.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_4.ResetCamera()
renderer_5.GetActiveCamera().SetPosition(2, 2, 2)
renderer_5.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_5.ResetCamera()
renderer_6.GetActiveCamera().SetPosition(2, 2, 2)
renderer_6.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_6.ResetCamera()
renderer_7.GetActiveCamera().SetPosition(2, 2, 2)
renderer_7.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_7.ResetCamera()
renderer_8.GetActiveCamera().SetPosition(2, 2, 2)
renderer_8.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_8.ResetCamera()
renderer_9.GetActiveCamera().SetPosition(2, 2, 2)
renderer_9.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_9.ResetCamera()
renderer_10.GetActiveCamera().SetPosition(2, 2, 2)
renderer_10.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_10.ResetCamera()
renderer_11.GetActiveCamera().SetPosition(2, 2, 2)
renderer_11.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_11.ResetCamera()
renderer_12.GetActiveCamera().SetPosition(2, 2, 2)
renderer_12.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_12.ResetCamera()
renderer_13.GetActiveCamera().SetPosition(2, 2, 2)
renderer_13.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_13.ResetCamera()
renderer_14.GetActiveCamera().SetPosition(2, 2, 2)
renderer_14.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_14.ResetCamera()
renderer_15.GetActiveCamera().SetPosition(2, 2, 2)
renderer_15.GetActiveCamera().SetFocalPoint(center[0], center[1], center[2])
renderer_15.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
