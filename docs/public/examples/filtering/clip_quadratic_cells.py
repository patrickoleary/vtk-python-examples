#!/usr/bin/env python

# Clip every quadratic cell type and display results in a scene with
# wireframe originals and clipped solid cells on a backdrop.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import numpy as np

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkBiQuadraticQuad,
    vtkBiQuadraticQuadraticHexahedron,
    vtkBiQuadraticQuadraticWedge,
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
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.util.numpy_support import numpy_to_vtk as ntov

# ================================================================
# QuadraticEdge
# ================================================================
edge_points = vtkPoints()
edge_points.SetNumberOfPoints(3)
edge_points.SetData(ntov(np.array([[0, 0, 0], [1.0, 0, 0], [0.5, 0.25, 0]])))
edge_scalars = vtkFloatArray()
edge_scalars.SetNumberOfTuples(3)
edge_scalars.InsertValue(0, 0.0)
edge_scalars.InsertValue(1, 0.0)
edge_scalars.InsertValue(2, 0.9)
a_edge = vtkQuadraticEdge()
for i in range(a_edge.GetNumberOfPoints()):
    a_edge.GetPointIds().SetId(i, i)
edge_grid = vtkUnstructuredGrid()
edge_grid.Allocate(1, 1)
edge_grid.InsertNextCell(a_edge.GetCellType(), a_edge.GetPointIds())
edge_grid.SetPoints(edge_points)
edge_grid.GetPointData().SetScalars(edge_scalars)

edge_clip_filter = vtkClipDataSet()
edge_clip_filter.SetInputData(edge_grid)
edge_clip_filter.SetValue(0.5)
edge_clip_mapper = vtkDataSetMapper()
edge_clip_mapper.SetInputConnection(edge_clip_filter.GetOutputPort())
edge_clip_mapper.ScalarVisibilityOff()
edge_wire_mapper = vtkDataSetMapper()
edge_wire_mapper.SetInputData(edge_grid)
edge_wire_mapper.ScalarVisibilityOff()
edge_wire_actor = vtkActor()
edge_wire_actor.SetMapper(edge_wire_mapper)
edge_wire_actor.GetProperty().SetRepresentationToWireframe()
edge_wire_actor.GetProperty().SetAmbient(1.0)
edge_clip_actor = vtkActor()
edge_clip_actor.SetMapper(edge_clip_mapper)
edge_clip_actor.GetProperty().BackfaceCullingOn()
edge_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic triangle
# ================================================================
tri_points = vtkPoints()
tri_points.SetNumberOfPoints(6)
tri_points.SetData(ntov(np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.8, 0.0],
    [0.5, 0.0, 0.0], [0.75, 0.4, 0.0], [0.25, 0.4, 0.0]])))
tri_scalars = vtkFloatArray()
tri_scalars.SetNumberOfTuples(6)
tri_scalars.InsertValue(0, 0.0)
tri_scalars.InsertValue(1, 0.0)
tri_scalars.InsertValue(2, 0.0)
tri_scalars.InsertValue(3, 1.0)
tri_scalars.InsertValue(4, 0.0)
tri_scalars.InsertValue(5, 0.0)
a_tri = vtkQuadraticTriangle()
for i in range(a_tri.GetNumberOfPoints()):
    a_tri.GetPointIds().SetId(i, i)
tri_grid = vtkUnstructuredGrid()
tri_grid.Allocate(1, 1)
tri_grid.InsertNextCell(a_tri.GetCellType(), a_tri.GetPointIds())
tri_grid.SetPoints(tri_points)
tri_grid.GetPointData().SetScalars(tri_scalars)

tri_clip_filter = vtkClipDataSet()
tri_clip_filter.SetInputData(tri_grid)
tri_clip_filter.SetValue(0.5)
tri_clip_mapper = vtkDataSetMapper()
tri_clip_mapper.SetInputConnection(tri_clip_filter.GetOutputPort())
tri_clip_mapper.ScalarVisibilityOff()
tri_wire_mapper = vtkDataSetMapper()
tri_wire_mapper.SetInputData(tri_grid)
tri_wire_mapper.ScalarVisibilityOff()
tri_wire_actor = vtkActor()
tri_wire_actor.SetMapper(tri_wire_mapper)
tri_wire_actor.GetProperty().SetRepresentationToWireframe()
tri_wire_actor.GetProperty().SetAmbient(1.0)
tri_clip_actor = vtkActor()
tri_clip_actor.SetMapper(tri_clip_mapper)
tri_clip_actor.GetProperty().BackfaceCullingOn()
tri_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic quadrilateral
# ================================================================
quad_points = vtkPoints()
quad_points.SetNumberOfPoints(8)
quad_points.SetData(ntov(np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
    [0.5, 0.0, 0.0], [1.0, 0.5, 0.0], [0.5, 1.0, 0.0], [0.0, 0.5, 0.0]])))
quad_scalars = vtkFloatArray()
quad_scalars.SetNumberOfTuples(8)
quad_scalars.InsertValue(0, 0.0)
quad_scalars.InsertValue(1, 0.0)
quad_scalars.InsertValue(2, 1.0)
quad_scalars.InsertValue(3, 1.0)
quad_scalars.InsertValue(4, 1.0)
quad_scalars.InsertValue(5, 0.0)
quad_scalars.InsertValue(6, 0.0)
quad_scalars.InsertValue(7, 0.0)
a_quad = vtkQuadraticQuad()
for i in range(a_quad.GetNumberOfPoints()):
    a_quad.GetPointIds().SetId(i, i)
quad_grid = vtkUnstructuredGrid()
quad_grid.Allocate(1, 1)
quad_grid.InsertNextCell(a_quad.GetCellType(), a_quad.GetPointIds())
quad_grid.SetPoints(quad_points)
quad_grid.GetPointData().SetScalars(quad_scalars)

quad_clip_filter = vtkClipDataSet()
quad_clip_filter.SetInputData(quad_grid)
quad_clip_filter.SetValue(0.5)
quad_clip_mapper = vtkDataSetMapper()
quad_clip_mapper.SetInputConnection(quad_clip_filter.GetOutputPort())
quad_clip_mapper.ScalarVisibilityOff()
quad_wire_mapper = vtkDataSetMapper()
quad_wire_mapper.SetInputData(quad_grid)
quad_wire_mapper.ScalarVisibilityOff()
quad_wire_actor = vtkActor()
quad_wire_actor.SetMapper(quad_wire_mapper)
quad_wire_actor.GetProperty().SetRepresentationToWireframe()
quad_wire_actor.GetProperty().SetAmbient(1.0)
quad_clip_actor = vtkActor()
quad_clip_actor.SetMapper(quad_clip_mapper)
quad_clip_actor.GetProperty().BackfaceCullingOn()
quad_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# BiQuadratic quadrilateral
# ================================================================
bquad_points = vtkPoints()
bquad_points.SetNumberOfPoints(9)
bquad_points.SetData(ntov(np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
    [0.5, 0.0, 0.0], [1.0, 0.5, 0.0], [0.5, 1.0, 0.0], [0.0, 0.5, 0.0],
    [0.5, 0.5, 0.0]])))
bquad_scalars = vtkFloatArray()
bquad_scalars.SetNumberOfTuples(9)
bquad_scalars.InsertValue(0, 1.0)
bquad_scalars.InsertValue(1, 1.0)
bquad_scalars.InsertValue(2, 1.0)
bquad_scalars.InsertValue(3, 1.0)
bquad_scalars.InsertValue(4, 0.0)
bquad_scalars.InsertValue(5, 0.0)
bquad_scalars.InsertValue(6, 0.0)
bquad_scalars.InsertValue(7, 0.0)
bquad_scalars.InsertValue(8, 1.0)
a_bquad = vtkBiQuadraticQuad()
for i in range(a_bquad.GetNumberOfPoints()):
    a_bquad.GetPointIds().SetId(i, i)
bquad_grid = vtkUnstructuredGrid()
bquad_grid.Allocate(1, 1)
bquad_grid.InsertNextCell(a_bquad.GetCellType(), a_bquad.GetPointIds())
bquad_grid.SetPoints(bquad_points)
bquad_grid.GetPointData().SetScalars(bquad_scalars)

bquad_clip_filter = vtkClipDataSet()
bquad_clip_filter.SetInputData(bquad_grid)
bquad_clip_filter.SetValue(0.5)
bquad_clip_mapper = vtkDataSetMapper()
bquad_clip_mapper.SetInputConnection(bquad_clip_filter.GetOutputPort())
bquad_clip_mapper.ScalarVisibilityOff()
bquad_wire_mapper = vtkDataSetMapper()
bquad_wire_mapper.SetInputData(bquad_grid)
bquad_wire_mapper.ScalarVisibilityOff()
bquad_wire_actor = vtkActor()
bquad_wire_actor.SetMapper(bquad_wire_mapper)
bquad_wire_actor.GetProperty().SetRepresentationToWireframe()
bquad_wire_actor.GetProperty().SetAmbient(1.0)
bquad_clip_actor = vtkActor()
bquad_clip_actor.SetMapper(bquad_clip_mapper)
bquad_clip_actor.GetProperty().BackfaceCullingOn()
bquad_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic linear quadrilateral
# ================================================================
qlquad_points = vtkPoints()
qlquad_points.SetNumberOfPoints(6)
qlquad_points.SetData(ntov(np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0],
    [0.5, 0.0, 0.0], [0.5, 1.0, 0.0]])))
qlquad_scalars = vtkFloatArray()
qlquad_scalars.SetNumberOfTuples(6)
qlquad_scalars.InsertValue(0, 1.0)
qlquad_scalars.InsertValue(1, 1.0)
qlquad_scalars.InsertValue(2, 0.0)
qlquad_scalars.InsertValue(3, 0.0)
qlquad_scalars.InsertValue(4, 0.0)
qlquad_scalars.InsertValue(5, 1.0)
a_qlquad = vtkQuadraticLinearQuad()
for i in range(a_qlquad.GetNumberOfPoints()):
    a_qlquad.GetPointIds().SetId(i, i)
qlquad_grid = vtkUnstructuredGrid()
qlquad_grid.Allocate(1, 1)
qlquad_grid.InsertNextCell(a_qlquad.GetCellType(), a_qlquad.GetPointIds())
qlquad_grid.SetPoints(qlquad_points)
qlquad_grid.GetPointData().SetScalars(qlquad_scalars)

qlquad_clip_filter = vtkClipDataSet()
qlquad_clip_filter.SetInputData(qlquad_grid)
qlquad_clip_filter.SetValue(0.5)
qlquad_clip_mapper = vtkDataSetMapper()
qlquad_clip_mapper.SetInputConnection(qlquad_clip_filter.GetOutputPort())
qlquad_clip_mapper.ScalarVisibilityOff()
qlquad_wire_mapper = vtkDataSetMapper()
qlquad_wire_mapper.SetInputData(qlquad_grid)
qlquad_wire_mapper.ScalarVisibilityOff()
qlquad_wire_actor = vtkActor()
qlquad_wire_actor.SetMapper(qlquad_wire_mapper)
qlquad_wire_actor.GetProperty().SetRepresentationToWireframe()
qlquad_wire_actor.GetProperty().SetAmbient(1.0)
qlquad_clip_actor = vtkActor()
qlquad_clip_actor.SetMapper(qlquad_clip_mapper)
qlquad_clip_actor.GetProperty().BackfaceCullingOn()
qlquad_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic tetrahedron
# ================================================================
tet_points = vtkPoints()
tet_points.SetNumberOfPoints(10)
tet_points.SetData(ntov(np.array([
    [0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 0.8, 0.0], [0.5, 0.4, 1.0],
    [0.5, 0.0, 0.0], [0.75, 0.4, 0.0], [0.25, 0.4, 0.0],
    [0.25, 0.2, 0.5], [0.75, 0.2, 0.5], [0.50, 0.6, 0.5]])))
tet_scalars = vtkFloatArray()
tet_scalars.SetNumberOfTuples(10)
for i in range(4):
    tet_scalars.InsertValue(i, 1.0)
for i in range(4, 10):
    tet_scalars.InsertValue(i, 0.0)
a_tet = vtkQuadraticTetra()
for i in range(a_tet.GetNumberOfPoints()):
    a_tet.GetPointIds().SetId(i, i)
tet_grid = vtkUnstructuredGrid()
tet_grid.Allocate(1, 1)
tet_grid.InsertNextCell(a_tet.GetCellType(), a_tet.GetPointIds())
tet_grid.SetPoints(tet_points)
tet_grid.GetPointData().SetScalars(tet_scalars)

tet_clip_filter = vtkClipDataSet()
tet_clip_filter.SetInputData(tet_grid)
tet_clip_filter.SetValue(0.5)
tet_clip_mapper = vtkDataSetMapper()
tet_clip_mapper.SetInputConnection(tet_clip_filter.GetOutputPort())
tet_clip_mapper.ScalarVisibilityOff()
tet_wire_mapper = vtkDataSetMapper()
tet_wire_mapper.SetInputData(tet_grid)
tet_wire_mapper.ScalarVisibilityOff()
tet_wire_actor = vtkActor()
tet_wire_actor.SetMapper(tet_wire_mapper)
tet_wire_actor.GetProperty().SetRepresentationToWireframe()
tet_wire_actor.GetProperty().SetAmbient(1.0)
tet_clip_actor = vtkActor()
tet_clip_actor.SetMapper(tet_clip_mapper)
tet_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic hexahedron
# ================================================================
hex_points = vtkPoints()
hex_points.SetNumberOfPoints(20)
hex_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0.5, 0, 1], [1, 0.5, 1], [0.5, 1, 1], [0, 0.5, 1],
    [0, 0, 0.5], [1, 0, 0.5], [1, 1, 0.5], [0, 1, 0.5]])))
hex_scalars = vtkFloatArray()
hex_scalars.SetNumberOfTuples(20)
for i in range(8):
    hex_scalars.InsertValue(i, 1.0)
for i in range(8, 20):
    hex_scalars.InsertValue(i, 0.0)
a_hex = vtkQuadraticHexahedron()
for i in range(a_hex.GetNumberOfPoints()):
    a_hex.GetPointIds().SetId(i, i)
hex_grid = vtkUnstructuredGrid()
hex_grid.Allocate(1, 1)
hex_grid.InsertNextCell(a_hex.GetCellType(), a_hex.GetPointIds())
hex_grid.SetPoints(hex_points)
hex_grid.GetPointData().SetScalars(hex_scalars)

hex_clip_filter = vtkClipDataSet()
hex_clip_filter.SetInputData(hex_grid)
hex_clip_filter.SetValue(0.5)
hex_clip_mapper = vtkDataSetMapper()
hex_clip_mapper.SetInputConnection(hex_clip_filter.GetOutputPort())
hex_clip_mapper.ScalarVisibilityOff()
hex_wire_mapper = vtkDataSetMapper()
hex_wire_mapper.SetInputData(hex_grid)
hex_wire_mapper.ScalarVisibilityOff()
hex_wire_actor = vtkActor()
hex_wire_actor.SetMapper(hex_wire_mapper)
hex_wire_actor.GetProperty().SetRepresentationToWireframe()
hex_wire_actor.GetProperty().SetAmbient(1.0)
hex_clip_actor = vtkActor()
hex_clip_actor.SetMapper(hex_clip_mapper)
hex_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# TriQuadratic hexahedron
# ================================================================
tqhex_points = vtkPoints()
tqhex_points.SetNumberOfPoints(27)
tqhex_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0.5, 0, 1], [1, 0.5, 1], [0.5, 1, 1], [0, 0.5, 1],
    [0, 0, 0.5], [1, 0, 0.5], [1, 1, 0.5], [0, 1, 0.5],
    [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 1, 0.5],
    [0.5, 0.5, 0.0], [0.5, 0.5, 1], [0.5, 0.5, 0.5]])))
tqhex_scalars = vtkFloatArray()
tqhex_scalars.SetNumberOfTuples(27)
for i in range(8):
    tqhex_scalars.InsertValue(i, 1.0)
for i in range(8, 27):
    tqhex_scalars.InsertValue(i, 0.0)
a_tqhex = vtkTriQuadraticHexahedron()
for i in range(a_tqhex.GetNumberOfPoints()):
    a_tqhex.GetPointIds().SetId(i, i)
tqhex_grid = vtkUnstructuredGrid()
tqhex_grid.Allocate(1, 1)
tqhex_grid.InsertNextCell(a_tqhex.GetCellType(), a_tqhex.GetPointIds())
tqhex_grid.SetPoints(tqhex_points)
tqhex_grid.GetPointData().SetScalars(tqhex_scalars)

tqhex_clip_filter = vtkClipDataSet()
tqhex_clip_filter.SetInputData(tqhex_grid)
tqhex_clip_filter.SetValue(0.5)
tqhex_clip_mapper = vtkDataSetMapper()
tqhex_clip_mapper.SetInputConnection(tqhex_clip_filter.GetOutputPort())
tqhex_clip_mapper.ScalarVisibilityOff()
tqhex_wire_mapper = vtkDataSetMapper()
tqhex_wire_mapper.SetInputData(tqhex_grid)
tqhex_wire_mapper.ScalarVisibilityOff()
tqhex_wire_actor = vtkActor()
tqhex_wire_actor.SetMapper(tqhex_wire_mapper)
tqhex_wire_actor.GetProperty().SetRepresentationToWireframe()
tqhex_wire_actor.GetProperty().SetAmbient(1.0)
tqhex_clip_actor = vtkActor()
tqhex_clip_actor.SetMapper(tqhex_clip_mapper)
tqhex_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# BiQuadratic Quadratic hexahedron
# ================================================================
bqhex_points = vtkPoints()
bqhex_points.SetNumberOfPoints(24)
bqhex_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [1, 1, 1], [0, 1, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0.5, 0, 1], [1, 0.5, 1], [0.5, 1, 1], [0, 0.5, 1],
    [0, 0, 0.5], [1, 0, 0.5], [1, 1, 0.5], [0, 1, 0.5],
    [0, 0.5, 0.5], [1, 0.5, 0.5], [0.5, 0, 0.5], [0.5, 1, 0.5]])))
bqhex_points.InsertPoint(20, 0, 0.5, 0.5)
bqhex_scalars = vtkFloatArray()
bqhex_scalars.SetNumberOfTuples(24)
for i in range(8):
    bqhex_scalars.InsertValue(i, 1.0)
for i in range(8, 24):
    bqhex_scalars.InsertValue(i, 0.0)
a_bqhex = vtkBiQuadraticQuadraticHexahedron()
for i in range(a_bqhex.GetNumberOfPoints()):
    a_bqhex.GetPointIds().SetId(i, i)
bqhex_grid = vtkUnstructuredGrid()
bqhex_grid.Allocate(1, 1)
bqhex_grid.InsertNextCell(a_bqhex.GetCellType(), a_bqhex.GetPointIds())
bqhex_grid.SetPoints(bqhex_points)
bqhex_grid.GetPointData().SetScalars(bqhex_scalars)

bqhex_clip_filter = vtkClipDataSet()
bqhex_clip_filter.SetInputData(bqhex_grid)
bqhex_clip_filter.SetValue(0.5)
bqhex_clip_mapper = vtkDataSetMapper()
bqhex_clip_mapper.SetInputConnection(bqhex_clip_filter.GetOutputPort())
bqhex_clip_mapper.ScalarVisibilityOff()
bqhex_wire_mapper = vtkDataSetMapper()
bqhex_wire_mapper.SetInputData(bqhex_grid)
bqhex_wire_mapper.ScalarVisibilityOff()
bqhex_wire_actor = vtkActor()
bqhex_wire_actor.SetMapper(bqhex_wire_mapper)
bqhex_wire_actor.GetProperty().SetRepresentationToWireframe()
bqhex_wire_actor.GetProperty().SetAmbient(1.0)
bqhex_clip_actor = vtkActor()
bqhex_clip_actor.SetMapper(bqhex_clip_mapper)
bqhex_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic wedge
# ================================================================
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(15)
wedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [0, 1, 1],
    [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0],
    [0.5, 0, 1], [0.5, 0.5, 1], [0, 0.5, 1],
    [0, 0, 0.5], [1, 0, 0.5], [0, 1, 0.5]])))
wedge_scalars = vtkFloatArray()
wedge_scalars.SetNumberOfTuples(15)
for i in range(6):
    wedge_scalars.InsertValue(i, 1.0)
for i in range(6, 15):
    wedge_scalars.InsertValue(i, 0.0)
a_wedge = vtkQuadraticWedge()
for i in range(a_wedge.GetNumberOfPoints()):
    a_wedge.GetPointIds().SetId(i, i)
wedge_grid = vtkUnstructuredGrid()
wedge_grid.Allocate(1, 1)
wedge_grid.InsertNextCell(a_wedge.GetCellType(), a_wedge.GetPointIds())
wedge_grid.SetPoints(wedge_points)
wedge_grid.GetPointData().SetScalars(wedge_scalars)

wedge_clip_filter = vtkClipDataSet()
wedge_clip_filter.SetInputData(wedge_grid)
wedge_clip_filter.SetValue(0.5)
wedge_clip_mapper = vtkDataSetMapper()
wedge_clip_mapper.SetInputConnection(wedge_clip_filter.GetOutputPort())
wedge_clip_mapper.ScalarVisibilityOff()
wedge_wire_mapper = vtkDataSetMapper()
wedge_wire_mapper.SetInputData(wedge_grid)
wedge_wire_mapper.ScalarVisibilityOff()
wedge_wire_actor = vtkActor()
wedge_wire_actor.SetMapper(wedge_wire_mapper)
wedge_wire_actor.GetProperty().SetRepresentationToWireframe()
wedge_wire_actor.GetProperty().SetAmbient(1.0)
wedge_clip_actor = vtkActor()
wedge_clip_actor.SetMapper(wedge_clip_mapper)
wedge_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic linear wedge
# ================================================================
qlwedge_points = vtkPoints()
qlwedge_points.SetNumberOfPoints(12)
qlwedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [0, 1, 1],
    [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0],
    [0.5, 0, 1], [0.5, 0.5, 1], [0, 0.5, 1]])))
qlwedge_scalars = vtkFloatArray()
qlwedge_scalars.SetNumberOfTuples(12)
for i in range(6):
    qlwedge_scalars.InsertValue(i, 1.0)
for i in range(6, 12):
    qlwedge_scalars.InsertValue(i, 0.0)
a_qlwedge = vtkQuadraticLinearWedge()
for i in range(a_qlwedge.GetNumberOfPoints()):
    a_qlwedge.GetPointIds().SetId(i, i)
qlwedge_grid = vtkUnstructuredGrid()
qlwedge_grid.Allocate(1, 1)
qlwedge_grid.InsertNextCell(a_qlwedge.GetCellType(), a_qlwedge.GetPointIds())
qlwedge_grid.SetPoints(qlwedge_points)
qlwedge_grid.GetPointData().SetScalars(qlwedge_scalars)

qlwedge_clip_filter = vtkClipDataSet()
qlwedge_clip_filter.SetInputData(qlwedge_grid)
qlwedge_clip_filter.SetValue(0.5)
qlwedge_clip_mapper = vtkDataSetMapper()
qlwedge_clip_mapper.SetInputConnection(qlwedge_clip_filter.GetOutputPort())
qlwedge_clip_mapper.ScalarVisibilityOff()
qlwedge_wire_mapper = vtkDataSetMapper()
qlwedge_wire_mapper.SetInputData(qlwedge_grid)
qlwedge_wire_mapper.ScalarVisibilityOff()
qlwedge_wire_actor = vtkActor()
qlwedge_wire_actor.SetMapper(qlwedge_wire_mapper)
qlwedge_wire_actor.GetProperty().SetRepresentationToWireframe()
qlwedge_wire_actor.GetProperty().SetAmbient(1.0)
qlwedge_clip_actor = vtkActor()
qlwedge_clip_actor.SetMapper(qlwedge_clip_mapper)
qlwedge_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# BiQuadratic wedge
# ================================================================
bqwedge_points = vtkPoints()
bqwedge_points.SetNumberOfPoints(18)
bqwedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0],
    [0, 0, 1], [1, 0, 1], [0, 1, 1],
    [0.5, 0, 0], [0.5, 0.5, 0], [0, 0.5, 0],
    [0.5, 0, 1], [0.5, 0.5, 1], [0, 0.5, 1],
    [0, 0, 0.5], [1, 0, 0.5], [0, 1, 0.5],
    [0.5, 0, 0.5], [0.5, 0.5, 0.5], [0, 0.5, 0.5]])))
bqwedge_scalars = vtkFloatArray()
bqwedge_scalars.SetNumberOfTuples(18)
for i in range(6):
    bqwedge_scalars.InsertValue(i, 1.0)
for i in range(6, 18):
    bqwedge_scalars.InsertValue(i, 0.0)
a_bqwedge = vtkBiQuadraticQuadraticWedge()
for i in range(a_bqwedge.GetNumberOfPoints()):
    a_bqwedge.GetPointIds().SetId(i, i)
bqwedge_grid = vtkUnstructuredGrid()
bqwedge_grid.Allocate(1, 1)
bqwedge_grid.InsertNextCell(a_bqwedge.GetCellType(), a_bqwedge.GetPointIds())
bqwedge_grid.SetPoints(bqwedge_points)
bqwedge_grid.GetPointData().SetScalars(bqwedge_scalars)

bqwedge_clip_filter = vtkClipDataSet()
bqwedge_clip_filter.SetInputData(bqwedge_grid)
bqwedge_clip_filter.SetValue(0.5)
bqwedge_clip_mapper = vtkDataSetMapper()
bqwedge_clip_mapper.SetInputConnection(bqwedge_clip_filter.GetOutputPort())
bqwedge_clip_mapper.ScalarVisibilityOff()
bqwedge_wire_mapper = vtkDataSetMapper()
bqwedge_wire_mapper.SetInputData(bqwedge_grid)
bqwedge_wire_mapper.ScalarVisibilityOff()
bqwedge_wire_actor = vtkActor()
bqwedge_wire_actor.SetMapper(bqwedge_wire_mapper)
bqwedge_wire_actor.GetProperty().SetRepresentationToWireframe()
bqwedge_wire_actor.GetProperty().SetAmbient(1.0)
bqwedge_clip_actor = vtkActor()
bqwedge_clip_actor.SetMapper(bqwedge_clip_mapper)
bqwedge_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Quadratic pyramid
# ================================================================
pyra_points = vtkPoints()
pyra_points.SetNumberOfPoints(13)
pyra_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0, 0, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [0, 0.5, 0.5]])))
pyra_scalars = vtkFloatArray()
pyra_scalars.SetNumberOfTuples(13)
for i in range(5):
    pyra_scalars.InsertValue(i, 1.0)
for i in range(5, 13):
    pyra_scalars.InsertValue(i, 0.0)
a_pyramid = vtkQuadraticPyramid()
for i in range(a_pyramid.GetNumberOfPoints()):
    a_pyramid.GetPointIds().SetId(i, i)
pyra_grid = vtkUnstructuredGrid()
pyra_grid.Allocate(1, 1)
pyra_grid.InsertNextCell(a_pyramid.GetCellType(), a_pyramid.GetPointIds())
pyra_grid.SetPoints(pyra_points)
pyra_grid.GetPointData().SetScalars(pyra_scalars)

pyra_clip_filter = vtkClipDataSet()
pyra_clip_filter.SetInputData(pyra_grid)
pyra_clip_filter.SetValue(0.5)
pyra_clip_mapper = vtkDataSetMapper()
pyra_clip_mapper.SetInputConnection(pyra_clip_filter.GetOutputPort())
pyra_clip_mapper.ScalarVisibilityOff()
pyra_wire_mapper = vtkDataSetMapper()
pyra_wire_mapper.SetInputData(pyra_grid)
pyra_wire_mapper.ScalarVisibilityOff()
pyra_wire_actor = vtkActor()
pyra_wire_actor.SetMapper(pyra_wire_mapper)
pyra_wire_actor.GetProperty().SetRepresentationToWireframe()
pyra_wire_actor.GetProperty().SetAmbient(1.0)
pyra_clip_actor = vtkActor()
pyra_clip_actor.SetMapper(pyra_clip_mapper)
pyra_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# TriQuadratic pyramid
# ================================================================
tqpyra_points = vtkPoints()
tqpyra_points.SetNumberOfPoints(19)
tqpyra_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0, 0, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [0, 0.5, 0.5],
    [0.5, 0.5, 0],
    [1.0 / 3.0, 0, 1.0 / 3.0],
    [2.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
    [1.0 / 3.0, 2.0 / 3.0, 1.0 / 3.0],
    [0, 1.0 / 3.0, 1.0 / 3.0],
    [0.4, 0.4, 0.2]])))
tqpyra_scalars = vtkFloatArray()
tqpyra_scalars.SetNumberOfTuples(19)
for i in range(5):
    tqpyra_scalars.InsertValue(i, 1.0)
for i in range(5, 19):
    tqpyra_scalars.InsertValue(i, 0.0)
a_tqpyramid = vtkTriQuadraticPyramid()
for i in range(a_tqpyramid.GetNumberOfPoints()):
    a_tqpyramid.GetPointIds().SetId(i, i)
tqpyra_grid = vtkUnstructuredGrid()
tqpyra_grid.Allocate(1, 1)
tqpyra_grid.InsertNextCell(a_tqpyramid.GetCellType(), a_tqpyramid.GetPointIds())
tqpyra_grid.SetPoints(tqpyra_points)
tqpyra_grid.GetPointData().SetScalars(tqpyra_scalars)

tqpyra_clip_filter = vtkClipDataSet()
tqpyra_clip_filter.SetInputData(tqpyra_grid)
tqpyra_clip_filter.SetValue(0.5)
tqpyra_clip_mapper = vtkDataSetMapper()
tqpyra_clip_mapper.SetInputConnection(tqpyra_clip_filter.GetOutputPort())
tqpyra_clip_mapper.ScalarVisibilityOff()
tqpyra_wire_mapper = vtkDataSetMapper()
tqpyra_wire_mapper.SetInputData(tqpyra_grid)
tqpyra_wire_mapper.ScalarVisibilityOff()
tqpyra_wire_actor = vtkActor()
tqpyra_wire_actor.SetMapper(tqpyra_wire_mapper)
tqpyra_wire_actor.GetProperty().SetRepresentationToWireframe()
tqpyra_wire_actor.GetProperty().SetAmbient(1.0)
tqpyra_clip_actor = vtkActor()
tqpyra_clip_actor.SetMapper(tqpyra_clip_mapper)
tqpyra_clip_actor.GetProperty().SetAmbient(1.0)

# ================================================================
# Renderer setup
# ================================================================
renderer = vtkRenderer()
renderer.GetCullers().RemoveAllItems()
renderer.SetBackground(0.1, 0.2, 0.3)

renderer.AddActor(edge_wire_actor)
renderer.AddActor(edge_clip_actor)
renderer.AddActor(tri_wire_actor)
renderer.AddActor(tri_clip_actor)
renderer.AddActor(quad_wire_actor)
renderer.AddActor(quad_clip_actor)
renderer.AddActor(bquad_wire_actor)
renderer.AddActor(bquad_clip_actor)
renderer.AddActor(qlquad_wire_actor)
renderer.AddActor(qlquad_clip_actor)
renderer.AddActor(tet_wire_actor)
renderer.AddActor(tet_clip_actor)
renderer.AddActor(hex_wire_actor)
renderer.AddActor(hex_clip_actor)
renderer.AddActor(tqhex_wire_actor)
renderer.AddActor(tqhex_clip_actor)
renderer.AddActor(bqhex_wire_actor)
renderer.AddActor(bqhex_clip_actor)
renderer.AddActor(wedge_wire_actor)
renderer.AddActor(wedge_clip_actor)
renderer.AddActor(bqwedge_wire_actor)
renderer.AddActor(bqwedge_clip_actor)
renderer.AddActor(qlwedge_wire_actor)
renderer.AddActor(qlwedge_clip_actor)
renderer.AddActor(pyra_wire_actor)
renderer.AddActor(pyra_clip_actor)
renderer.AddActor(tqpyra_wire_actor)
renderer.AddActor(tqpyra_clip_actor)

# Position actors in a grid
edge_clip_actor.AddPosition(0, 2, 0)
tri_wire_actor.AddPosition(2, 0, 0)
tri_clip_actor.AddPosition(2, 2, 0)
quad_wire_actor.AddPosition(4, 0, 0)
bquad_wire_actor.AddPosition(4, 0, 2)
qlquad_wire_actor.AddPosition(4, 0, 4)
quad_clip_actor.AddPosition(4, 2, 0)
bquad_clip_actor.AddPosition(4, 2, 2)
qlquad_clip_actor.AddPosition(4, 2, 4)
tet_wire_actor.AddPosition(6, 0, 0)
tet_clip_actor.AddPosition(6, 2, 0)
hex_wire_actor.AddPosition(8, 0, 0)
tqhex_wire_actor.AddPosition(8, 0, 2)
bqhex_wire_actor.AddPosition(8, 0, 4)
hex_clip_actor.AddPosition(8, 2, 0)
tqhex_clip_actor.AddPosition(8, 2, 2)
bqhex_clip_actor.AddPosition(8, 2, 4)
wedge_wire_actor.AddPosition(10, 0, 0)
qlwedge_wire_actor.AddPosition(10, 0, 2)
bqwedge_wire_actor.AddPosition(10, 0, 4)
wedge_clip_actor.AddPosition(10, 2, 0)
qlwedge_clip_actor.AddPosition(10, 2, 2)
bqwedge_clip_actor.AddPosition(10, 2, 4)
pyra_wire_actor.AddPosition(12, 0, 0)
tqpyra_wire_actor.AddPosition(12, 0, 2)
pyra_clip_actor.AddPosition(12, 2, 0)
tqpyra_clip_actor.AddPosition(12, 2, 2)

# Backdrop (inlined from backdrop.py)
base_plane = vtkCubeSource()
base_plane.SetCenter((-1 + 15) / 2.0, -1, (-1 + 6) / 2.0)
base_plane.SetXLength(15 - (-1))
base_plane.SetYLength(0.1)
base_plane.SetZLength(6 - (-1))
base_mapper = vtkPolyDataMapper()
base_mapper.SetInputConnection(base_plane.GetOutputPort())
base_actor = vtkActor()
base_actor.SetMapper(base_mapper)
base_actor.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)
renderer.AddActor(base_actor)

back_plane = vtkCubeSource()
back_plane.SetCenter((-1 + 15) / 2.0, (-1 + 4) / 2.0, -1)
back_plane.SetXLength(15 - (-1))
back_plane.SetYLength(4 - (-1))
back_plane.SetZLength(0.1)
back_mapper = vtkPolyDataMapper()
back_mapper.SetInputConnection(back_plane.GetOutputPort())
back_actor = vtkActor()
back_actor.SetMapper(back_mapper)
back_actor.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)
renderer.AddActor(back_actor)

left_plane = vtkCubeSource()
left_plane.SetCenter(-1, (-1 + 4) / 2.0, (-1 + 6) / 2.0)
left_plane.SetXLength(0.1)
left_plane.SetYLength(4 - (-1))
left_plane.SetZLength(6 - (-1))
left_mapper = vtkPolyDataMapper()
left_mapper.SetInputConnection(left_plane.GetOutputPort())
left_actor = vtkActor()
left_actor.SetMapper(left_mapper)
left_actor.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)
renderer.AddActor(left_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 200)
render_window.SetWindowName("clip quadratic cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(2.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
