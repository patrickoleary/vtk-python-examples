#!/usr/bin/env python

# Contour every quadratic cell type (edge, triangle, quad, biquadratic
# quad, quadratic-linear quad, tetra, hexahedron, tri-quadratic hex,
# biquadratic hex, wedge, quadratic-linear wedge, biquadratic wedge,
# pyramid, tri-quadratic pyramid) with wireframe and contour actors
# on a backdrop.

import numpy as np

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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
from vtkmodules.vtkFiltersCore import vtkContourFilter
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

# --- QuadraticEdge ---
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
a_edge_grid = vtkUnstructuredGrid()
a_edge_grid.Allocate(1, 1)
a_edge_grid.InsertNextCell(a_edge.GetCellType(), a_edge.GetPointIds())
a_edge_grid.SetPoints(edge_points)
a_edge_grid.GetPointData().SetScalars(edge_scalars)
edge_contours = vtkContourFilter()
edge_contours.SetInputData(a_edge_grid)
edge_contours.SetValue(0, 0.5)
a_edge_contour_mapper = vtkDataSetMapper()
a_edge_contour_mapper.SetInputConnection(edge_contours.GetOutputPort())
a_edge_contour_mapper.ScalarVisibilityOff()
a_edge_mapper = vtkDataSetMapper()
a_edge_mapper.SetInputData(a_edge_grid)
a_edge_mapper.ScalarVisibilityOff()
a_edge_actor = vtkActor()
a_edge_actor.SetMapper(a_edge_mapper)
a_edge_actor.GetProperty().SetRepresentationToWireframe()
a_edge_actor.GetProperty().SetAmbient(1.0)
a_edge_contour_actor = vtkActor()
a_edge_contour_actor.SetMapper(a_edge_contour_mapper)
a_edge_contour_actor.GetProperty().BackfaceCullingOn()
a_edge_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticTriangle ---
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
a_tri_grid = vtkUnstructuredGrid()
a_tri_grid.Allocate(1, 1)
a_tri_grid.InsertNextCell(a_tri.GetCellType(), a_tri.GetPointIds())
a_tri_grid.SetPoints(tri_points)
a_tri_grid.GetPointData().SetScalars(tri_scalars)
tri_contours = vtkContourFilter()
tri_contours.SetInputData(a_tri_grid)
tri_contours.SetValue(0, 0.5)
a_tri_contour_mapper = vtkDataSetMapper()
a_tri_contour_mapper.SetInputConnection(tri_contours.GetOutputPort())
a_tri_contour_mapper.ScalarVisibilityOff()
a_tri_mapper = vtkDataSetMapper()
a_tri_mapper.SetInputData(a_tri_grid)
a_tri_mapper.ScalarVisibilityOff()
a_tri_actor = vtkActor()
a_tri_actor.SetMapper(a_tri_mapper)
a_tri_actor.GetProperty().SetRepresentationToWireframe()
a_tri_actor.GetProperty().SetAmbient(1.0)
a_tri_contour_actor = vtkActor()
a_tri_contour_actor.SetMapper(a_tri_contour_mapper)
a_tri_contour_actor.GetProperty().BackfaceCullingOn()
a_tri_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticQuad ---
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
a_quad_grid = vtkUnstructuredGrid()
a_quad_grid.Allocate(1, 1)
a_quad_grid.InsertNextCell(a_quad.GetCellType(), a_quad.GetPointIds())
a_quad_grid.SetPoints(quad_points)
a_quad_grid.GetPointData().SetScalars(quad_scalars)
quad_contours = vtkContourFilter()
quad_contours.SetInputData(a_quad_grid)
quad_contours.SetValue(0, 0.5)
a_quad_contour_mapper = vtkDataSetMapper()
a_quad_contour_mapper.SetInputConnection(quad_contours.GetOutputPort())
a_quad_contour_mapper.ScalarVisibilityOff()
a_quad_mapper = vtkDataSetMapper()
a_quad_mapper.SetInputData(a_quad_grid)
a_quad_mapper.ScalarVisibilityOff()
a_quad_actor = vtkActor()
a_quad_actor.SetMapper(a_quad_mapper)
a_quad_actor.GetProperty().SetRepresentationToWireframe()
a_quad_actor.GetProperty().SetAmbient(1.0)
a_quad_contour_actor = vtkActor()
a_quad_contour_actor.SetMapper(a_quad_contour_mapper)
a_quad_contour_actor.GetProperty().BackfaceCullingOn()
a_quad_contour_actor.GetProperty().SetAmbient(1.0)

# --- BiQuadraticQuad ---
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
a_bquad_grid = vtkUnstructuredGrid()
a_bquad_grid.Allocate(1, 1)
a_bquad_grid.InsertNextCell(a_bquad.GetCellType(), a_bquad.GetPointIds())
a_bquad_grid.SetPoints(bquad_points)
a_bquad_grid.GetPointData().SetScalars(bquad_scalars)
bquad_contours = vtkContourFilter()
bquad_contours.SetInputData(a_bquad_grid)
bquad_contours.SetValue(0, 0.5)
a_bquad_contour_mapper = vtkDataSetMapper()
a_bquad_contour_mapper.SetInputConnection(bquad_contours.GetOutputPort())
a_bquad_contour_mapper.ScalarVisibilityOff()
a_bquad_mapper = vtkDataSetMapper()
a_bquad_mapper.SetInputData(a_bquad_grid)
a_bquad_mapper.ScalarVisibilityOff()
a_bquad_actor = vtkActor()
a_bquad_actor.SetMapper(a_bquad_mapper)
a_bquad_actor.GetProperty().SetRepresentationToWireframe()
a_bquad_actor.GetProperty().SetAmbient(1.0)
a_bquad_contour_actor = vtkActor()
a_bquad_contour_actor.SetMapper(a_bquad_contour_mapper)
a_bquad_contour_actor.GetProperty().BackfaceCullingOn()
a_bquad_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticLinearQuad ---
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
a_qlquad_grid = vtkUnstructuredGrid()
a_qlquad_grid.Allocate(1, 1)
a_qlquad_grid.InsertNextCell(a_qlquad.GetCellType(), a_qlquad.GetPointIds())
a_qlquad_grid.SetPoints(qlquad_points)
a_qlquad_grid.GetPointData().SetScalars(qlquad_scalars)
qlquad_contours = vtkContourFilter()
qlquad_contours.SetInputData(a_qlquad_grid)
qlquad_contours.SetValue(0, 0.5)
a_qlquad_contour_mapper = vtkDataSetMapper()
a_qlquad_contour_mapper.SetInputConnection(qlquad_contours.GetOutputPort())
a_qlquad_contour_mapper.ScalarVisibilityOff()
a_qlquad_mapper = vtkDataSetMapper()
a_qlquad_mapper.SetInputData(a_qlquad_grid)
a_qlquad_mapper.ScalarVisibilityOff()
a_qlquad_actor = vtkActor()
a_qlquad_actor.SetMapper(a_qlquad_mapper)
a_qlquad_actor.GetProperty().SetRepresentationToWireframe()
a_qlquad_actor.GetProperty().SetAmbient(1.0)
a_qlquad_contour_actor = vtkActor()
a_qlquad_contour_actor.SetMapper(a_qlquad_contour_mapper)
a_qlquad_contour_actor.GetProperty().BackfaceCullingOn()
a_qlquad_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticTetra ---
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
a_tet_grid = vtkUnstructuredGrid()
a_tet_grid.Allocate(1, 1)
a_tet_grid.InsertNextCell(a_tet.GetCellType(), a_tet.GetPointIds())
a_tet_grid.SetPoints(tet_points)
a_tet_grid.GetPointData().SetScalars(tet_scalars)
tet_contours = vtkContourFilter()
tet_contours.SetInputData(a_tet_grid)
tet_contours.SetValue(0, 0.5)
a_tet_contour_mapper = vtkDataSetMapper()
a_tet_contour_mapper.SetInputConnection(tet_contours.GetOutputPort())
a_tet_contour_mapper.ScalarVisibilityOff()
a_tet_mapper = vtkDataSetMapper()
a_tet_mapper.SetInputData(a_tet_grid)
a_tet_mapper.ScalarVisibilityOff()
a_tet_actor = vtkActor()
a_tet_actor.SetMapper(a_tet_mapper)
a_tet_actor.GetProperty().SetRepresentationToWireframe()
a_tet_actor.GetProperty().SetAmbient(1.0)
a_tet_contour_actor = vtkActor()
a_tet_contour_actor.SetMapper(a_tet_contour_mapper)
a_tet_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticHexahedron ---
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
a_hex_grid = vtkUnstructuredGrid()
a_hex_grid.Allocate(1, 1)
a_hex_grid.InsertNextCell(a_hex.GetCellType(), a_hex.GetPointIds())
a_hex_grid.SetPoints(hex_points)
a_hex_grid.GetPointData().SetScalars(hex_scalars)
hex_contours = vtkContourFilter()
hex_contours.SetInputData(a_hex_grid)
hex_contours.SetValue(0, 0.5)
a_hex_contour_mapper = vtkDataSetMapper()
a_hex_contour_mapper.SetInputConnection(hex_contours.GetOutputPort())
a_hex_contour_mapper.ScalarVisibilityOff()
a_hex_mapper = vtkDataSetMapper()
a_hex_mapper.SetInputData(a_hex_grid)
a_hex_mapper.ScalarVisibilityOff()
a_hex_actor = vtkActor()
a_hex_actor.SetMapper(a_hex_mapper)
a_hex_actor.GetProperty().SetRepresentationToWireframe()
a_hex_actor.GetProperty().SetAmbient(1.0)
a_hex_contour_actor = vtkActor()
a_hex_contour_actor.SetMapper(a_hex_contour_mapper)
a_hex_contour_actor.GetProperty().SetAmbient(1.0)

# --- TriQuadraticHexahedron ---
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
for i in range(8, 26):
    tqhex_scalars.InsertValue(i, 0.0)
tqhex_scalars.InsertValue(26, 1.0)
a_tqhex = vtkTriQuadraticHexahedron()
for i in range(a_tqhex.GetNumberOfPoints()):
    a_tqhex.GetPointIds().SetId(i, i)
a_tqhex_grid = vtkUnstructuredGrid()
a_tqhex_grid.Allocate(1, 1)
a_tqhex_grid.InsertNextCell(a_tqhex.GetCellType(), a_tqhex.GetPointIds())
a_tqhex_grid.SetPoints(tqhex_points)
a_tqhex_grid.GetPointData().SetScalars(tqhex_scalars)
tqhex_contours = vtkContourFilter()
tqhex_contours.SetInputData(a_tqhex_grid)
tqhex_contours.SetValue(0, 0.5)
a_tqhex_contour_mapper = vtkDataSetMapper()
a_tqhex_contour_mapper.SetInputConnection(tqhex_contours.GetOutputPort())
a_tqhex_contour_mapper.ScalarVisibilityOff()
a_tqhex_mapper = vtkDataSetMapper()
a_tqhex_mapper.SetInputData(a_tqhex_grid)
a_tqhex_mapper.ScalarVisibilityOff()
a_tqhex_actor = vtkActor()
a_tqhex_actor.SetMapper(a_tqhex_mapper)
a_tqhex_actor.GetProperty().SetRepresentationToWireframe()
a_tqhex_actor.GetProperty().SetAmbient(1.0)
a_tqhex_contour_actor = vtkActor()
a_tqhex_contour_actor.SetMapper(a_tqhex_contour_mapper)
a_tqhex_contour_actor.GetProperty().SetAmbient(1.0)

# --- BiQuadraticQuadraticHexahedron ---
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
a_bqhex_grid = vtkUnstructuredGrid()
a_bqhex_grid.Allocate(1, 1)
a_bqhex_grid.InsertNextCell(a_bqhex.GetCellType(), a_bqhex.GetPointIds())
a_bqhex_grid.SetPoints(bqhex_points)
a_bqhex_grid.GetPointData().SetScalars(bqhex_scalars)
bqhex_contours = vtkContourFilter()
bqhex_contours.SetInputData(a_bqhex_grid)
bqhex_contours.SetValue(0, 0.5)
a_bqhex_contour_mapper = vtkDataSetMapper()
a_bqhex_contour_mapper.SetInputConnection(bqhex_contours.GetOutputPort())
a_bqhex_contour_mapper.ScalarVisibilityOff()
a_bqhex_mapper = vtkDataSetMapper()
a_bqhex_mapper.SetInputData(a_bqhex_grid)
a_bqhex_mapper.ScalarVisibilityOff()
a_bqhex_actor = vtkActor()
a_bqhex_actor.SetMapper(a_bqhex_mapper)
a_bqhex_actor.GetProperty().SetRepresentationToWireframe()
a_bqhex_actor.GetProperty().SetAmbient(1.0)
a_bqhex_contour_actor = vtkActor()
a_bqhex_contour_actor.SetMapper(a_bqhex_contour_mapper)
a_bqhex_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticWedge ---
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(15)
wedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1],
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
a_wedge_grid = vtkUnstructuredGrid()
a_wedge_grid.Allocate(1, 1)
a_wedge_grid.InsertNextCell(a_wedge.GetCellType(), a_wedge.GetPointIds())
a_wedge_grid.SetPoints(wedge_points)
a_wedge_grid.GetPointData().SetScalars(wedge_scalars)
wedge_contours = vtkContourFilter()
wedge_contours.SetInputData(a_wedge_grid)
wedge_contours.SetValue(0, 0.5)
a_wedge_contour_mapper = vtkDataSetMapper()
a_wedge_contour_mapper.SetInputConnection(wedge_contours.GetOutputPort())
a_wedge_contour_mapper.ScalarVisibilityOff()
a_wedge_mapper = vtkDataSetMapper()
a_wedge_mapper.SetInputData(a_wedge_grid)
a_wedge_mapper.ScalarVisibilityOff()
a_wedge_actor = vtkActor()
a_wedge_actor.SetMapper(a_wedge_mapper)
a_wedge_actor.GetProperty().SetRepresentationToWireframe()
a_wedge_actor.GetProperty().SetAmbient(1.0)
a_wedge_contour_actor = vtkActor()
a_wedge_contour_actor.SetMapper(a_wedge_contour_mapper)
a_wedge_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticLinearWedge ---
qlwedge_points = vtkPoints()
qlwedge_points.SetNumberOfPoints(12)
qlwedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1],
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
a_qlwedge_grid = vtkUnstructuredGrid()
a_qlwedge_grid.Allocate(1, 1)
a_qlwedge_grid.InsertNextCell(a_qlwedge.GetCellType(), a_qlwedge.GetPointIds())
a_qlwedge_grid.SetPoints(qlwedge_points)
a_qlwedge_grid.GetPointData().SetScalars(qlwedge_scalars)
qlwedge_contours = vtkContourFilter()
qlwedge_contours.SetInputData(a_qlwedge_grid)
qlwedge_contours.SetValue(0, 0.5)
a_qlwedge_contour_mapper = vtkDataSetMapper()
a_qlwedge_contour_mapper.SetInputConnection(qlwedge_contours.GetOutputPort())
a_qlwedge_contour_mapper.ScalarVisibilityOff()
a_qlwedge_mapper = vtkDataSetMapper()
a_qlwedge_mapper.SetInputData(a_qlwedge_grid)
a_qlwedge_mapper.ScalarVisibilityOff()
a_qlwedge_actor = vtkActor()
a_qlwedge_actor.SetMapper(a_qlwedge_mapper)
a_qlwedge_actor.GetProperty().SetRepresentationToWireframe()
a_qlwedge_actor.GetProperty().SetAmbient(1.0)
a_qlwedge_contour_actor = vtkActor()
a_qlwedge_contour_actor.SetMapper(a_qlwedge_contour_mapper)
a_qlwedge_contour_actor.GetProperty().SetAmbient(1.0)

# --- BiQuadraticQuadraticWedge ---
bqwedge_points = vtkPoints()
bqwedge_points.SetNumberOfPoints(18)
bqwedge_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [0, 1, 0], [0, 0, 1], [1, 0, 1], [0, 1, 1],
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
a_bqwedge_grid = vtkUnstructuredGrid()
a_bqwedge_grid.Allocate(1, 1)
a_bqwedge_grid.InsertNextCell(a_bqwedge.GetCellType(), a_bqwedge.GetPointIds())
a_bqwedge_grid.SetPoints(bqwedge_points)
a_bqwedge_grid.GetPointData().SetScalars(bqwedge_scalars)
bqwedge_contours = vtkContourFilter()
bqwedge_contours.SetInputData(a_bqwedge_grid)
bqwedge_contours.SetValue(0, 0.5)
a_bqwedge_contour_mapper = vtkDataSetMapper()
a_bqwedge_contour_mapper.SetInputConnection(bqwedge_contours.GetOutputPort())
a_bqwedge_contour_mapper.ScalarVisibilityOff()
a_bqwedge_mapper = vtkDataSetMapper()
a_bqwedge_mapper.SetInputData(a_bqwedge_grid)
a_bqwedge_mapper.ScalarVisibilityOff()
a_bqwedge_actor = vtkActor()
a_bqwedge_actor.SetMapper(a_bqwedge_mapper)
a_bqwedge_actor.GetProperty().SetRepresentationToWireframe()
a_bqwedge_actor.GetProperty().SetAmbient(1.0)
a_bqwedge_contour_actor = vtkActor()
a_bqwedge_contour_actor.SetMapper(a_bqwedge_contour_mapper)
a_bqwedge_contour_actor.GetProperty().SetAmbient(1.0)

# --- QuadraticPyramid ---
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
a_pyramid_grid = vtkUnstructuredGrid()
a_pyramid_grid.Allocate(1, 1)
a_pyramid_grid.InsertNextCell(a_pyramid.GetCellType(), a_pyramid.GetPointIds())
a_pyramid_grid.SetPoints(pyra_points)
a_pyramid_grid.GetPointData().SetScalars(pyra_scalars)
pyra_contours = vtkContourFilter()
pyra_contours.SetInputData(a_pyramid_grid)
pyra_contours.SetValue(0, 0.5)
a_pyramid_contour_mapper = vtkDataSetMapper()
a_pyramid_contour_mapper.SetInputConnection(pyra_contours.GetOutputPort())
a_pyramid_contour_mapper.ScalarVisibilityOff()
a_pyramid_mapper = vtkDataSetMapper()
a_pyramid_mapper.SetInputData(a_pyramid_grid)
a_pyramid_mapper.ScalarVisibilityOff()
a_pyramid_actor = vtkActor()
a_pyramid_actor.SetMapper(a_pyramid_mapper)
a_pyramid_actor.GetProperty().SetRepresentationToWireframe()
a_pyramid_actor.GetProperty().SetAmbient(1.0)
a_pyramid_contour_actor = vtkActor()
a_pyramid_contour_actor.SetMapper(a_pyramid_contour_mapper)
a_pyramid_contour_actor.GetProperty().SetAmbient(1.0)

# --- TriQuadraticPyramid ---
tqpyra_points = vtkPoints()
tqpyra_points.SetNumberOfPoints(19)
tqpyra_points.SetData(ntov(np.array([
    [0, 0, 0], [1, 0, 0], [1, 1, 0], [0, 1, 0], [0, 0, 1],
    [0.5, 0, 0], [1, 0.5, 0], [0.5, 1, 0], [0, 0.5, 0],
    [0, 0, 0.5], [0.5, 0, 0.5], [0.5, 0.5, 0.5], [0, 0.5, 0.5],
    [0.5, 0.5, 0],
    [1.0 / 3.0, 0, 1.0 / 3.0], [2.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0],
    [1.0 / 3.0, 2.0 / 3.0, 1.0 / 3.0], [0, 1.0 / 3.0, 1.0 / 3.0],
    [0.4, 0.4, 0.2]])))
tqpyra_scalars = vtkFloatArray()
tqpyra_scalars.SetNumberOfTuples(19)
for i in range(5):
    tqpyra_scalars.InsertValue(i, 1.0)
for i in range(5, 18):
    tqpyra_scalars.InsertValue(i, 0.0)
tqpyra_scalars.InsertValue(18, 1.0)
a_tqpyramid = vtkTriQuadraticPyramid()
for i in range(a_tqpyramid.GetNumberOfPoints()):
    a_tqpyramid.GetPointIds().SetId(i, i)
a_tqpyramid_grid = vtkUnstructuredGrid()
a_tqpyramid_grid.Allocate(1, 1)
a_tqpyramid_grid.InsertNextCell(a_tqpyramid.GetCellType(), a_tqpyramid.GetPointIds())
a_tqpyramid_grid.SetPoints(tqpyra_points)
a_tqpyramid_grid.GetPointData().SetScalars(tqpyra_scalars)
tqpyra_contours = vtkContourFilter()
tqpyra_contours.SetInputData(a_tqpyramid_grid)
tqpyra_contours.SetValue(0, 0.5)
a_tqpyramid_contour_mapper = vtkDataSetMapper()
a_tqpyramid_contour_mapper.SetInputConnection(tqpyra_contours.GetOutputPort())
a_tqpyramid_contour_mapper.ScalarVisibilityOff()
a_tqpyramid_mapper = vtkDataSetMapper()
a_tqpyramid_mapper.SetInputData(a_tqpyramid_grid)
a_tqpyramid_mapper.ScalarVisibilityOff()
a_tqpyramid_actor = vtkActor()
a_tqpyramid_actor.SetMapper(a_tqpyramid_mapper)
a_tqpyramid_actor.GetProperty().SetRepresentationToWireframe()
a_tqpyramid_actor.GetProperty().SetAmbient(1.0)
a_tqpyramid_contour_actor = vtkActor()
a_tqpyramid_contour_actor.SetMapper(a_tqpyramid_contour_mapper)
a_tqpyramid_contour_actor.GetProperty().SetAmbient(1.0)

# Renderer
renderer = vtkRenderer()
renderer.GetCullers().RemoveAllItems()
renderer.SetBackground(0.1, 0.2, 0.3)

# Add all actors
renderer.AddActor(a_edge_actor)
renderer.AddActor(a_edge_contour_actor)
renderer.AddActor(a_tri_actor)
renderer.AddActor(a_tri_contour_actor)
renderer.AddActor(a_quad_actor)
renderer.AddActor(a_quad_contour_actor)
renderer.AddActor(a_bquad_actor)
renderer.AddActor(a_bquad_contour_actor)
renderer.AddActor(a_qlquad_actor)
renderer.AddActor(a_qlquad_contour_actor)
renderer.AddActor(a_tet_actor)
renderer.AddActor(a_tet_contour_actor)
renderer.AddActor(a_hex_actor)
renderer.AddActor(a_hex_contour_actor)
renderer.AddActor(a_tqhex_actor)
renderer.AddActor(a_tqhex_contour_actor)
renderer.AddActor(a_bqhex_actor)
renderer.AddActor(a_bqhex_contour_actor)
renderer.AddActor(a_wedge_actor)
renderer.AddActor(a_wedge_contour_actor)
renderer.AddActor(a_bqwedge_actor)
renderer.AddActor(a_bqwedge_contour_actor)
renderer.AddActor(a_qlwedge_actor)
renderer.AddActor(a_qlwedge_contour_actor)
renderer.AddActor(a_pyramid_actor)
renderer.AddActor(a_pyramid_contour_actor)
renderer.AddActor(a_tqpyramid_actor)
renderer.AddActor(a_tqpyramid_contour_actor)

# Position actors in grid layout
a_edge_contour_actor.AddPosition(0, 2, 0)
a_tri_actor.AddPosition(2, 0, 0)
a_tri_contour_actor.AddPosition(2, 2, 0)
a_quad_actor.AddPosition(4, 0, 0)
a_bquad_actor.AddPosition(4, 0, 2)
a_qlquad_actor.AddPosition(4, 0, 4)
a_quad_contour_actor.AddPosition(4, 2, 0)
a_bquad_contour_actor.AddPosition(4, 2, 2)
a_qlquad_contour_actor.AddPosition(4, 2, 4)
a_tet_actor.AddPosition(6, 0, 0)
a_tet_contour_actor.AddPosition(6, 2, 0)
a_hex_actor.AddPosition(8, 0, 0)
a_tqhex_actor.AddPosition(8, 0, 2)
a_bqhex_actor.AddPosition(8, 0, 4)
a_hex_contour_actor.AddPosition(8, 2, 0)
a_tqhex_contour_actor.AddPosition(8, 2, 2)
a_bqhex_contour_actor.AddPosition(8, 2, 4)
a_wedge_actor.AddPosition(10, 0, 0)
a_qlwedge_actor.AddPosition(10, 0, 2)
a_bqwedge_actor.AddPosition(10, 0, 4)
a_wedge_contour_actor.AddPosition(10, 2, 0)
a_qlwedge_contour_actor.AddPosition(10, 2, 2)
a_bqwedge_contour_actor.AddPosition(10, 2, 4)
a_pyramid_actor.AddPosition(12, 0, 0)
a_tqpyramid_actor.AddPosition(12, 0, 2)
a_pyramid_contour_actor.AddPosition(12, 2, 0)
a_tqpyramid_contour_actor.AddPosition(12, 2, 2)

# Backdrop: base plane
base_plane = vtkCubeSource()
base_plane.SetCenter(7.0, -1, 2.5)
base_plane.SetXLength(16)
base_plane.SetYLength(0.1)
base_plane.SetZLength(7)
base_mapper = vtkPolyDataMapper()
base_mapper.SetInputConnection(base_plane.GetOutputPort())
base_actor = vtkActor()
base_actor.SetMapper(base_mapper)
base_actor.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)
renderer.AddActor(base_actor)

# Backdrop: back plane
back_plane = vtkCubeSource()
back_plane.SetCenter(7.0, 1.5, -1)
back_plane.SetXLength(16)
back_plane.SetYLength(5)
back_plane.SetZLength(0.1)
back_mapper = vtkPolyDataMapper()
back_mapper.SetInputConnection(back_plane.GetOutputPort())
back_actor = vtkActor()
back_actor.SetMapper(back_mapper)
back_actor.GetProperty().SetDiffuseColor(0.2, 0.2, 0.2)
renderer.AddActor(back_actor)

# Backdrop: left plane
left_plane = vtkCubeSource()
left_plane.SetCenter(-1, 1.5, 2.5)
left_plane.SetXLength(0.1)
left_plane.SetYLength(5)
left_plane.SetZLength(7)
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
render_window.SetWindowName("contour quadratic cells")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(2.5)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
