#!/usr/bin/env python

# Demonstrate vtkExtractEdges on various quadratic cell types including
# triangles, quads, tetrahedra, hexahedra, wedges, and pyramids with
# shrink filter visualization.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
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
from vtkmodules.vtkFiltersCore import (
    vtkAppendFilter,
    vtkExtractEdges,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.util.numpy_support import numpy_to_vtk as ntov

# Quadratic triangle
tri_points = vtkPoints()
tri_points.SetNumberOfPoints(6)
tri_points.SetData(ntov(np.array([
    [2.0, 0.0, 0.0], [3.0, 0.0, 0.0], [2.5, 0.8, 0.0],
    [2.5, 0.0, 0.0], [2.75, 0.4, 0.0], [2.25, 0.4, 0.0]])))
tri_scalars = vtkFloatArray()
tri_scalars.SetNumberOfTuples(6)
for i, v in enumerate([0.0, 0.0, 0.0, 1.0, 1.0, 0.0]):
    tri_scalars.InsertValue(i, v)
quadratic_triangle = vtkQuadraticTriangle()
for i in range(quadratic_triangle.GetNumberOfPoints()):
    quadratic_triangle.GetPointIds().SetId(i, i)
a_tri_grid = vtkUnstructuredGrid()
a_tri_grid.Allocate(1, 1)
a_tri_grid.InsertNextCell(quadratic_triangle.GetCellType(), quadratic_triangle.GetPointIds())
a_tri_grid.SetPoints(tri_points)
a_tri_grid.GetPointData().SetScalars(tri_scalars)

# Quadratic quadrilateral
quad_points = vtkPoints()
quad_points.SetNumberOfPoints(8)
quad_points.SetData(ntov(np.array([
    [4.0, 0.0, 0.0], [5.0, 0.0, 0.0], [5.0, 1.0, 0.0], [4.0, 1.0, 0.0],
    [4.5, 0.0, 0.0], [5.0, 0.5, 0.0], [4.5, 1.0, 0.0], [4.0, 0.5, 0.0]])))
quad_scalars = vtkFloatArray()
quad_scalars.SetNumberOfTuples(8)
for i, v in enumerate([0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0]):
    quad_scalars.InsertValue(i, v)
quadratic_quad = vtkQuadraticQuad()
for i in range(quadratic_quad.GetNumberOfPoints()):
    quadratic_quad.GetPointIds().SetId(i, i)
a_quad_grid = vtkUnstructuredGrid()
a_quad_grid.Allocate(1, 1)
a_quad_grid.InsertNextCell(quadratic_quad.GetCellType(), quadratic_quad.GetPointIds())
a_quad_grid.SetPoints(quad_points)
a_quad_grid.GetPointData().SetScalars(quad_scalars)

# BiQuadratic quadrilateral
bquad_points = vtkPoints()
bquad_points.SetNumberOfPoints(9)
bquad_points.SetData(ntov(np.array([
    [4.0, 2.0, 0.0], [5.0, 2.0, 0.0], [5.0, 3.0, 0.0], [4.0, 3.0, 0.0],
    [4.5, 2.0, 0.0], [5.0, 2.5, 0.0], [4.5, 3.0, 0.0], [4.0, 2.5, 0.0],
    [4.5, 2.5, 0.0]])))
bquad_scalars = vtkFloatArray()
bquad_scalars.SetNumberOfTuples(9)
for i, v in enumerate([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
    bquad_scalars.InsertValue(i, v)
biquadratic_quad = vtkBiQuadraticQuad()
for i in range(biquadratic_quad.GetNumberOfPoints()):
    biquadratic_quad.GetPointIds().SetId(i, i)
b_quad_grid = vtkUnstructuredGrid()
b_quad_grid.Allocate(1, 1)
b_quad_grid.InsertNextCell(biquadratic_quad.GetCellType(), biquadratic_quad.GetPointIds())
b_quad_grid.SetPoints(bquad_points)
b_quad_grid.GetPointData().SetScalars(bquad_scalars)

# Quadratic linear quadrilateral
ql_quad_points = vtkPoints()
ql_quad_points.SetNumberOfPoints(6)
ql_quad_points.SetData(ntov(np.array([
    [4.0, 4.0, 0.0], [5.0, 4.0, 0.0], [5.0, 5.0, 0.0], [4.0, 5.0, 0.0],
    [4.5, 4.0, 0.0], [4.5, 5.0, 0.0]])))
ql_quad_scalars = vtkFloatArray()
ql_quad_scalars.SetNumberOfTuples(6)
for i, v in enumerate([1.0, 1.0, 1.0, 1.0, 0.0, 0.0]):
    ql_quad_scalars.InsertValue(i, v)
ql_quad = vtkQuadraticLinearQuad()
for i in range(ql_quad.GetNumberOfPoints()):
    ql_quad.GetPointIds().SetId(i, i)
ql_quad_grid = vtkUnstructuredGrid()
ql_quad_grid.Allocate(1, 1)
ql_quad_grid.InsertNextCell(ql_quad.GetCellType(), ql_quad.GetPointIds())
ql_quad_grid.SetPoints(ql_quad_points)
ql_quad_grid.GetPointData().SetScalars(ql_quad_scalars)

# Quadratic tetrahedron
tet_points = vtkPoints()
tet_points.SetNumberOfPoints(10)
tet_points.SetData(ntov(np.array([
    [6.0, 0.0, 0.0], [7.0, 0.0, 0.0], [6.5, 0.8, 0.0], [6.5, 0.4, 1.0],
    [6.5, 0.0, 0.0], [6.75, 0.4, 0.0], [6.25, 0.4, 0.0],
    [6.25, 0.2, 0.5], [6.75, 0.2, 0.5], [6.50, 0.6, 0.5]])))
tet_scalars = vtkFloatArray()
tet_scalars.SetNumberOfTuples(10)
for i, v in enumerate([1.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]):
    tet_scalars.InsertValue(i, v)
quadratic_tetra = vtkQuadraticTetra()
for i in range(quadratic_tetra.GetNumberOfPoints()):
    quadratic_tetra.GetPointIds().SetId(i, i)
a_tet_grid = vtkUnstructuredGrid()
a_tet_grid.Allocate(1, 1)
a_tet_grid.InsertNextCell(quadratic_tetra.GetCellType(), quadratic_tetra.GetPointIds())
a_tet_grid.SetPoints(tet_points)
a_tet_grid.GetPointData().SetScalars(tet_scalars)

# Quadratic hexahedron
hex_points = vtkPoints()
hex_points.SetNumberOfPoints(20)
hex_points.SetData(ntov(np.array([
    [8, 0, 0], [9, 0, 0], [9, 1, 0], [8, 1, 0],
    [8, 0, 1], [9, 0, 1], [9, 1, 1], [8, 1, 1],
    [8.5, 0, 0], [9, 0.5, 0], [8.5, 1, 0], [8, 0.5, 0],
    [8.5, 0, 1], [9, 0.5, 1], [8.5, 1, 1], [8, 0.5, 1],
    [8, 0, 0.5], [9, 0, 0.5], [9, 1, 0.5], [8, 1, 0.5]])))
hex_scalars = vtkFloatArray()
hex_scalars.SetNumberOfTuples(20)
for i in range(20):
    hex_scalars.InsertValue(i, 1.0 if i < 8 else 0.0)
quadratic_hex = vtkQuadraticHexahedron()
for i in range(quadratic_hex.GetNumberOfPoints()):
    quadratic_hex.GetPointIds().SetId(i, i)
a_hex_grid = vtkUnstructuredGrid()
a_hex_grid.Allocate(1, 1)
a_hex_grid.InsertNextCell(quadratic_hex.GetCellType(), quadratic_hex.GetPointIds())
a_hex_grid.SetPoints(hex_points)
a_hex_grid.GetPointData().SetScalars(hex_scalars)

# TriQuadratic hexahedron
tq_hex_points = vtkPoints()
tq_hex_points.SetNumberOfPoints(27)
tq_hex_points.SetData(ntov(np.array([
    [8, 2, 0], [9, 2, 0], [9, 3, 0], [8, 3, 0],
    [8, 2, 1], [9, 2, 1], [9, 3, 1], [8, 3, 1],
    [8.5, 2, 0], [9, 2.5, 0], [8.5, 3, 0], [8, 2.5, 0],
    [8.5, 2, 1], [9, 2.5, 1], [8.5, 3, 1], [8, 2.5, 1],
    [8, 2, 0.5], [9, 2, 0.5], [9, 3, 0.5], [8, 3, 0.5],
    [8, 2.5, 0.5], [9, 2.5, 0.5], [8.5, 2, 0.5], [8.5, 3, 0.5],
    [8.5, 2.5, 0.0], [8.5, 2.5, 1], [8.5, 2.5, 0.5]])))
tq_hex_scalars = vtkFloatArray()
tq_hex_scalars.SetNumberOfTuples(27)
for i in range(27):
    tq_hex_scalars.InsertValue(i, 1.0 if i < 8 else 0.0)
tq_hex = vtkTriQuadraticHexahedron()
for i in range(tq_hex.GetNumberOfPoints()):
    tq_hex.GetPointIds().SetId(i, i)
tq_hex_grid = vtkUnstructuredGrid()
tq_hex_grid.Allocate(1, 1)
tq_hex_grid.InsertNextCell(tq_hex.GetCellType(), tq_hex.GetPointIds())
tq_hex_grid.SetPoints(tq_hex_points)
tq_hex_grid.GetPointData().SetScalars(tq_hex_scalars)

# BiQuadratic Quadratic hexahedron
bq_hex_points = vtkPoints()
bq_hex_points.SetNumberOfPoints(24)
bq_hex_points.SetData(ntov(np.array([
    [8, 4, 0], [9, 4, 0], [9, 5, 0], [8, 5, 0],
    [8, 4, 1], [9, 4, 1], [9, 5, 1], [8, 5, 1],
    [8.5, 4, 0], [9, 4.5, 0], [8.5, 5, 0], [8, 4.5, 0],
    [8.5, 4, 1], [9, 4.5, 1], [8.5, 5, 1], [8, 4.5, 1],
    [8, 4, 0.5], [9, 4, 0.5], [9, 5, 0.5], [8, 5, 0.5],
    [8, 4.5, 0.5], [9, 4.5, 0.5], [8.5, 4, 0.5], [8.5, 5, 0.5]])))
bq_hex_scalars = vtkFloatArray()
bq_hex_scalars.SetNumberOfTuples(24)
for i in range(24):
    bq_hex_scalars.InsertValue(i, 1.0 if i < 8 else 0.0)
bq_hex = vtkBiQuadraticQuadraticHexahedron()
for i in range(bq_hex.GetNumberOfPoints()):
    bq_hex.GetPointIds().SetId(i, i)
bq_hex_grid = vtkUnstructuredGrid()
bq_hex_grid.Allocate(1, 1)
bq_hex_grid.InsertNextCell(bq_hex.GetCellType(), bq_hex.GetPointIds())
bq_hex_grid.SetPoints(bq_hex_points)
bq_hex_grid.GetPointData().SetScalars(bq_hex_scalars)

# Quadratic wedge
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(15)
wedge_points.SetData(ntov(np.array([
    [10, 0, 0], [11, 0, 0], [10, 1, 0], [10, 0, 1], [11, 0, 1], [10, 1, 1],
    [10.5, 0, 0], [10.5, 0.5, 0], [10, 0.5, 0],
    [10.5, 0, 1], [10.5, 0.5, 1], [10, 0.5, 1],
    [10, 0, 0.5], [11, 0, 0.5], [10, 1, 0.5]])))
wedge_scalars = vtkFloatArray()
wedge_scalars.SetNumberOfTuples(15)
for i in range(15):
    wedge_scalars.InsertValue(i, 1.0 if i < 6 else 0.0)
quadratic_wedge = vtkQuadraticWedge()
for i in range(quadratic_wedge.GetNumberOfPoints()):
    quadratic_wedge.GetPointIds().SetId(i, i)
a_wedge_grid = vtkUnstructuredGrid()
a_wedge_grid.Allocate(1, 1)
a_wedge_grid.InsertNextCell(quadratic_wedge.GetCellType(), quadratic_wedge.GetPointIds())
a_wedge_grid.SetPoints(wedge_points)
a_wedge_grid.GetPointData().SetScalars(wedge_scalars)

# Quadratic linear wedge
ql_wedge_points = vtkPoints()
ql_wedge_points.SetNumberOfPoints(12)
ql_wedge_points.SetData(ntov(np.array([
    [10, 4, 0], [11, 4, 0], [10, 5, 0], [10, 4, 1], [11, 4, 1], [10, 5, 1],
    [10.5, 4, 0], [10.5, 4.5, 0], [10, 4.5, 0],
    [10.5, 4, 1], [10.5, 4.5, 1], [10, 4.5, 1]])))
ql_wedge_scalars = vtkFloatArray()
ql_wedge_scalars.SetNumberOfTuples(12)
for i in range(12):
    ql_wedge_scalars.InsertValue(i, 1.0 if i < 6 else 0.0)
ql_wedge = vtkQuadraticLinearWedge()
for i in range(ql_wedge.GetNumberOfPoints()):
    ql_wedge.GetPointIds().SetId(i, i)
ql_wedge_grid = vtkUnstructuredGrid()
ql_wedge_grid.Allocate(1, 1)
ql_wedge_grid.InsertNextCell(ql_wedge.GetCellType(), ql_wedge.GetPointIds())
ql_wedge_grid.SetPoints(ql_wedge_points)
ql_wedge_grid.GetPointData().SetScalars(ql_wedge_scalars)

# BiQuadratic wedge
bq_wedge_points = vtkPoints()
bq_wedge_points.SetNumberOfPoints(18)
bq_wedge_points.SetData(ntov(np.array([
    [10, 2, 0], [11, 2, 0], [10, 3, 0], [10, 2, 1], [11, 2, 1], [10, 3, 1],
    [10.5, 2, 0], [10.5, 2.5, 0], [10, 2.5, 0],
    [10.5, 2, 1], [10.5, 2.5, 1], [10, 2.5, 1],
    [10, 2, 0.5], [11, 2, 0.5], [10, 3, 0.5],
    [10.5, 2, 0.5], [10.5, 2.5, 0.5], [10, 2.5, 0.5]])))
bq_wedge_scalars = vtkFloatArray()
bq_wedge_scalars.SetNumberOfTuples(18)
for i in range(18):
    bq_wedge_scalars.InsertValue(i, 1.0 if i < 6 else 0.0)
bq_wedge = vtkBiQuadraticQuadraticWedge()
for i in range(bq_wedge.GetNumberOfPoints()):
    bq_wedge.GetPointIds().SetId(i, i)
bq_wedge_grid = vtkUnstructuredGrid()
bq_wedge_grid.Allocate(1, 1)
bq_wedge_grid.InsertNextCell(bq_wedge.GetCellType(), bq_wedge.GetPointIds())
bq_wedge_grid.SetPoints(bq_wedge_points)
bq_wedge_grid.GetPointData().SetScalars(bq_wedge_scalars)

# Quadratic pyramid
pyra_points = vtkPoints()
pyra_points.SetNumberOfPoints(13)
pyra_points.SetData(ntov(np.array([
    [12, 0, 0], [13, 0, 0], [13, 1, 0], [12, 1, 0], [12, 0, 1],
    [12.5, 0, 0], [13, 0.5, 0], [12.5, 1, 0], [12, 0.5, 0],
    [12, 0, 0.5], [12.5, 0, 0.5], [12.5, 0.5, 0.5], [12, 0.5, 0.5]])))
pyra_scalars = vtkFloatArray()
pyra_scalars.SetNumberOfTuples(13)
for i in range(13):
    pyra_scalars.InsertValue(i, 1.0 if i < 6 else 0.0)
quadratic_pyramid = vtkQuadraticPyramid()
for i in range(quadratic_pyramid.GetNumberOfPoints()):
    quadratic_pyramid.GetPointIds().SetId(i, i)
a_pyramid_grid = vtkUnstructuredGrid()
a_pyramid_grid.Allocate(1, 1)
a_pyramid_grid.InsertNextCell(quadratic_pyramid.GetCellType(), quadratic_pyramid.GetPointIds())
a_pyramid_grid.SetPoints(pyra_points)
a_pyramid_grid.GetPointData().SetScalars(pyra_scalars)

# TriQuadratic pyramid
tq_pyra_points = vtkPoints()
tq_pyra_points.SetNumberOfPoints(19)
tq_pyra_points.SetData(ntov(np.array([
    [12, 2, 0], [13, 2, 0], [13, 3, 0], [12, 3, 0], [12, 2, 1],
    [12.5, 2, 0], [13, 2.5, 0], [12.5, 3, 0], [12, 2.5, 0],
    [12, 2, 0.5], [12.5, 2, 0.5], [12.5, 2.5, 0.5], [12, 2.5, 0.5],
    [12.5, 2.5, 0],
    [12 + 1.0 / 3.0, 2, 1.0 / 3.0],
    [12 + 2.0 / 3.0, 2 + 1.0 / 3.0, 1.0 / 3.0],
    [12 + 1.0 / 3.0, 2 + 2.0 / 3.0, 1.0 / 3.0],
    [12, 2 + 1.0 / 3.0, 1.0 / 3.0],
    [12 + 0.4, 2 + 0.4, 0.2]])))
tq_pyra_scalars = vtkFloatArray()
tq_pyra_scalars.SetNumberOfTuples(19)
for i in range(19):
    if i < 6 or i == 18:
        tq_pyra_scalars.InsertValue(i, 1.0)
    else:
        tq_pyra_scalars.InsertValue(i, 0.0)
triquadratic_pyramid = vtkTriQuadraticPyramid()
for i in range(triquadratic_pyramid.GetNumberOfPoints()):
    triquadratic_pyramid.GetPointIds().SetId(i, i)
a_tq_pyramid_grid = vtkUnstructuredGrid()
a_tq_pyramid_grid.Allocate(1, 1)
a_tq_pyramid_grid.InsertNextCell(triquadratic_pyramid.GetCellType(), triquadratic_pyramid.GetPointIds())
a_tq_pyramid_grid.SetPoints(tq_pyra_points)
a_tq_pyramid_grid.GetPointData().SetScalars(tq_pyra_scalars)

# Append all quadratic cells together
append_filter = vtkAppendFilter()
append_filter.AddInputData(b_quad_grid)
append_filter.AddInputData(ql_quad_grid)
append_filter.AddInputData(ql_wedge_grid)
append_filter.AddInputData(a_tri_grid)
append_filter.AddInputData(a_quad_grid)
append_filter.AddInputData(a_tet_grid)
append_filter.AddInputData(a_hex_grid)
append_filter.AddInputData(tq_hex_grid)
append_filter.AddInputData(bq_hex_grid)
append_filter.AddInputData(a_wedge_grid)
append_filter.AddInputData(bq_wedge_grid)
append_filter.AddInputData(a_pyramid_grid)
append_filter.AddInputData(a_tq_pyramid_grid)

# Extract edges
extract = vtkExtractEdges()
extract.SetInputConnection(append_filter.GetOutputPort())

shrink = vtkShrinkPolyData()
shrink.SetInputConnection(extract.GetOutputPort())
shrink.SetShrinkFactor(0.90)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.3)
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 200)
render_window.SetWindowName("extract edges quadratic cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(2.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
