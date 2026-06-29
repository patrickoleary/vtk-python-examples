#!/usr/bin/env python

# Test picking props, points, and cells with vtkCompositePolyDataMapper.

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
    vtkPicker,
    vtkPointPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Construct the multi-block dataset
multi_block = vtkMultiBlockDataSet()
multi_block.SetNumberOfBlocks(3)

display_attributes = vtkCompositeDataDisplayAttributes()
mapper = vtkCompositePolyDataMapper()
mapper.SetInputDataObject(multi_block)
mapper.SetCompositeDataDisplayAttributes(display_attributes)

# Block 0
points_0 = vtkPoints()
points_0.InsertNextPoint(4., 4., 0.)
points_0.InsertNextPoint(10., 4., 0.)
points_0.InsertNextPoint(10., 6., 0.)
points_0.InsertNextPoint(4., 6., 0.)
points_0.InsertNextPoint(20., 0., 0.)
points_0.InsertNextPoint(25., 0., 0.)
points_0.InsertNextPoint(30., 0., 0.)
points_0.InsertNextPoint(30., 1., 0.)
points_0.InsertNextPoint(25., 1., 0.)
points_0.InsertNextPoint(20., 1., 0.)

polys_0 = vtkCellArray()
polys_0.InsertNextCell(4)
polys_0.InsertCellPoint(0)
polys_0.InsertCellPoint(1)
polys_0.InsertCellPoint(2)
polys_0.InsertCellPoint(3)
polys_0.InsertNextCell(4)
polys_0.InsertCellPoint(4)
polys_0.InsertCellPoint(5)
polys_0.InsertCellPoint(8)
polys_0.InsertCellPoint(9)
polys_0.InsertNextCell(4)
polys_0.InsertCellPoint(5)
polys_0.InsertCellPoint(6)
polys_0.InsertCellPoint(7)
polys_0.InsertCellPoint(8)

poly_0 = vtkPolyData()
poly_0.SetPoints(points_0)
poly_0.SetPolys(polys_0)
multi_block.SetBlock(0, poly_0)
mapper.SetBlockColor(0, 1, 0, 0)

# Block 1
points_1 = vtkPoints()
points_1.InsertNextPoint(2., 2., 1.)
points_1.InsertNextPoint(12., 2., 1.)
points_1.InsertNextPoint(12., 8., 1.)
points_1.InsertNextPoint(2., 8., 1.)
points_1.InsertNextPoint(22., -1., 1.)
points_1.InsertNextPoint(28., -1., 1.)
points_1.InsertNextPoint(28., 2., 1.)
points_1.InsertNextPoint(22., 2., 1.)

polys_1 = vtkCellArray()
polys_1.InsertNextCell(3)
polys_1.InsertCellPoint(0)
polys_1.InsertCellPoint(1)
polys_1.InsertCellPoint(2)
polys_1.InsertNextCell(3)
polys_1.InsertCellPoint(2)
polys_1.InsertCellPoint(3)
polys_1.InsertCellPoint(0)
polys_1.InsertNextCell(3)
polys_1.InsertCellPoint(4)
polys_1.InsertCellPoint(5)
polys_1.InsertCellPoint(6)
polys_1.InsertNextCell(3)
polys_1.InsertCellPoint(6)
polys_1.InsertCellPoint(7)
polys_1.InsertCellPoint(4)

poly_1 = vtkPolyData()
poly_1.SetPoints(points_1)
poly_1.SetPolys(polys_1)
multi_block.SetBlock(1, poly_1)
mapper.SetBlockColor(1, 0, 0, 1)

# Block 2
points_2 = vtkPoints()
points_2.InsertNextPoint(0., 0., 2.)
points_2.InsertNextPoint(14., 0., 2.)
points_2.InsertNextPoint(14., 10., 2.)
points_2.InsertNextPoint(0., 10., 2.)
points_2.InsertNextPoint(24., -2., 2.)
points_2.InsertNextPoint(26., -2., 2.)
points_2.InsertNextPoint(26., 3., 2.)
points_2.InsertNextPoint(24., 3., 2.)

polys_2 = vtkCellArray()
polys_2.InsertNextCell(4)
polys_2.InsertCellPoint(0)
polys_2.InsertCellPoint(1)
polys_2.InsertCellPoint(2)
polys_2.InsertCellPoint(3)
polys_2.InsertNextCell(4)
polys_2.InsertCellPoint(4)
polys_2.InsertCellPoint(5)
polys_2.InsertCellPoint(6)
polys_2.InsertCellPoint(7)

poly_2 = vtkPolyData()
poly_2.SetPoints(points_2)
poly_2.SetPolys(polys_2)
multi_block.SetBlock(2, poly_2)
mapper.SetBlockColor(2, 0, 1, 0)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(1, 1, 1)

renderer = vtkRenderer()
renderer.AddViewProp(actor)
renderer.SetBackground(0, 0, 0)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pick composite data")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# Pickers
prop_picker = vtkPicker()
cell_picker = vtkCellPicker()
point_picker = vtkPointPicker()

# Pick test data
pick_data = [
    ([0., 0.], (True, 3), (True, 3, 0), (True, 3, 0, 0)),
    ([4., 4.], (True, 1), (True, 1, 0), (True, 1, 0, 0)),
    ([5., 5.], (True, 1), (False, -1, -1), (True, 1, 0, 0)),
    ([18., -1.], (True, 2), (False, -1, -1), (False, -1, -1, -1)),
    ([18., -3.], (False, -1), (False, -1, -1), (False, -1, -1, -1)),
    ([25., 0.], (True, 1), (True, 1, 5), (True, 1, 1, 5)),
    ([28., 2.], (True, 1), (True, 2, 6), (True, 2, 2, 6)),
]

# Run picks
for data in pick_data:
    xy = data[0]
    size = render_window.GetSize()
    p = [size[0] / 2, size[1] / 2, 0]

    camera = renderer.GetActiveCamera()
    camera.SetPosition(xy[0], xy[1], -10.0)
    camera.SetFocalPoint(xy[0], xy[1], 0.0)
    camera.SetViewUp(0, 1, 0)
    camera.SetViewAngle(90)
    camera.ParallelProjectionOff()
    renderer.ResetCameraClippingRange()
    render_window.Render()

    prop_picker.Pick(p[0], p[1], 0, renderer)
    point_picker.Pick(p[0], p[1], 0, renderer)
    cell_picker.Pick(p[0], p[1], 0, renderer)

interactor.Initialize()
interactor.Start()
