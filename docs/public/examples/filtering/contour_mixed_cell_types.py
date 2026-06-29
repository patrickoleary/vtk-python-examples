#!/usr/bin/env python

# Contour a manually-built unstructured grid containing mixed cell types
# (quad, voxel, hex, triangle, pixel, pyramid, wedge) with vtkContour3DLinearGrid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIdList,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkHexahedron,
    vtkPixel,
    vtkPyramid,
    vtkQuad,
    vtkTriangle,
    vtkUnstructuredGrid,
    vtkVoxel,
    vtkWedge,
)
from vtkmodules.vtkFiltersCore import (
    vtkContour3DLinearGrid,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

merge_points = 1
interpolate_attr = 1
compute_normals = 1

# Build an unstructured grid with mixed cell types: quad, 8 voxels,
# triangle, 8 hexes, pixel, pyramid, wedge. 76 points, 21 cells.
unstructured_grid = vtkUnstructuredGrid()
grid_points = vtkPoints()
grid_points.SetNumberOfPoints(76)
unstructured_grid.SetPoints(grid_points)

# Quad points
grid_points.SetPoint(0, 0, 0, 0)
grid_points.SetPoint(1, 2, 0, 0)
grid_points.SetPoint(2, 0, 2, 0)
grid_points.SetPoint(3, 2, 2, 0)

# 3x3x3 voxel volume points (indices 4-30)
grid_points.SetPoint(4, 4, 0, -1)
grid_points.SetPoint(5, 5, 0, -1)
grid_points.SetPoint(6, 6, 0, -1)
grid_points.SetPoint(7, 4, 1, -1)
grid_points.SetPoint(8, 5, 1, -1)
grid_points.SetPoint(9, 6, 1, -1)
grid_points.SetPoint(10, 4, 2, -1)
grid_points.SetPoint(11, 5, 2, -1)
grid_points.SetPoint(12, 6, 2, -1)
grid_points.SetPoint(13, 4, 0, 0)
grid_points.SetPoint(14, 5, 0, 0)
grid_points.SetPoint(15, 6, 0, 0)
grid_points.SetPoint(16, 4, 1, 0)
grid_points.SetPoint(17, 5, 1, 0)
grid_points.SetPoint(18, 6, 1, 0)
grid_points.SetPoint(19, 4, 2, 0)
grid_points.SetPoint(20, 5, 2, 0)
grid_points.SetPoint(21, 6, 2, 0)
grid_points.SetPoint(22, 4, 0, 1)
grid_points.SetPoint(23, 5, 0, 1)
grid_points.SetPoint(24, 6, 0, 1)
grid_points.SetPoint(25, 4, 1, 1)
grid_points.SetPoint(26, 5, 1, 1)
grid_points.SetPoint(27, 6, 1, 1)
grid_points.SetPoint(28, 4, 2, 1)
grid_points.SetPoint(29, 5, 2, 1)
grid_points.SetPoint(30, 6, 2, 1)

# Triangle point
grid_points.SetPoint(31, 8, 0, 0)
grid_points.SetPoint(32, 10, 0, 0)
grid_points.SetPoint(33, 9, 2, 0)

# 3x3x3 hex volume points (indices 34-60)
grid_points.SetPoint(34, 12, 0, -1)
grid_points.SetPoint(35, 13, 0, -1)
grid_points.SetPoint(36, 14, 0, -1)
grid_points.SetPoint(37, 12, 1, -1)
grid_points.SetPoint(38, 13, 1, -1)
grid_points.SetPoint(39, 14, 1, -1)
grid_points.SetPoint(40, 12, 2, -1)
grid_points.SetPoint(41, 13, 2, -1)
grid_points.SetPoint(42, 14, 2, -1)
grid_points.SetPoint(43, 12, 0, 0)
grid_points.SetPoint(44, 13, 0, 0)
grid_points.SetPoint(45, 14, 0, 0)
grid_points.SetPoint(46, 12, 1, 0)
grid_points.SetPoint(47, 13, 1, 0)
grid_points.SetPoint(48, 14, 1, 0)
grid_points.SetPoint(49, 12, 2, 0)
grid_points.SetPoint(50, 13, 2, 0)
grid_points.SetPoint(51, 14, 2, 0)
grid_points.SetPoint(52, 12, 0, 1)
grid_points.SetPoint(53, 13, 0, 1)
grid_points.SetPoint(54, 14, 0, 1)
grid_points.SetPoint(55, 12, 1, 1)
grid_points.SetPoint(56, 13, 1, 1)
grid_points.SetPoint(57, 14, 1, 1)
grid_points.SetPoint(58, 12, 2, 1)
grid_points.SetPoint(59, 13, 2, 1)
grid_points.SetPoint(60, 14, 2, 1)

# Pixel points
grid_points.SetPoint(61, 16, 0, 0)
grid_points.SetPoint(62, 18, 0, 0)
grid_points.SetPoint(63, 16, 2, 0)
grid_points.SetPoint(64, 18, 2, 0)

# Pyramid points
grid_points.SetPoint(65, 20, 0, -1)
grid_points.SetPoint(66, 22, 0, -1)
grid_points.SetPoint(67, 20, 2, -1)
grid_points.SetPoint(68, 22, 2, -1)
grid_points.SetPoint(69, 21, 1, 1)

# Wedge points
grid_points.SetPoint(70, 24, 0, 1)
grid_points.SetPoint(71, 26, 0, 1)
grid_points.SetPoint(72, 24, 2, 1)
grid_points.SetPoint(73, 26, 2, 1)
grid_points.SetPoint(74, 25, 0, -1)
grid_points.SetPoint(75, 25, 2, -1)

# Insert cells
cell_ids = vtkIdList()

# Quad
quad = vtkQuad()
cell_ids.SetNumberOfIds(4)
cell_ids.SetId(0, 0)
cell_ids.SetId(1, 1)
cell_ids.SetId(2, 3)
cell_ids.SetId(3, 2)
unstructured_grid.InsertNextCell(quad.GetCellType(), cell_ids)

# 8 voxels
voxel_cell = vtkVoxel()
voxel_connectivity = [
    [4, 5, 7, 8, 13, 14, 16, 17],
    [5, 6, 8, 9, 14, 15, 17, 18],
    [7, 8, 10, 11, 16, 17, 19, 20],
    [8, 9, 11, 12, 17, 18, 20, 21],
    [13, 14, 16, 17, 22, 23, 25, 26],
    [14, 15, 17, 18, 23, 24, 26, 27],
    [16, 17, 19, 20, 25, 26, 28, 29],
    [17, 18, 20, 21, 26, 27, 29, 30],
]
cell_ids.SetNumberOfIds(8)
for conn in voxel_connectivity:
    for j in range(8):
        cell_ids.SetId(j, conn[j])
    unstructured_grid.InsertNextCell(voxel_cell.GetCellType(), cell_ids)

# Triangle
triangle_cell = vtkTriangle()
cell_ids.SetNumberOfIds(3)
cell_ids.SetId(0, 31)
cell_ids.SetId(1, 32)
cell_ids.SetId(2, 33)
unstructured_grid.InsertNextCell(triangle_cell.GetCellType(), cell_ids)

# 8 hexes
hex_cell = vtkHexahedron()
hex_connectivity = [
    [34, 35, 38, 37, 43, 44, 47, 46],
    [35, 36, 39, 38, 44, 45, 48, 47],
    [37, 38, 41, 40, 46, 47, 50, 49],
    [38, 39, 42, 41, 47, 48, 51, 50],
    [43, 44, 47, 46, 52, 53, 56, 55],
    [44, 45, 48, 47, 53, 54, 57, 56],
    [46, 47, 50, 49, 55, 56, 59, 58],
    [47, 48, 51, 50, 56, 57, 60, 59],
]
cell_ids.SetNumberOfIds(8)
for conn in hex_connectivity:
    for j in range(8):
        cell_ids.SetId(j, conn[j])
    unstructured_grid.InsertNextCell(hex_cell.GetCellType(), cell_ids)

# Pixel
pixel = vtkPixel()
cell_ids.SetNumberOfIds(4)
cell_ids.SetId(0, 61)
cell_ids.SetId(1, 62)
cell_ids.SetId(2, 63)
cell_ids.SetId(3, 64)
unstructured_grid.InsertNextCell(pixel.GetCellType(), cell_ids)

# Pyramid
pyramid_cell = vtkPyramid()
cell_ids.SetNumberOfIds(5)
cell_ids.SetId(0, 65)
cell_ids.SetId(1, 66)
cell_ids.SetId(2, 68)
cell_ids.SetId(3, 67)
cell_ids.SetId(4, 69)
unstructured_grid.InsertNextCell(pyramid_cell.GetCellType(), cell_ids)

# Wedge
wedge = vtkWedge()
cell_ids.SetNumberOfIds(6)
cell_ids.SetId(0, 70)
cell_ids.SetId(1, 71)
cell_ids.SetId(2, 74)
cell_ids.SetId(3, 72)
cell_ids.SetId(4, 73)
cell_ids.SetId(5, 75)
unstructured_grid.InsertNextCell(wedge.GetCellType(), cell_ids)

# Elevation filter to generate scalars for contouring
elevation = vtkSimpleElevationFilter()
elevation.SetInputData(unstructured_grid)
elevation.SetVector(0, 1, 0)

# Contour the mixed-cell grid
contour = vtkContour3DLinearGrid()
contour.SetInputConnection(elevation.GetOutputPort())
contour.SetValue(0, 1)
contour.SetMergePoints(merge_points)
contour.SetInterpolateAttributes(interpolate_attr)
contour.SetComputeNormals(compute_normals)
contour.Update()

contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour.GetOutputPort())
contour_mapper.ScalarVisibilityOff()

contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(0.8, 0.4, 0.4)

# Wireframe of the original grid
cell_mapper = vtkDataSetMapper()
cell_mapper.SetInputData(unstructured_grid)
cell_mapper.ScalarVisibilityOff()

cell_actor = vtkActor()
cell_actor.SetMapper(cell_mapper)
cell_actor.GetProperty().SetColor(0.8, 0.4, 0.4)
cell_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(contour_actor)
renderer.AddActor(cell_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 100)
render_window.SetWindowName("contour mixed cell types")

# Scene
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(0, 0.5, 1)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(3.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
