#!/usr/bin/env python

# Test vtkCellPicker flat block index matching with vtkCompositePolyDataMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkMultiBlockDataSet,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkCompositeDataDisplayAttributes,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Regular 3x3x3 grid of points
dx = 2.0
dy = 3.0
grid_coords = [
    [0.0, 0.0, -4.0], [2.0, 0.0, -4.0], [4.0, 0.0, -4.0],
    [0.0, 3.0, -4.0], [2.0, 3.0, -4.0], [4.0, 3.0, -4.0],
    [0.0, 6.0, -4.0], [2.0, 6.0, -4.0], [4.0, 6.0, -4.0],
    [0.0, 0.0, -2.0], [2.0, 0.0, -2.0], [4.0, 0.0, -2.0],
    [0.0, 3.0, -2.0], [2.0, 3.0, -2.0], [4.0, 3.0, -2.0],
    [0.0, 6.0, -2.0], [2.0, 6.0, -2.0], [4.0, 6.0, -2.0],
    [0.0, 0.0, 0.0], [2.0, 0.0, 0.0], [4.0, 0.0, 0.0],
    [0.0, 3.0, 0.0], [2.0, 3.0, 0.0], [4.0, 3.0, 0.0],
    [0.0, 6.0, 0.0], [2.0, 6.0, 0.0], [4.0, 6.0, 0.0],
]

# Construct multi-block dataset
multi_block = vtkMultiBlockDataSet()
multi_block.SetNumberOfBlocks(4)

display_attributes = vtkCompositeDataDisplayAttributes()
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(multi_block)
mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Part 0: verts [0],[1],[2],[3], polys [0,1,4,3], color red
points_0 = vtkPoints()
for coord in grid_coords:
    points_0.InsertNextPoint(coord)
verts_0 = vtkCellArray()
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(0)
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(1)
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(2)
verts_0.InsertNextCell(1)
verts_0.InsertCellPoint(3)
polys_0 = vtkCellArray()
polys_0.InsertNextCell(4)
polys_0.InsertCellPoint(0)
polys_0.InsertCellPoint(1)
polys_0.InsertCellPoint(4)
polys_0.InsertCellPoint(3)
poly_0 = vtkPolyData()
poly_0.SetPoints(points_0)
poly_0.SetVerts(verts_0)
poly_0.SetPolys(polys_0)
multi_block.SetBlock(0, poly_0)
mapper.SetBlockColor(1, [1, 0, 0])

# Part 1: verts [0],[1],[2], polys [1,2,5,4], color green
points_1 = vtkPoints()
for coord in grid_coords:
    points_1.InsertNextPoint(coord)
verts_1 = vtkCellArray()
verts_1.InsertNextCell(1)
verts_1.InsertCellPoint(0)
verts_1.InsertNextCell(1)
verts_1.InsertCellPoint(1)
verts_1.InsertNextCell(1)
verts_1.InsertCellPoint(2)
polys_1 = vtkCellArray()
polys_1.InsertNextCell(4)
polys_1.InsertCellPoint(1)
polys_1.InsertCellPoint(2)
polys_1.InsertCellPoint(5)
polys_1.InsertCellPoint(4)
poly_1 = vtkPolyData()
poly_1.SetPoints(points_1)
poly_1.SetVerts(verts_1)
poly_1.SetPolys(polys_1)
multi_block.SetBlock(1, poly_1)
mapper.SetBlockColor(2, [0, 1, 0])

# Part 2: verts [0],[1], polys [3,4,7,6], color blue
points_2 = vtkPoints()
for coord in grid_coords:
    points_2.InsertNextPoint(coord)
verts_2 = vtkCellArray()
verts_2.InsertNextCell(1)
verts_2.InsertCellPoint(0)
verts_2.InsertNextCell(1)
verts_2.InsertCellPoint(1)
polys_2 = vtkCellArray()
polys_2.InsertNextCell(4)
polys_2.InsertCellPoint(3)
polys_2.InsertCellPoint(4)
polys_2.InsertCellPoint(7)
polys_2.InsertCellPoint(6)
poly_2 = vtkPolyData()
poly_2.SetPoints(points_2)
poly_2.SetVerts(verts_2)
poly_2.SetPolys(polys_2)
multi_block.SetBlock(2, poly_2)
mapper.SetBlockColor(3, [0, 0, 1])

# Part 3: verts [0], polys [4,5,8,7], color yellow
points_3 = vtkPoints()
for coord in grid_coords:
    points_3.InsertNextPoint(coord)
verts_3 = vtkCellArray()
verts_3.InsertNextCell(1)
verts_3.InsertCellPoint(0)
polys_3 = vtkCellArray()
polys_3.InsertNextCell(4)
polys_3.InsertCellPoint(4)
polys_3.InsertCellPoint(5)
polys_3.InsertCellPoint(8)
polys_3.InsertCellPoint(7)
poly_3 = vtkPolyData()
poly_3.SetPoints(points_3)
poly_3.SetVerts(verts_3)
poly_3.SetPolys(polys_3)
multi_block.SetBlock(3, poly_3)
mapper.SetBlockColor(4, [1, 1, 0])

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(1, 1, 1)

renderer = vtkRenderer()
renderer.AddViewProp(actor)
renderer.SetBackground(0, 0, 0)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cell picker composite block")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# Picker
cell_picker = vtkCellPicker()

# Pick test data: (pick-coordinate, (result, block, cell, point))
delta = 0.00001
pick_data = [
    ((0.1 * dx, 0.1 * dy), (True, 1, 4, 0)),
    ((0.9 * dx, 0.9 * dy), (True, 1, 4, 4)),
    ((0.9 * dx, dy - delta), (True, 3, 2, 4)),
    ((0.9 * dx, dy + delta), (True, 3, 2, 4)),
]

# Run picks
for data in pick_data:
    xy = data[0]
    size = render_window.GetSize()
    p = [size[0] / 2, size[1] / 2, 0]

    camera = renderer.GetActiveCamera()
    camera.SetPosition(xy[0], xy[1], 2.0)
    camera.SetFocalPoint(xy[0], xy[1], 0.0)
    camera.SetViewUp(0, 1, 0)
    camera.SetViewAngle(35)
    camera.ParallelProjectionOn()
    renderer.ResetCameraClippingRange()
    render_window.Render()

    cell_picker.Pick(p[0], p[1], 0, renderer)

interactor.Initialize()
interactor.Start()
