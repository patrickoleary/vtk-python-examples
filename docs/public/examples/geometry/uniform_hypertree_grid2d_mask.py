#!/usr/bin/env python
# Demonstrate building a 2D uniform hyper tree grid with mask, with shrink filter.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkBitArray, vtkLookupTable, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import (
    vtkHyperTreeGridNonOrientedCursor,
    vtkUniformHyperTreeGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersHyperTree import vtkHyperTreeGridGeometry
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create the hyper tree grid.
htg = vtkUniformHyperTreeGrid()
htg.Initialize()

scalar_array = vtkUnsignedCharArray()
scalar_array.SetName("scalar")
scalar_array.SetNumberOfValues(0)
htg.GetCellData().AddArray(scalar_array)
htg.GetCellData().SetActiveScalars("scalar")

mask = vtkBitArray()
mask.SetName("mask")
mask.SetNumberOfValues(26)
mask.FillComponent(0, 0)
htg.SetMask(mask)

htg.SetDimensions([4, 3, 1])
htg.SetBranchFactor(2)
htg.SetOrigin([-1.0, -1.0, -2])
htg.SetGridScale([1.0, 1.0, 1.0])

# Split the various trees.
cursor = vtkHyperTreeGridNonOrientedCursor()
offset_index = 0

# ROOT CELL 0
htg.InitializeNonOrientedCursor(cursor, 0, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 1)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 7)
mask.SetValue(idx, 1)  # MASK 0/0
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 8)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 9)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 10)
mask.SetValue(idx, 1)  # MASK 0/3
cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 1
htg.InitializeNonOrientedCursor(cursor, 1, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 2)
mask.SetValue(idx, 1)  # MASK
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 2
htg.InitializeNonOrientedCursor(cursor, 2, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 3)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 11)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 12)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 13)
mask.SetValue(idx, 1)  # MASK 2/2
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14)
cursor.ToParent()

idx = cursor.GetGlobalNodeIndex()
mask.SetValue(idx, 1)  # MASK 2 (ROOT CELL)

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 3
htg.InitializeNonOrientedCursor(cursor, 3, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 4)
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 4
htg.InitializeNonOrientedCursor(cursor, 4, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 5)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 15)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 16)
mask.SetValue(idx, 1)  # MASK 4/1
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 17)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 18)
cursor.SubdivideLeaf()

# ROOT CELL 4/3/[0-3]
cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 19)
cursor.SubdivideLeaf()

# ROOT CELL 4/3/0/[0-3]
cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 23)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 24)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 25)
mask.SetValue(idx, 1)  # MASK 4/3/0/2
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 26)
cursor.ToParent()

cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 20)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 21)
mask.SetValue(idx, 1)  # MASK 4/3/2
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 22)
cursor.ToParent()

cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 5
htg.InitializeNonOrientedCursor(cursor, 5, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 6)

# Geometry filter.
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputData(htg)

# Shrink filter.
shrink = vtkShrinkFilter()
shrink.SetInputConnection(geometry.GetOutputPort())
shrink.SetShrinkFactor(0.8)

# Lookup table.
lut = vtkLookupTable()
lut.SetHueRange(0.66, 0)
lut.UsingLogScale()
lut.Build()

# Mapper.
mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("scalar")
data_range = [1, 26]
mapper.SetScalarRange(data_range[0], data_range[1])

# Actor.
actor = vtkActor()
actor.SetMapper(mapper)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("uniform hypertree grid2d mask")

# Camera.
bd = htg.GetBounds()
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
focal = []
for i in range(3):
    focal.append(bd[2 * i] + (bd[2 * i + 1] - bd[2 * i]) / 2.0)
camera.SetFocalPoint(focal)
camera.SetPosition(focal[0], focal[1], focal[2] + 4.0)
renderer.SetActiveCamera(camera)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
