#!/usr/bin/env python

# Test picking cells and points on various cell types.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
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
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkPointPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWorldPointPicker,
)

# Voxel
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
a_voxel = vtkVoxel()
for i in range(8):
    a_voxel.GetPointIds().SetId(i, i)
a_voxel_grid = vtkUnstructuredGrid()
a_voxel_grid.Allocate(1, 1)
a_voxel_grid.InsertNextCell(a_voxel.GetCellType(), a_voxel.GetPointIds())
a_voxel_grid.SetPoints(voxel_points)
a_voxel_mapper = vtkDataSetMapper()
a_voxel_mapper.SetInputData(a_voxel_grid)
a_voxel_actor = vtkActor()
a_voxel_actor.SetMapper(a_voxel_mapper)
a_voxel_actor.GetProperty().BackfaceCullingOn()

# Hexahedron
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
a_hexahedron = vtkHexahedron()
for i in range(8):
    a_hexahedron.GetPointIds().SetId(i, i)
a_hexahedron_grid = vtkUnstructuredGrid()
a_hexahedron_grid.Allocate(1, 1)
a_hexahedron_grid.InsertNextCell(a_hexahedron.GetCellType(), a_hexahedron.GetPointIds())
a_hexahedron_grid.SetPoints(hexahedron_points)
a_hexahedron_mapper = vtkDataSetMapper()
a_hexahedron_mapper.SetInputData(a_hexahedron_grid)
a_hexahedron_actor = vtkActor()
a_hexahedron_actor.SetMapper(a_hexahedron_mapper)
a_hexahedron_actor.AddPosition(2, 0, 0)
a_hexahedron_actor.GetProperty().BackfaceCullingOn()

# Tetra
tetra_points = vtkPoints()
tetra_points.SetNumberOfPoints(4)
tetra_points.InsertPoint(0, 0, 0, 0)
tetra_points.InsertPoint(1, 1, 0, 0)
tetra_points.InsertPoint(2, 0.5, 1, 0)
tetra_points.InsertPoint(3, 0.5, 0.5, 1)
a_tetra = vtkTetra()
for i in range(4):
    a_tetra.GetPointIds().SetId(i, i)
a_tetra_grid = vtkUnstructuredGrid()
a_tetra_grid.Allocate(1, 1)
a_tetra_grid.InsertNextCell(a_tetra.GetCellType(), a_tetra.GetPointIds())
a_tetra_grid.SetPoints(tetra_points)
a_tetra_mapper = vtkDataSetMapper()
a_tetra_mapper.SetInputData(a_tetra_grid)
a_tetra_actor = vtkActor()
a_tetra_actor.SetMapper(a_tetra_mapper)
a_tetra_actor.AddPosition(4, 0, 0)
a_tetra_actor.GetProperty().BackfaceCullingOn()

# Wedge
wedge_points = vtkPoints()
wedge_points.SetNumberOfPoints(6)
wedge_points.InsertPoint(0, 0, 1, 0)
wedge_points.InsertPoint(1, 0, 0, 0)
wedge_points.InsertPoint(2, 0, 0.5, 0.5)
wedge_points.InsertPoint(3, 1, 1, 0)
wedge_points.InsertPoint(4, 1, 0, 0)
wedge_points.InsertPoint(5, 1, 0.5, 0.5)
a_wedge = vtkWedge()
for i in range(6):
    a_wedge.GetPointIds().SetId(i, i)
a_wedge_grid = vtkUnstructuredGrid()
a_wedge_grid.Allocate(1, 1)
a_wedge_grid.InsertNextCell(a_wedge.GetCellType(), a_wedge.GetPointIds())
a_wedge_grid.SetPoints(wedge_points)
a_wedge_mapper = vtkDataSetMapper()
a_wedge_mapper.SetInputData(a_wedge_grid)
a_wedge_actor = vtkActor()
a_wedge_actor.SetMapper(a_wedge_mapper)
a_wedge_actor.AddPosition(6, 0, 0)
a_wedge_actor.GetProperty().BackfaceCullingOn()

# Pyramid
pyramid_points = vtkPoints()
pyramid_points.SetNumberOfPoints(5)
pyramid_points.InsertPoint(0, 0, 0, 0)
pyramid_points.InsertPoint(1, 1, 0, 0)
pyramid_points.InsertPoint(2, 1, 1, 0)
pyramid_points.InsertPoint(3, 0, 1, 0)
pyramid_points.InsertPoint(4, 0.5, 0.5, 1)
a_pyramid = vtkPyramid()
for i in range(5):
    a_pyramid.GetPointIds().SetId(i, i)
a_pyramid_grid = vtkUnstructuredGrid()
a_pyramid_grid.Allocate(1, 1)
a_pyramid_grid.InsertNextCell(a_pyramid.GetCellType(), a_pyramid.GetPointIds())
a_pyramid_grid.SetPoints(pyramid_points)
a_pyramid_mapper = vtkDataSetMapper()
a_pyramid_mapper.SetInputData(a_pyramid_grid)
a_pyramid_actor = vtkActor()
a_pyramid_actor.SetMapper(a_pyramid_mapper)
a_pyramid_actor.AddPosition(8, 0, 0)
a_pyramid_actor.GetProperty().BackfaceCullingOn()

# Pixel
pixel_points = vtkPoints()
pixel_points.SetNumberOfPoints(4)
pixel_points.InsertPoint(0, 0, 0, 0)
pixel_points.InsertPoint(1, 1, 0, 0)
pixel_points.InsertPoint(2, 0, 1, 0)
pixel_points.InsertPoint(3, 1, 1, 0)
a_pixel = vtkPixel()
for i in range(4):
    a_pixel.GetPointIds().SetId(i, i)
a_pixel_grid = vtkUnstructuredGrid()
a_pixel_grid.Allocate(1, 1)
a_pixel_grid.InsertNextCell(a_pixel.GetCellType(), a_pixel.GetPointIds())
a_pixel_grid.SetPoints(pixel_points)
a_pixel_mapper = vtkDataSetMapper()
a_pixel_mapper.SetInputData(a_pixel_grid)
a_pixel_actor = vtkActor()
a_pixel_actor.SetMapper(a_pixel_mapper)
a_pixel_actor.AddPosition(0, 0, 2)
a_pixel_actor.GetProperty().BackfaceCullingOn()

# Quad
quad_points = vtkPoints()
quad_points.SetNumberOfPoints(4)
quad_points.InsertPoint(0, 0, 0, 0)
quad_points.InsertPoint(1, 1, 0, 0)
quad_points.InsertPoint(2, 1, 1, 0)
quad_points.InsertPoint(3, 0, 1, 0)
a_quad = vtkQuad()
for i in range(4):
    a_quad.GetPointIds().SetId(i, i)
a_quad_grid = vtkUnstructuredGrid()
a_quad_grid.Allocate(1, 1)
a_quad_grid.InsertNextCell(a_quad.GetCellType(), a_quad.GetPointIds())
a_quad_grid.SetPoints(quad_points)
a_quad_mapper = vtkDataSetMapper()
a_quad_mapper.SetInputData(a_quad_grid)
a_quad_actor = vtkActor()
a_quad_actor.SetMapper(a_quad_mapper)
a_quad_actor.AddPosition(2, 0, 2)
a_quad_actor.GetProperty().BackfaceCullingOn()

# Triangle
triangle_points = vtkPoints()
triangle_points.SetNumberOfPoints(3)
triangle_points.InsertPoint(0, 0, 0, 0)
triangle_points.InsertPoint(1, 1, 0, 0)
triangle_points.InsertPoint(2, 0.5, 0.5, 0)
a_triangle = vtkTriangle()
for i in range(3):
    a_triangle.GetPointIds().SetId(i, i)
a_triangle_grid = vtkUnstructuredGrid()
a_triangle_grid.Allocate(1, 1)
a_triangle_grid.InsertNextCell(a_triangle.GetCellType(), a_triangle.GetPointIds())
a_triangle_grid.SetPoints(triangle_points)
a_triangle_mapper = vtkDataSetMapper()
a_triangle_mapper.SetInputData(a_triangle_grid)
a_triangle_actor = vtkActor()
a_triangle_actor.SetMapper(a_triangle_mapper)
a_triangle_actor.AddPosition(4, 0, 2)
a_triangle_actor.GetProperty().BackfaceCullingOn()

# Polygon
polygon_points = vtkPoints()
polygon_points.SetNumberOfPoints(4)
polygon_points.InsertPoint(0, 0, 0, 0)
polygon_points.InsertPoint(1, 1, 0, 0)
polygon_points.InsertPoint(2, 1, 1, 0)
polygon_points.InsertPoint(3, 0, 1, 0)
a_polygon = vtkPolygon()
a_polygon.GetPointIds().SetNumberOfIds(4)
for i in range(4):
    a_polygon.GetPointIds().SetId(i, i)
a_polygon_grid = vtkUnstructuredGrid()
a_polygon_grid.Allocate(1, 1)
a_polygon_grid.InsertNextCell(a_polygon.GetCellType(), a_polygon.GetPointIds())
a_polygon_grid.SetPoints(polygon_points)
a_polygon_mapper = vtkDataSetMapper()
a_polygon_mapper.SetInputData(a_polygon_grid)
a_polygon_actor = vtkActor()
a_polygon_actor.SetMapper(a_polygon_mapper)
a_polygon_actor.AddPosition(6, 0, 2)
a_polygon_actor.GetProperty().BackfaceCullingOn()

# Triangle strip
triangle_strip_points = vtkPoints()
triangle_strip_points.SetNumberOfPoints(5)
triangle_strip_points.InsertPoint(0, 0, 1, 0)
triangle_strip_points.InsertPoint(1, 0, 0, 0)
triangle_strip_points.InsertPoint(2, 1, 1, 0)
triangle_strip_points.InsertPoint(3, 1, 0, 0)
triangle_strip_points.InsertPoint(4, 2, 1, 0)
a_triangle_strip = vtkTriangleStrip()
a_triangle_strip.GetPointIds().SetNumberOfIds(5)
for i in range(5):
    a_triangle_strip.GetPointIds().SetId(i, i)
a_triangle_strip_grid = vtkUnstructuredGrid()
a_triangle_strip_grid.Allocate(1, 1)
a_triangle_strip_grid.InsertNextCell(a_triangle_strip.GetCellType(), a_triangle_strip.GetPointIds())
a_triangle_strip_grid.SetPoints(triangle_strip_points)
a_triangle_strip_mapper = vtkDataSetMapper()
a_triangle_strip_mapper.SetInputData(a_triangle_strip_grid)
a_triangle_strip_actor = vtkActor()
a_triangle_strip_actor.SetMapper(a_triangle_strip_mapper)
a_triangle_strip_actor.AddPosition(8, 0, 2)
a_triangle_strip_actor.GetProperty().BackfaceCullingOn()

# Line
line_points = vtkPoints()
line_points.SetNumberOfPoints(2)
line_points.InsertPoint(0, 0, 0, 0)
line_points.InsertPoint(1, 1, 1, 0)
a_line = vtkLine()
a_line.GetPointIds().SetId(0, 0)
a_line.GetPointIds().SetId(1, 1)
a_line_grid = vtkUnstructuredGrid()
a_line_grid.Allocate(1, 1)
a_line_grid.InsertNextCell(a_line.GetCellType(), a_line.GetPointIds())
a_line_grid.SetPoints(line_points)
a_line_mapper = vtkDataSetMapper()
a_line_mapper.SetInputData(a_line_grid)
a_line_actor = vtkActor()
a_line_actor.SetMapper(a_line_mapper)
a_line_actor.AddPosition(0, 0, 4)
a_line_actor.GetProperty().BackfaceCullingOn()

# Poly line
poly_line_points = vtkPoints()
poly_line_points.SetNumberOfPoints(3)
poly_line_points.InsertPoint(0, 0, 0, 0)
poly_line_points.InsertPoint(1, 1, 1, 0)
poly_line_points.InsertPoint(2, 1, 0, 0)
a_poly_line = vtkPolyLine()
a_poly_line.GetPointIds().SetNumberOfIds(3)
for i in range(3):
    a_poly_line.GetPointIds().SetId(i, i)
a_poly_line_grid = vtkUnstructuredGrid()
a_poly_line_grid.Allocate(1, 1)
a_poly_line_grid.InsertNextCell(a_poly_line.GetCellType(), a_poly_line.GetPointIds())
a_poly_line_grid.SetPoints(poly_line_points)
a_poly_line_mapper = vtkDataSetMapper()
a_poly_line_mapper.SetInputData(a_poly_line_grid)
a_poly_line_actor = vtkActor()
a_poly_line_actor.SetMapper(a_poly_line_mapper)
a_poly_line_actor.AddPosition(2, 0, 4)
a_poly_line_actor.GetProperty().BackfaceCullingOn()

# Vertex
vertex_points = vtkPoints()
vertex_points.SetNumberOfPoints(1)
vertex_points.InsertPoint(0, 0, 0, 0)
a_vertex = vtkVertex()
a_vertex.GetPointIds().SetId(0, 0)
a_vertex_grid = vtkUnstructuredGrid()
a_vertex_grid.Allocate(1, 1)
a_vertex_grid.InsertNextCell(a_vertex.GetCellType(), a_vertex.GetPointIds())
a_vertex_grid.SetPoints(vertex_points)
a_vertex_mapper = vtkDataSetMapper()
a_vertex_mapper.SetInputData(a_vertex_grid)
a_vertex_actor = vtkActor()
a_vertex_actor.SetMapper(a_vertex_mapper)
a_vertex_actor.AddPosition(0, 0, 6)
a_vertex_actor.GetProperty().BackfaceCullingOn()

# Poly vertex
poly_vertex_points = vtkPoints()
poly_vertex_points.SetNumberOfPoints(3)
poly_vertex_points.InsertPoint(0, 0, 0, 0)
poly_vertex_points.InsertPoint(1, 1, 0, 0)
poly_vertex_points.InsertPoint(2, 1, 1, 0)
a_poly_vertex = vtkPolyVertex()
a_poly_vertex.GetPointIds().SetNumberOfIds(3)
for i in range(3):
    a_poly_vertex.GetPointIds().SetId(i, i)
a_poly_vertex_grid = vtkUnstructuredGrid()
a_poly_vertex_grid.Allocate(1, 1)
a_poly_vertex_grid.InsertNextCell(a_poly_vertex.GetCellType(), a_poly_vertex.GetPointIds())
a_poly_vertex_grid.SetPoints(poly_vertex_points)
a_poly_vertex_mapper = vtkDataSetMapper()
a_poly_vertex_mapper.SetInputData(a_poly_vertex_grid)
a_poly_vertex_actor = vtkActor()
a_poly_vertex_actor.SetMapper(a_poly_vertex_mapper)
a_poly_vertex_actor.AddPosition(2, 0, 6)
a_poly_vertex_actor.GetProperty().BackfaceCullingOn()

# Pentagonal prism
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
a_penta = vtkPentagonalPrism()
for i in range(10):
    a_penta.GetPointIds().SetId(i, i)
a_penta_grid = vtkUnstructuredGrid()
a_penta_grid.Allocate(1, 1)
a_penta_grid.InsertNextCell(a_penta.GetCellType(), a_penta.GetPointIds())
a_penta_grid.SetPoints(penta_points)
a_penta_mapper = vtkDataSetMapper()
a_penta_mapper.SetInputData(a_penta_grid)
a_penta_actor = vtkActor()
a_penta_actor.SetMapper(a_penta_mapper)
a_penta_actor.AddPosition(10, 0, 0)
a_penta_actor.GetProperty().BackfaceCullingOn()

# Hexagonal prism
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
a_hexa = vtkHexagonalPrism()
for i in range(12):
    a_hexa.GetPointIds().SetId(i, i)
a_hexa_grid = vtkUnstructuredGrid()
a_hexa_grid.Allocate(1, 1)
a_hexa_grid.InsertNextCell(a_hexa.GetCellType(), a_hexa.GetPointIds())
a_hexa_grid.SetPoints(hexa_points)
a_hexa_mapper = vtkDataSetMapper()
a_hexa_mapper.SetInputData(a_hexa_grid)
a_hexa_actor = vtkActor()
a_hexa_actor.SetMapper(a_hexa_mapper)
a_hexa_actor.AddPosition(12, 0, 0)
a_hexa_actor.GetProperty().BackfaceCullingOn()

# Renderer setup
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

renderer.AddActor(a_voxel_actor)
a_voxel_actor.GetProperty().SetDiffuseColor(1, 0, 0)
renderer.AddActor(a_hexahedron_actor)
a_hexahedron_actor.GetProperty().SetDiffuseColor(1, 1, 0)
renderer.AddActor(a_tetra_actor)
a_tetra_actor.GetProperty().SetDiffuseColor(0, 1, 0)
renderer.AddActor(a_wedge_actor)
a_wedge_actor.GetProperty().SetDiffuseColor(0, 1, 1)
renderer.AddActor(a_pyramid_actor)
a_pyramid_actor.GetProperty().SetDiffuseColor(1, 0, 1)
renderer.AddActor(a_pixel_actor)
a_pixel_actor.GetProperty().SetDiffuseColor(0, 1, 1)
renderer.AddActor(a_quad_actor)
a_quad_actor.GetProperty().SetDiffuseColor(1, 0, 1)
renderer.AddActor(a_triangle_actor)
a_triangle_actor.GetProperty().SetDiffuseColor(0.3, 1, 0.5)
renderer.AddActor(a_polygon_actor)
a_polygon_actor.GetProperty().SetDiffuseColor(1, 0.4, 0.5)
renderer.AddActor(a_triangle_strip_actor)
a_triangle_strip_actor.GetProperty().SetDiffuseColor(0.3, 0.7, 1)
renderer.AddActor(a_line_actor)
a_line_actor.GetProperty().SetDiffuseColor(0.2, 1, 1)
renderer.AddActor(a_poly_line_actor)
a_poly_line_actor.GetProperty().SetDiffuseColor(1, 1, 1)
renderer.AddActor(a_vertex_actor)
a_vertex_actor.GetProperty().SetDiffuseColor(1, 1, 1)
renderer.AddActor(a_poly_vertex_actor)
a_poly_vertex_actor.GetProperty().SetDiffuseColor(1, 1, 1)
renderer.AddActor(a_penta_actor)
a_penta_actor.GetProperty().SetDiffuseColor(0.2, 0.4, 0.7)
renderer.AddActor(a_hexa_actor)
a_hexa_actor.GetProperty().SetDiffuseColor(0.7, 0.5, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pick cells")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Dolly(1.25)
renderer.ResetCameraClippingRange()

render_window.Render()

# Perform picks
cell_picker = vtkCellPicker()
point_picker = vtkPointPicker()
world_picker = vtkWorldPointPicker()

renderer.IsInViewport(0, 0)
x = 0
while x <= 265:
    y = 100
    while y <= 200:
        cell_picker.Pick(x, y, 0, renderer)
        point_picker.Pick(x, y, 0, renderer)
        world_picker.Pick(x, y, 0, renderer)
        y = y + 6
    x = x + 6

interactor.Initialize()
interactor.Start()
