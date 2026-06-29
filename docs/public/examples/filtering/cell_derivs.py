#!/usr/bin/env python

# Demonstrate vtkCellDerivatives for all linear cell types with hedgehog
# glyphs showing the computed gradient at cell centers.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkHexagonalPrism,
    vtkHexahedron,
    vtkLine,
    vtkPentagonalPrism,
    vtkPixel,
    vtkPolyLine,
    vtkPolyVertex,
    vtkPolygon,
    vtkPyramid,
    vtkQuad,
    vtkTetra,
    vtkTriangle,
    vtkTriangleStrip,
    vtkUnstructuredGrid,
    vtkVertex,
    vtkVoxel,
    vtkWedge,
)
from vtkmodules.vtkFiltersCore import (
    vtkCellCenters,
    vtkHedgeHog,
)
from vtkmodules.vtkFiltersGeneral import vtkCellDerivatives
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Voxel ---
voxel_points = vtkPoints()
voxel_points.SetNumberOfPoints(8)
voxel_points.InsertPoint(0, 0, 0, 0)
voxel_points.InsertPoint(1, 1, 0, 0)
voxel_points.InsertPoint(2, 0, 1, 0)
voxel_points.InsertPoint(3, 1, 1, 0)
voxel_points.InsertPoint(4, 0, 0, 1)
voxel_points.InsertPoint(5, 1, 0, 1)
voxel_points.InsertPoint(6, 0, 1, 1)
voxel_points.InsertPoint(7, 1, 1, 1)

voxel_cell = vtkVoxel()
for i in range(8):
    voxel_cell.GetPointIds().SetId(i, i)

voxel_grid = vtkUnstructuredGrid()
voxel_grid.Allocate(1, 1)
voxel_grid.InsertNextCell(voxel_cell.GetCellType(), voxel_cell.GetPointIds())
voxel_grid.SetPoints(voxel_points)

voxel_mapper = vtkDataSetMapper()
voxel_mapper.SetInputData(voxel_grid)

voxel_actor = vtkActor()
voxel_actor.SetMapper(voxel_mapper)
voxel_actor.GetProperty().BackfaceCullingOn()

# --- Hexahedron ---
hexahedron_points = vtkPoints()
hexahedron_points.SetNumberOfPoints(8)
hexahedron_points.InsertPoint(0, 0, 0, 0)
hexahedron_points.InsertPoint(1, 1, 0, 0)
hexahedron_points.InsertPoint(2, 1, 1, 0)
hexahedron_points.InsertPoint(3, 0, 1, 0)
hexahedron_points.InsertPoint(4, 0, 0, 1)
hexahedron_points.InsertPoint(5, 1, 0, 1)
hexahedron_points.InsertPoint(6, 1, 1, 1)
hexahedron_points.InsertPoint(7, 0, 1, 1)

hexahedron_cell = vtkHexahedron()
for i in range(8):
    hexahedron_cell.GetPointIds().SetId(i, i)

hexahedron_grid = vtkUnstructuredGrid()
hexahedron_grid.Allocate(1, 1)
hexahedron_grid.InsertNextCell(hexahedron_cell.GetCellType(), hexahedron_cell.GetPointIds())
hexahedron_grid.SetPoints(hexahedron_points)

hexahedron_mapper = vtkDataSetMapper()
hexahedron_mapper.SetInputData(hexahedron_grid)

hexahedron_actor = vtkActor()
hexahedron_actor.SetMapper(hexahedron_mapper)
hexahedron_actor.AddPosition(2, 0, 0)
hexahedron_actor.GetProperty().BackfaceCullingOn()

# --- Tetra ---
tetra_points = vtkPoints()
tetra_points.SetNumberOfPoints(4)
tetra_points.InsertPoint(0, 0, 0, 0)
tetra_points.InsertPoint(1, 1, 0, 0)
tetra_points.InsertPoint(2, 0, 1, 0)
tetra_points.InsertPoint(3, 1, 1, 1)

tetra_cell = vtkTetra()
for i in range(4):
    tetra_cell.GetPointIds().SetId(i, i)

tetra_grid = vtkUnstructuredGrid()
tetra_grid.Allocate(1, 1)
tetra_grid.InsertNextCell(tetra_cell.GetCellType(), tetra_cell.GetPointIds())
tetra_grid.SetPoints(tetra_points)

tetra_mapper = vtkDataSetMapper()
tetra_mapper.SetInputData(tetra_grid)

tetra_actor = vtkActor()
tetra_actor.SetMapper(tetra_mapper)
tetra_actor.AddPosition(4, 0, 0)
tetra_actor.GetProperty().BackfaceCullingOn()

# --- Wedge ---
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(6)
wedge_points.InsertPoint(0, 0, 1, 0)
wedge_points.InsertPoint(1, 0, 0, 0)
wedge_points.InsertPoint(2, 0, 0.5, 0.5)
wedge_points.InsertPoint(3, 1, 1, 0)
wedge_points.InsertPoint(4, 1, 0, 0)
wedge_points.InsertPoint(5, 1, 0.5, 0.5)

wedge_cell = vtkWedge()
for i in range(6):
    wedge_cell.GetPointIds().SetId(i, i)

wedge_grid = vtkUnstructuredGrid()
wedge_grid.Allocate(1, 1)
wedge_grid.InsertNextCell(wedge_cell.GetCellType(), wedge_cell.GetPointIds())
wedge_grid.SetPoints(wedge_points)

wedge_mapper = vtkDataSetMapper()
wedge_mapper.SetInputData(wedge_grid)

wedge_actor = vtkActor()
wedge_actor.SetMapper(wedge_mapper)
wedge_actor.AddPosition(6, 0, 0)
wedge_actor.GetProperty().BackfaceCullingOn()

# --- Pyramid ---
pyramid_points = vtkPoints()
pyramid_points.SetNumberOfPoints(5)
pyramid_points.InsertPoint(0, 0, 0, 0)
pyramid_points.InsertPoint(1, 1, 0, 0)
pyramid_points.InsertPoint(2, 1, 1, 0)
pyramid_points.InsertPoint(3, 0, 1, 0)
pyramid_points.InsertPoint(4, 0.5, 0.5, 1)

pyramid_cell = vtkPyramid()
for i in range(5):
    pyramid_cell.GetPointIds().SetId(i, i)

pyramid_grid = vtkUnstructuredGrid()
pyramid_grid.Allocate(1, 1)
pyramid_grid.InsertNextCell(pyramid_cell.GetCellType(), pyramid_cell.GetPointIds())
pyramid_grid.SetPoints(pyramid_points)

pyramid_mapper = vtkDataSetMapper()
pyramid_mapper.SetInputData(pyramid_grid)

pyramid_actor = vtkActor()
pyramid_actor.SetMapper(pyramid_mapper)
pyramid_actor.AddPosition(8, 0, 0)
pyramid_actor.GetProperty().BackfaceCullingOn()

# --- Pixel ---
pixel_points = vtkPoints()
pixel_points.SetNumberOfPoints(4)
pixel_points.InsertPoint(0, 0, 0, 0)
pixel_points.InsertPoint(1, 1, 0, 0)
pixel_points.InsertPoint(2, 0, 1, 0)
pixel_points.InsertPoint(3, 1, 1, 0)

pixel_cell = vtkPixel()
for i in range(4):
    pixel_cell.GetPointIds().SetId(i, i)

pixel_grid = vtkUnstructuredGrid()
pixel_grid.Allocate(1, 1)
pixel_grid.InsertNextCell(pixel_cell.GetCellType(), pixel_cell.GetPointIds())
pixel_grid.SetPoints(pixel_points)

pixel_mapper = vtkDataSetMapper()
pixel_mapper.SetInputData(pixel_grid)

pixel_actor = vtkActor()
pixel_actor.SetMapper(pixel_mapper)
pixel_actor.AddPosition(0, 0, 2)
pixel_actor.GetProperty().BackfaceCullingOn()

# --- Quad ---
quad_points = vtkPoints()
quad_points.SetNumberOfPoints(4)
quad_points.InsertPoint(0, 0, 0, 0)
quad_points.InsertPoint(1, 1, 0, 0)
quad_points.InsertPoint(2, 1, 1, 0)
quad_points.InsertPoint(3, 0, 1, 0)

quad_cell = vtkQuad()
for i in range(4):
    quad_cell.GetPointIds().SetId(i, i)

quad_grid = vtkUnstructuredGrid()
quad_grid.Allocate(1, 1)
quad_grid.InsertNextCell(quad_cell.GetCellType(), quad_cell.GetPointIds())
quad_grid.SetPoints(quad_points)

quad_mapper = vtkDataSetMapper()
quad_mapper.SetInputData(quad_grid)

quad_actor = vtkActor()
quad_actor.SetMapper(quad_mapper)
quad_actor.AddPosition(2, 0, 2)
quad_actor.GetProperty().BackfaceCullingOn()

# --- Triangle ---
triangle_points = vtkPoints()
triangle_points.SetNumberOfPoints(3)
triangle_points.InsertPoint(0, 0, 0, 0)
triangle_points.InsertPoint(1, 1, 0, 0)
triangle_points.InsertPoint(2, 0.5, 0.5, 0)

triangle_tcoords = vtkFloatArray()
triangle_tcoords.SetNumberOfComponents(2)
triangle_tcoords.SetNumberOfTuples(3)
triangle_tcoords.InsertTuple2(0, 1, 1)
triangle_tcoords.InsertTuple2(1, 2, 2)
triangle_tcoords.InsertTuple2(2, 3, 3)

triangle_cell = vtkTriangle()
for i in range(3):
    triangle_cell.GetPointIds().SetId(i, i)

triangle_grid = vtkUnstructuredGrid()
triangle_grid.Allocate(1, 1)
triangle_grid.InsertNextCell(triangle_cell.GetCellType(), triangle_cell.GetPointIds())
triangle_grid.SetPoints(triangle_points)
triangle_grid.GetPointData().SetTCoords(triangle_tcoords)

triangle_mapper = vtkDataSetMapper()
triangle_mapper.SetInputData(triangle_grid)

triangle_actor = vtkActor()
triangle_actor.SetMapper(triangle_mapper)
triangle_actor.AddPosition(4, 0, 2)
triangle_actor.GetProperty().BackfaceCullingOn()

# --- Polygon ---
polygon_points = vtkPoints()
polygon_points.SetNumberOfPoints(4)
polygon_points.InsertPoint(0, 0, 0, 0)
polygon_points.InsertPoint(1, 1, 0, 0)
polygon_points.InsertPoint(2, 1, 1, 0)
polygon_points.InsertPoint(3, 0, 1, 0)

polygon_cell = vtkPolygon()
polygon_cell.GetPointIds().SetNumberOfIds(4)
for i in range(4):
    polygon_cell.GetPointIds().SetId(i, i)

polygon_grid = vtkUnstructuredGrid()
polygon_grid.Allocate(1, 1)
polygon_grid.InsertNextCell(polygon_cell.GetCellType(), polygon_cell.GetPointIds())
polygon_grid.SetPoints(polygon_points)

polygon_mapper = vtkDataSetMapper()
polygon_mapper.SetInputData(polygon_grid)

polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)
polygon_actor.AddPosition(6, 0, 2)
polygon_actor.GetProperty().BackfaceCullingOn()

# --- Triangle Strip ---
triangle_strip_points = vtkPoints()
triangle_strip_points.SetNumberOfPoints(5)
triangle_strip_points.InsertPoint(0, 0, 1, 0)
triangle_strip_points.InsertPoint(1, 0, 0, 0)
triangle_strip_points.InsertPoint(2, 1, 1, 0)
triangle_strip_points.InsertPoint(3, 1, 0, 0)
triangle_strip_points.InsertPoint(4, 2, 1, 0)

triangle_strip_tcoords = vtkFloatArray()
triangle_strip_tcoords.SetNumberOfComponents(2)
triangle_strip_tcoords.SetNumberOfTuples(3)
triangle_strip_tcoords.InsertTuple2(0, 1, 1)
triangle_strip_tcoords.InsertTuple2(1, 2, 2)
triangle_strip_tcoords.InsertTuple2(2, 3, 3)
triangle_strip_tcoords.InsertTuple2(3, 4, 4)
triangle_strip_tcoords.InsertTuple2(4, 5, 5)

triangle_strip_cell = vtkTriangleStrip()
triangle_strip_cell.GetPointIds().SetNumberOfIds(5)
for i in range(5):
    triangle_strip_cell.GetPointIds().SetId(i, i)

triangle_strip_grid = vtkUnstructuredGrid()
triangle_strip_grid.Allocate(1, 1)
triangle_strip_grid.InsertNextCell(triangle_strip_cell.GetCellType(), triangle_strip_cell.GetPointIds())
triangle_strip_grid.SetPoints(triangle_strip_points)
triangle_strip_grid.GetPointData().SetTCoords(triangle_strip_tcoords)

triangle_strip_mapper = vtkDataSetMapper()
triangle_strip_mapper.SetInputData(triangle_strip_grid)

triangle_strip_actor = vtkActor()
triangle_strip_actor.SetMapper(triangle_strip_mapper)
triangle_strip_actor.AddPosition(8, 0, 2)
triangle_strip_actor.GetProperty().BackfaceCullingOn()

# --- Line ---
line_points = vtkPoints()
line_points.SetNumberOfPoints(2)
line_points.InsertPoint(0, 0, 0, 0)
line_points.InsertPoint(1, 1, 1, 0)

line_cell = vtkLine()
line_cell.GetPointIds().SetId(0, 0)
line_cell.GetPointIds().SetId(1, 1)

line_grid = vtkUnstructuredGrid()
line_grid.Allocate(1, 1)
line_grid.InsertNextCell(line_cell.GetCellType(), line_cell.GetPointIds())
line_grid.SetPoints(line_points)

line_mapper = vtkDataSetMapper()
line_mapper.SetInputData(line_grid)

line_actor = vtkActor()
line_actor.SetMapper(line_mapper)
line_actor.AddPosition(0, 0, 4)
line_actor.GetProperty().BackfaceCullingOn()

# --- PolyLine ---
poly_line_points = vtkPoints()
poly_line_points.SetNumberOfPoints(3)
poly_line_points.InsertPoint(0, 0, 0, 0)
poly_line_points.InsertPoint(1, 1, 1, 0)
poly_line_points.InsertPoint(2, 1, 0, 0)

poly_line_cell = vtkPolyLine()
poly_line_cell.GetPointIds().SetNumberOfIds(3)
for i in range(3):
    poly_line_cell.GetPointIds().SetId(i, i)

poly_line_grid = vtkUnstructuredGrid()
poly_line_grid.Allocate(1, 1)
poly_line_grid.InsertNextCell(poly_line_cell.GetCellType(), poly_line_cell.GetPointIds())
poly_line_grid.SetPoints(poly_line_points)

poly_line_mapper = vtkDataSetMapper()
poly_line_mapper.SetInputData(poly_line_grid)

poly_line_actor = vtkActor()
poly_line_actor.SetMapper(poly_line_mapper)
poly_line_actor.AddPosition(2, 0, 4)
poly_line_actor.GetProperty().BackfaceCullingOn()

# --- Vertex ---
vertex_points = vtkPoints()
vertex_points.SetNumberOfPoints(1)
vertex_points.InsertPoint(0, 0, 0, 0)

vertex_cell = vtkVertex()
vertex_cell.GetPointIds().SetId(0, 0)

vertex_grid = vtkUnstructuredGrid()
vertex_grid.Allocate(1, 1)
vertex_grid.InsertNextCell(vertex_cell.GetCellType(), vertex_cell.GetPointIds())
vertex_grid.SetPoints(vertex_points)

vertex_mapper = vtkDataSetMapper()
vertex_mapper.SetInputData(vertex_grid)

vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.AddPosition(0, 0, 6)
vertex_actor.GetProperty().BackfaceCullingOn()

# --- PolyVertex ---
poly_vertex_points = vtkPoints()
poly_vertex_points.SetNumberOfPoints(3)
poly_vertex_points.InsertPoint(0, 0, 0, 0)
poly_vertex_points.InsertPoint(1, 1, 0, 0)
poly_vertex_points.InsertPoint(2, 1, 1, 0)

poly_vertex_cell = vtkPolyVertex()
poly_vertex_cell.GetPointIds().SetNumberOfIds(3)
for i in range(3):
    poly_vertex_cell.GetPointIds().SetId(i, i)

poly_vertex_grid = vtkUnstructuredGrid()
poly_vertex_grid.Allocate(1, 1)
poly_vertex_grid.InsertNextCell(poly_vertex_cell.GetCellType(), poly_vertex_cell.GetPointIds())
poly_vertex_grid.SetPoints(poly_vertex_points)

poly_vertex_mapper = vtkDataSetMapper()
poly_vertex_mapper.SetInputData(poly_vertex_grid)

poly_vertex_actor = vtkActor()
poly_vertex_actor.SetMapper(poly_vertex_mapper)
poly_vertex_actor.AddPosition(2, 0, 6)
poly_vertex_actor.GetProperty().BackfaceCullingOn()

# --- Pentagonal Prism ---
penta_points = vtkPoints()
penta_points.SetNumberOfPoints(10)
penta_points.InsertPoint(0, 0.25, 0.0, 0.0)
penta_points.InsertPoint(1, 0.75, 0.0, 0.0)
penta_points.InsertPoint(2, 1.0, 0.5, 0.0)
penta_points.InsertPoint(3, 0.5, 1.0, 0.0)
penta_points.InsertPoint(4, 0.0, 0.5, 0.0)
penta_points.InsertPoint(5, 0.25, 0.0, 1.0)
penta_points.InsertPoint(6, 0.75, 0.0, 1.0)
penta_points.InsertPoint(7, 1.0, 0.5, 1.0)
penta_points.InsertPoint(8, 0.5, 1.0, 1.0)
penta_points.InsertPoint(9, 0.0, 0.5, 1.0)

penta_cell = vtkPentagonalPrism()
for i in range(10):
    penta_cell.GetPointIds().SetId(i, i)

penta_grid = vtkUnstructuredGrid()
penta_grid.Allocate(1, 1)
penta_grid.InsertNextCell(penta_cell.GetCellType(), penta_cell.GetPointIds())
penta_grid.SetPoints(penta_points)

penta_mapper = vtkDataSetMapper()
penta_mapper.SetInputData(penta_grid)

penta_actor = vtkActor()
penta_actor.SetMapper(penta_mapper)
penta_actor.AddPosition(10, 0, 0)
penta_actor.GetProperty().BackfaceCullingOn()

# --- Hexagonal Prism ---
hexa_points = vtkPoints()
hexa_points.SetNumberOfPoints(12)
hexa_points.InsertPoint(0, 0.0, 0.0, 0.0)
hexa_points.InsertPoint(1, 0.5, 0.0, 0.0)
hexa_points.InsertPoint(2, 1.0, 0.5, 0.0)
hexa_points.InsertPoint(3, 1.0, 1.0, 0.0)
hexa_points.InsertPoint(4, 0.5, 1.0, 0.0)
hexa_points.InsertPoint(5, 0.0, 0.5, 0.0)
hexa_points.InsertPoint(6, 0.0, 0.0, 1.0)
hexa_points.InsertPoint(7, 0.5, 0.0, 1.0)
hexa_points.InsertPoint(8, 1.0, 0.5, 1.0)
hexa_points.InsertPoint(9, 1.0, 1.0, 1.0)
hexa_points.InsertPoint(10, 0.5, 1.0, 1.0)
hexa_points.InsertPoint(11, 0.0, 0.5, 1.0)

hexa_cell = vtkHexagonalPrism()
for i in range(12):
    hexa_cell.GetPointIds().SetId(i, i)

hexa_grid = vtkUnstructuredGrid()
hexa_grid.Allocate(1, 1)
hexa_grid.InsertNextCell(hexa_cell.GetCellType(), hexa_cell.GetPointIds())
hexa_grid.SetPoints(hexa_points)

hexa_mapper = vtkDataSetMapper()
hexa_mapper.SetInputData(hexa_grid)

hexa_actor = vtkActor()
hexa_actor.SetMapper(hexa_mapper)
hexa_actor.AddPosition(12, 0, 0)
hexa_actor.GetProperty().BackfaceCullingOn()

# --- Set colors ---
voxel_actor.GetProperty().SetDiffuseColor(1, 0, 0)
hexahedron_actor.GetProperty().SetDiffuseColor(1, 1, 0)
tetra_actor.GetProperty().SetDiffuseColor(0, 1, 0)
wedge_actor.GetProperty().SetDiffuseColor(0, 1, 1)
pyramid_actor.GetProperty().SetDiffuseColor(1, 0, 1)
pixel_actor.GetProperty().SetDiffuseColor(0, 1, 1)
quad_actor.GetProperty().SetDiffuseColor(1, 0, 1)
triangle_actor.GetProperty().SetDiffuseColor(0.3, 1, 0.5)
polygon_actor.GetProperty().SetDiffuseColor(1, 0.4, 0.5)
triangle_strip_actor.GetProperty().SetDiffuseColor(0.3, 0.7, 1)
line_actor.GetProperty().SetDiffuseColor(0.2, 1, 1)
poly_line_actor.GetProperty().SetDiffuseColor(1, 1, 1)
vertex_actor.GetProperty().SetDiffuseColor(1, 1, 1)
poly_vertex_actor.GetProperty().SetDiffuseColor(1, 1, 1)
penta_actor.GetProperty().SetDiffuseColor(1, 1, 0)
hexa_actor.GetProperty().SetDiffuseColor(1, 1, 0)

# --- Compute derivatives and hedgehog glyphs for each cell type ---

# Set scalars on each grid.
scalar_voxel = vtkFloatArray()
scalar_voxel.SetNumberOfTuples(voxel_grid.GetNumberOfPoints())
scalar_voxel.SetNumberOfComponents(1)
scalar_voxel.Fill(0)
scalar_voxel.SetValue(0, 4)
voxel_grid.GetPointData().SetScalars(scalar_voxel)

scalar_hexahedron = vtkFloatArray()
scalar_hexahedron.SetNumberOfTuples(hexahedron_grid.GetNumberOfPoints())
scalar_hexahedron.SetNumberOfComponents(1)
scalar_hexahedron.Fill(0)
scalar_hexahedron.SetValue(0, 4)
hexahedron_grid.GetPointData().SetScalars(scalar_hexahedron)

scalar_wedge = vtkFloatArray()
scalar_wedge.SetNumberOfTuples(wedge_grid.GetNumberOfPoints())
scalar_wedge.SetNumberOfComponents(1)
scalar_wedge.Fill(0)
scalar_wedge.SetValue(0, 4)
wedge_grid.GetPointData().SetScalars(scalar_wedge)

scalar_pyramid = vtkFloatArray()
scalar_pyramid.SetNumberOfTuples(pyramid_grid.GetNumberOfPoints())
scalar_pyramid.SetNumberOfComponents(1)
scalar_pyramid.Fill(0)
scalar_pyramid.SetValue(0, 4)
pyramid_grid.GetPointData().SetScalars(scalar_pyramid)

scalar_tetra = vtkFloatArray()
scalar_tetra.SetNumberOfTuples(tetra_grid.GetNumberOfPoints())
scalar_tetra.SetNumberOfComponents(1)
scalar_tetra.Fill(0)
scalar_tetra.SetValue(0, 4)
tetra_grid.GetPointData().SetScalars(scalar_tetra)

scalar_quad = vtkFloatArray()
scalar_quad.SetNumberOfTuples(quad_grid.GetNumberOfPoints())
scalar_quad.SetNumberOfComponents(1)
scalar_quad.Fill(0)
scalar_quad.SetValue(0, 4)
quad_grid.GetPointData().SetScalars(scalar_quad)

scalar_triangle = vtkFloatArray()
scalar_triangle.SetNumberOfTuples(triangle_grid.GetNumberOfPoints())
scalar_triangle.SetNumberOfComponents(1)
scalar_triangle.Fill(0)
scalar_triangle.SetValue(0, 4)
triangle_grid.GetPointData().SetScalars(scalar_triangle)

scalar_triangle_strip = vtkFloatArray()
scalar_triangle_strip.SetNumberOfTuples(triangle_strip_grid.GetNumberOfPoints())
scalar_triangle_strip.SetNumberOfComponents(1)
scalar_triangle_strip.Fill(0)
scalar_triangle_strip.SetValue(0, 4)
triangle_strip_grid.GetPointData().SetScalars(scalar_triangle_strip)

scalar_line = vtkFloatArray()
scalar_line.SetNumberOfTuples(line_grid.GetNumberOfPoints())
scalar_line.SetNumberOfComponents(1)
scalar_line.Fill(0)
scalar_line.SetValue(0, 4)
line_grid.GetPointData().SetScalars(scalar_line)

scalar_poly_line = vtkFloatArray()
scalar_poly_line.SetNumberOfTuples(poly_line_grid.GetNumberOfPoints())
scalar_poly_line.SetNumberOfComponents(1)
scalar_poly_line.Fill(0)
scalar_poly_line.SetValue(0, 4)
poly_line_grid.GetPointData().SetScalars(scalar_poly_line)

scalar_vertex = vtkFloatArray()
scalar_vertex.SetNumberOfTuples(vertex_grid.GetNumberOfPoints())
scalar_vertex.SetNumberOfComponents(1)
scalar_vertex.Fill(0)
scalar_vertex.SetValue(0, 4)
vertex_grid.GetPointData().SetScalars(scalar_vertex)

scalar_poly_vertex = vtkFloatArray()
scalar_poly_vertex.SetNumberOfTuples(poly_vertex_grid.GetNumberOfPoints())
scalar_poly_vertex.SetNumberOfComponents(1)
scalar_poly_vertex.Fill(0)
scalar_poly_vertex.SetValue(0, 4)
poly_vertex_grid.GetPointData().SetScalars(scalar_poly_vertex)

scalar_pixel = vtkFloatArray()
scalar_pixel.SetNumberOfTuples(pixel_grid.GetNumberOfPoints())
scalar_pixel.SetNumberOfComponents(1)
scalar_pixel.Fill(0)
scalar_pixel.SetValue(0, 4)
pixel_grid.GetPointData().SetScalars(scalar_pixel)

scalar_polygon = vtkFloatArray()
scalar_polygon.SetNumberOfTuples(polygon_grid.GetNumberOfPoints())
scalar_polygon.SetNumberOfComponents(1)
scalar_polygon.Fill(0)
scalar_polygon.SetValue(0, 4)
polygon_grid.GetPointData().SetScalars(scalar_polygon)

scalar_penta = vtkFloatArray()
scalar_penta.SetNumberOfTuples(penta_grid.GetNumberOfPoints())
scalar_penta.SetNumberOfComponents(1)
scalar_penta.Fill(0)
scalar_penta.SetValue(0, 4)
penta_grid.GetPointData().SetScalars(scalar_penta)

scalar_hexa = vtkFloatArray()
scalar_hexa.SetNumberOfTuples(hexa_grid.GetNumberOfPoints())
scalar_hexa.SetNumberOfComponents(1)
scalar_hexa.Fill(0)
scalar_hexa.SetValue(0, 4)
hexa_grid.GetPointData().SetScalars(scalar_hexa)

# Compute derivatives and create hedgehog actors.

# Voxel hedgehog.
derivs_voxel = vtkCellDerivatives()
derivs_voxel.SetInputData(voxel_grid)
derivs_voxel.SetVectorModeToComputeGradient()
centers_voxel = vtkCellCenters()
centers_voxel.SetInputConnection(derivs_voxel.GetOutputPort())
centers_voxel.VertexCellsOn()
hog_voxel = vtkHedgeHog()
hog_voxel.SetInputConnection(centers_voxel.GetOutputPort())
hog_mapper_voxel = vtkPolyDataMapper()
hog_mapper_voxel.SetInputConnection(hog_voxel.GetOutputPort())
hog_mapper_voxel.SetScalarModeToUseCellData()
hog_mapper_voxel.ScalarVisibilityOff()
hog_actor_voxel = vtkActor()
hog_actor_voxel.SetMapper(hog_mapper_voxel)
hog_actor_voxel.GetProperty().SetColor(0, 1, 0)
hog_actor_voxel.SetPosition(voxel_actor.GetPosition())
hog_actor_voxel.GetProperty().SetRepresentationToWireframe()

# Hexahedron hedgehog.
derivs_hexahedron = vtkCellDerivatives()
derivs_hexahedron.SetInputData(hexahedron_grid)
derivs_hexahedron.SetVectorModeToComputeGradient()
centers_hexahedron = vtkCellCenters()
centers_hexahedron.SetInputConnection(derivs_hexahedron.GetOutputPort())
centers_hexahedron.VertexCellsOn()
hog_hexahedron = vtkHedgeHog()
hog_hexahedron.SetInputConnection(centers_hexahedron.GetOutputPort())
hog_mapper_hexahedron = vtkPolyDataMapper()
hog_mapper_hexahedron.SetInputConnection(hog_hexahedron.GetOutputPort())
hog_mapper_hexahedron.SetScalarModeToUseCellData()
hog_mapper_hexahedron.ScalarVisibilityOff()
hog_actor_hexahedron = vtkActor()
hog_actor_hexahedron.SetMapper(hog_mapper_hexahedron)
hog_actor_hexahedron.GetProperty().SetColor(0, 1, 0)
hog_actor_hexahedron.SetPosition(hexahedron_actor.GetPosition())
hog_actor_hexahedron.GetProperty().SetRepresentationToWireframe()

# Wedge hedgehog.
derivs_wedge = vtkCellDerivatives()
derivs_wedge.SetInputData(wedge_grid)
derivs_wedge.SetVectorModeToComputeGradient()
centers_wedge = vtkCellCenters()
centers_wedge.SetInputConnection(derivs_wedge.GetOutputPort())
centers_wedge.VertexCellsOn()
hog_wedge = vtkHedgeHog()
hog_wedge.SetInputConnection(centers_wedge.GetOutputPort())
hog_mapper_wedge = vtkPolyDataMapper()
hog_mapper_wedge.SetInputConnection(hog_wedge.GetOutputPort())
hog_mapper_wedge.SetScalarModeToUseCellData()
hog_mapper_wedge.ScalarVisibilityOff()
hog_actor_wedge = vtkActor()
hog_actor_wedge.SetMapper(hog_mapper_wedge)
hog_actor_wedge.GetProperty().SetColor(0, 1, 0)
hog_actor_wedge.SetPosition(wedge_actor.GetPosition())
hog_actor_wedge.GetProperty().SetRepresentationToWireframe()

# Pyramid hedgehog.
derivs_pyramid = vtkCellDerivatives()
derivs_pyramid.SetInputData(pyramid_grid)
derivs_pyramid.SetVectorModeToComputeGradient()
centers_pyramid = vtkCellCenters()
centers_pyramid.SetInputConnection(derivs_pyramid.GetOutputPort())
centers_pyramid.VertexCellsOn()
hog_pyramid = vtkHedgeHog()
hog_pyramid.SetInputConnection(centers_pyramid.GetOutputPort())
hog_mapper_pyramid = vtkPolyDataMapper()
hog_mapper_pyramid.SetInputConnection(hog_pyramid.GetOutputPort())
hog_mapper_pyramid.SetScalarModeToUseCellData()
hog_mapper_pyramid.ScalarVisibilityOff()
hog_actor_pyramid = vtkActor()
hog_actor_pyramid.SetMapper(hog_mapper_pyramid)
hog_actor_pyramid.GetProperty().SetColor(0, 1, 0)
hog_actor_pyramid.SetPosition(pyramid_actor.GetPosition())
hog_actor_pyramid.GetProperty().SetRepresentationToWireframe()

# Tetra hedgehog.
derivs_tetra = vtkCellDerivatives()
derivs_tetra.SetInputData(tetra_grid)
derivs_tetra.SetVectorModeToComputeGradient()
centers_tetra = vtkCellCenters()
centers_tetra.SetInputConnection(derivs_tetra.GetOutputPort())
centers_tetra.VertexCellsOn()
hog_tetra = vtkHedgeHog()
hog_tetra.SetInputConnection(centers_tetra.GetOutputPort())
hog_mapper_tetra = vtkPolyDataMapper()
hog_mapper_tetra.SetInputConnection(hog_tetra.GetOutputPort())
hog_mapper_tetra.SetScalarModeToUseCellData()
hog_mapper_tetra.ScalarVisibilityOff()
hog_actor_tetra = vtkActor()
hog_actor_tetra.SetMapper(hog_mapper_tetra)
hog_actor_tetra.GetProperty().SetColor(0, 1, 0)
hog_actor_tetra.SetPosition(tetra_actor.GetPosition())
hog_actor_tetra.GetProperty().SetRepresentationToWireframe()

# Quad hedgehog.
derivs_quad = vtkCellDerivatives()
derivs_quad.SetInputData(quad_grid)
derivs_quad.SetVectorModeToComputeGradient()
centers_quad = vtkCellCenters()
centers_quad.SetInputConnection(derivs_quad.GetOutputPort())
centers_quad.VertexCellsOn()
hog_quad = vtkHedgeHog()
hog_quad.SetInputConnection(centers_quad.GetOutputPort())
hog_mapper_quad = vtkPolyDataMapper()
hog_mapper_quad.SetInputConnection(hog_quad.GetOutputPort())
hog_mapper_quad.SetScalarModeToUseCellData()
hog_mapper_quad.ScalarVisibilityOff()
hog_actor_quad = vtkActor()
hog_actor_quad.SetMapper(hog_mapper_quad)
hog_actor_quad.GetProperty().SetColor(0, 1, 0)
hog_actor_quad.SetPosition(quad_actor.GetPosition())
hog_actor_quad.GetProperty().SetRepresentationToWireframe()

# Triangle hedgehog.
derivs_triangle = vtkCellDerivatives()
derivs_triangle.SetInputData(triangle_grid)
derivs_triangle.SetVectorModeToComputeGradient()
centers_triangle = vtkCellCenters()
centers_triangle.SetInputConnection(derivs_triangle.GetOutputPort())
centers_triangle.VertexCellsOn()
hog_triangle = vtkHedgeHog()
hog_triangle.SetInputConnection(centers_triangle.GetOutputPort())
hog_mapper_triangle = vtkPolyDataMapper()
hog_mapper_triangle.SetInputConnection(hog_triangle.GetOutputPort())
hog_mapper_triangle.SetScalarModeToUseCellData()
hog_mapper_triangle.ScalarVisibilityOff()
hog_actor_triangle = vtkActor()
hog_actor_triangle.SetMapper(hog_mapper_triangle)
hog_actor_triangle.GetProperty().SetColor(0, 1, 0)
hog_actor_triangle.SetPosition(triangle_actor.GetPosition())
hog_actor_triangle.GetProperty().SetRepresentationToWireframe()

# Triangle strip hedgehog.
derivs_triangle_strip = vtkCellDerivatives()
derivs_triangle_strip.SetInputData(triangle_strip_grid)
derivs_triangle_strip.SetVectorModeToComputeGradient()
centers_triangle_strip = vtkCellCenters()
centers_triangle_strip.SetInputConnection(derivs_triangle_strip.GetOutputPort())
centers_triangle_strip.VertexCellsOn()
hog_triangle_strip = vtkHedgeHog()
hog_triangle_strip.SetInputConnection(centers_triangle_strip.GetOutputPort())
hog_mapper_triangle_strip = vtkPolyDataMapper()
hog_mapper_triangle_strip.SetInputConnection(hog_triangle_strip.GetOutputPort())
hog_mapper_triangle_strip.SetScalarModeToUseCellData()
hog_mapper_triangle_strip.ScalarVisibilityOff()
hog_actor_triangle_strip = vtkActor()
hog_actor_triangle_strip.SetMapper(hog_mapper_triangle_strip)
hog_actor_triangle_strip.GetProperty().SetColor(0, 1, 0)
hog_actor_triangle_strip.SetPosition(triangle_strip_actor.GetPosition())
hog_actor_triangle_strip.GetProperty().SetRepresentationToWireframe()

# Line hedgehog.
derivs_line = vtkCellDerivatives()
derivs_line.SetInputData(line_grid)
derivs_line.SetVectorModeToComputeGradient()
centers_line = vtkCellCenters()
centers_line.SetInputConnection(derivs_line.GetOutputPort())
centers_line.VertexCellsOn()
hog_line = vtkHedgeHog()
hog_line.SetInputConnection(centers_line.GetOutputPort())
hog_mapper_line = vtkPolyDataMapper()
hog_mapper_line.SetInputConnection(hog_line.GetOutputPort())
hog_mapper_line.SetScalarModeToUseCellData()
hog_mapper_line.ScalarVisibilityOff()
hog_actor_line = vtkActor()
hog_actor_line.SetMapper(hog_mapper_line)
hog_actor_line.GetProperty().SetColor(0, 1, 0)
hog_actor_line.SetPosition(line_actor.GetPosition())
hog_actor_line.GetProperty().SetRepresentationToWireframe()

# Poly line hedgehog.
derivs_poly_line = vtkCellDerivatives()
derivs_poly_line.SetInputData(poly_line_grid)
derivs_poly_line.SetVectorModeToComputeGradient()
centers_poly_line = vtkCellCenters()
centers_poly_line.SetInputConnection(derivs_poly_line.GetOutputPort())
centers_poly_line.VertexCellsOn()
hog_poly_line = vtkHedgeHog()
hog_poly_line.SetInputConnection(centers_poly_line.GetOutputPort())
hog_mapper_poly_line = vtkPolyDataMapper()
hog_mapper_poly_line.SetInputConnection(hog_poly_line.GetOutputPort())
hog_mapper_poly_line.SetScalarModeToUseCellData()
hog_mapper_poly_line.ScalarVisibilityOff()
hog_actor_poly_line = vtkActor()
hog_actor_poly_line.SetMapper(hog_mapper_poly_line)
hog_actor_poly_line.GetProperty().SetColor(0, 1, 0)
hog_actor_poly_line.SetPosition(poly_line_actor.GetPosition())
hog_actor_poly_line.GetProperty().SetRepresentationToWireframe()

# Vertex hedgehog.
derivs_vertex = vtkCellDerivatives()
derivs_vertex.SetInputData(vertex_grid)
derivs_vertex.SetVectorModeToComputeGradient()
centers_vertex = vtkCellCenters()
centers_vertex.SetInputConnection(derivs_vertex.GetOutputPort())
centers_vertex.VertexCellsOn()
hog_vertex = vtkHedgeHog()
hog_vertex.SetInputConnection(centers_vertex.GetOutputPort())
hog_mapper_vertex = vtkPolyDataMapper()
hog_mapper_vertex.SetInputConnection(hog_vertex.GetOutputPort())
hog_mapper_vertex.SetScalarModeToUseCellData()
hog_mapper_vertex.ScalarVisibilityOff()
hog_actor_vertex = vtkActor()
hog_actor_vertex.SetMapper(hog_mapper_vertex)
hog_actor_vertex.GetProperty().SetColor(0, 1, 0)
hog_actor_vertex.SetPosition(vertex_actor.GetPosition())
hog_actor_vertex.GetProperty().SetRepresentationToWireframe()

# Poly vertex hedgehog.
derivs_poly_vertex = vtkCellDerivatives()
derivs_poly_vertex.SetInputData(poly_vertex_grid)
derivs_poly_vertex.SetVectorModeToComputeGradient()
centers_poly_vertex = vtkCellCenters()
centers_poly_vertex.SetInputConnection(derivs_poly_vertex.GetOutputPort())
centers_poly_vertex.VertexCellsOn()
hog_poly_vertex = vtkHedgeHog()
hog_poly_vertex.SetInputConnection(centers_poly_vertex.GetOutputPort())
hog_mapper_poly_vertex = vtkPolyDataMapper()
hog_mapper_poly_vertex.SetInputConnection(hog_poly_vertex.GetOutputPort())
hog_mapper_poly_vertex.SetScalarModeToUseCellData()
hog_mapper_poly_vertex.ScalarVisibilityOff()
hog_actor_poly_vertex = vtkActor()
hog_actor_poly_vertex.SetMapper(hog_mapper_poly_vertex)
hog_actor_poly_vertex.GetProperty().SetColor(0, 1, 0)
hog_actor_poly_vertex.SetPosition(poly_vertex_actor.GetPosition())
hog_actor_poly_vertex.GetProperty().SetRepresentationToWireframe()

# Pixel hedgehog.
derivs_pixel = vtkCellDerivatives()
derivs_pixel.SetInputData(pixel_grid)
derivs_pixel.SetVectorModeToComputeGradient()
centers_pixel = vtkCellCenters()
centers_pixel.SetInputConnection(derivs_pixel.GetOutputPort())
centers_pixel.VertexCellsOn()
hog_pixel = vtkHedgeHog()
hog_pixel.SetInputConnection(centers_pixel.GetOutputPort())
hog_mapper_pixel = vtkPolyDataMapper()
hog_mapper_pixel.SetInputConnection(hog_pixel.GetOutputPort())
hog_mapper_pixel.SetScalarModeToUseCellData()
hog_mapper_pixel.ScalarVisibilityOff()
hog_actor_pixel = vtkActor()
hog_actor_pixel.SetMapper(hog_mapper_pixel)
hog_actor_pixel.GetProperty().SetColor(0, 1, 0)
hog_actor_pixel.SetPosition(pixel_actor.GetPosition())
hog_actor_pixel.GetProperty().SetRepresentationToWireframe()

# Polygon hedgehog.
derivs_polygon = vtkCellDerivatives()
derivs_polygon.SetInputData(polygon_grid)
derivs_polygon.SetVectorModeToComputeGradient()
centers_polygon = vtkCellCenters()
centers_polygon.SetInputConnection(derivs_polygon.GetOutputPort())
centers_polygon.VertexCellsOn()
hog_polygon = vtkHedgeHog()
hog_polygon.SetInputConnection(centers_polygon.GetOutputPort())
hog_mapper_polygon = vtkPolyDataMapper()
hog_mapper_polygon.SetInputConnection(hog_polygon.GetOutputPort())
hog_mapper_polygon.SetScalarModeToUseCellData()
hog_mapper_polygon.ScalarVisibilityOff()
hog_actor_polygon = vtkActor()
hog_actor_polygon.SetMapper(hog_mapper_polygon)
hog_actor_polygon.GetProperty().SetColor(0, 1, 0)
hog_actor_polygon.SetPosition(polygon_actor.GetPosition())
hog_actor_polygon.GetProperty().SetRepresentationToWireframe()

# Pentagonal prism hedgehog.
derivs_penta = vtkCellDerivatives()
derivs_penta.SetInputData(penta_grid)
derivs_penta.SetVectorModeToComputeGradient()
centers_penta = vtkCellCenters()
centers_penta.SetInputConnection(derivs_penta.GetOutputPort())
centers_penta.VertexCellsOn()
hog_penta = vtkHedgeHog()
hog_penta.SetInputConnection(centers_penta.GetOutputPort())
hog_mapper_penta = vtkPolyDataMapper()
hog_mapper_penta.SetInputConnection(hog_penta.GetOutputPort())
hog_mapper_penta.SetScalarModeToUseCellData()
hog_mapper_penta.ScalarVisibilityOff()
hog_actor_penta = vtkActor()
hog_actor_penta.SetMapper(hog_mapper_penta)
hog_actor_penta.GetProperty().SetColor(0, 1, 0)
hog_actor_penta.SetPosition(penta_actor.GetPosition())
hog_actor_penta.GetProperty().SetRepresentationToWireframe()

# Hexagonal prism hedgehog.
derivs_hexa = vtkCellDerivatives()
derivs_hexa.SetInputData(hexa_grid)
derivs_hexa.SetVectorModeToComputeGradient()
centers_hexa = vtkCellCenters()
centers_hexa.SetInputConnection(derivs_hexa.GetOutputPort())
centers_hexa.VertexCellsOn()
hog_hexa = vtkHedgeHog()
hog_hexa.SetInputConnection(centers_hexa.GetOutputPort())
hog_mapper_hexa = vtkPolyDataMapper()
hog_mapper_hexa.SetInputConnection(hog_hexa.GetOutputPort())
hog_mapper_hexa.SetScalarModeToUseCellData()
hog_mapper_hexa.ScalarVisibilityOff()
hog_actor_hexa = vtkActor()
hog_actor_hexa.SetMapper(hog_mapper_hexa)
hog_actor_hexa.GetProperty().SetColor(0, 1, 0)
hog_actor_hexa.SetPosition(hexa_actor.GetPosition())
hog_actor_hexa.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)

# Add cell and hedgehog actors.
renderer.AddActor(voxel_actor)
renderer.AddActor(hexahedron_actor)
renderer.AddActor(tetra_actor)
renderer.AddActor(wedge_actor)
renderer.AddActor(pyramid_actor)
renderer.AddActor(pixel_actor)
renderer.AddActor(quad_actor)
renderer.AddActor(triangle_actor)
renderer.AddActor(polygon_actor)
renderer.AddActor(triangle_strip_actor)
renderer.AddActor(line_actor)
renderer.AddActor(poly_line_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(poly_vertex_actor)
renderer.AddActor(penta_actor)
renderer.AddActor(hexa_actor)
renderer.AddActor(hog_actor_voxel)
renderer.AddActor(hog_actor_hexahedron)
renderer.AddActor(hog_actor_wedge)
renderer.AddActor(hog_actor_pyramid)
renderer.AddActor(hog_actor_tetra)
renderer.AddActor(hog_actor_quad)
renderer.AddActor(hog_actor_triangle)
renderer.AddActor(hog_actor_triangle_strip)
renderer.AddActor(hog_actor_line)
renderer.AddActor(hog_actor_poly_line)
renderer.AddActor(hog_actor_vertex)
renderer.AddActor(hog_actor_poly_vertex)
renderer.AddActor(hog_actor_pixel)
renderer.AddActor(hog_actor_polygon)
renderer.AddActor(hog_actor_penta)
renderer.AddActor(hog_actor_hexa)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 150)
render_window.SetWindowName("cell derivs")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Dolly(3.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
