#!/usr/bin/env python

# Demonstrate vtkHyperTreeGridAxisReflection on a 2D uniform
# HyperTreeGrid reflected along the Y axis.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkLookupTable,
)
from vtkmodules.vtkCommonDataModel import (
    vtkHyperTreeGridNonOrientedCursor,
    vtkUniformHyperTreeGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkFiltersHyperTree import (
    vtkHyperTreeGridAxisReflection,
    vtkHyperTreeGridGeometry,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create 2D uniform HyperTreeGrid
htg = vtkUniformHyperTreeGrid()
htg.Initialize()

scalar_array = vtkDoubleArray()
scalar_array.SetName('scalar')
scalar_array.SetNumberOfValues(0)
htg.GetCellData().AddArray(scalar_array)
htg.GetCellData().SetActiveScalars('scalar')

htg.SetDimensions([4, 3, 1])
htg.SetBranchFactor(2)
htg.SetOrigin([-1, -1, 0])
htg.SetGridScale([1, 1, 1])

# Build the trees
cursor = vtkHyperTreeGridNonOrientedCursor()
offset_index = 0

# ROOT CELL 0
htg.InitializeNonOrientedCursor(cursor, 0, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 10)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 100)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 101)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 101)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 103)
cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 1
htg.InitializeNonOrientedCursor(cursor, 1, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 11)
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 2
htg.InitializeNonOrientedCursor(cursor, 2, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 12)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 120)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 121)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 122)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 123)
cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 3
htg.InitializeNonOrientedCursor(cursor, 3, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 13)
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 4
htg.InitializeNonOrientedCursor(cursor, 4, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 140)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 141)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 142)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 143)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 1430)
cursor.SubdivideLeaf()

cursor.ToChild(0)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14300)
cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14301)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14302)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 14303)
cursor.ToParent()

cursor.ToParent()

cursor.ToChild(1)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 1431)
cursor.ToParent()

cursor.ToChild(2)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 1432)
cursor.ToParent()

cursor.ToChild(3)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 1433)
cursor.ToParent()

cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 5
htg.InitializeNonOrientedCursor(cursor, 5, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 15)

# Axis reflection along Y
reflection = vtkHyperTreeGridAxisReflection()
reflection.SetInputData(htg)
reflection.SetPlaneToY()
reflection.SetCenter(0)

# Geometry filter
geometry = vtkHyperTreeGridGeometry()
geometry.SetInputConnection(reflection.GetOutputPort())

# Shrink filter
shrink = vtkShrinkFilter()
shrink.SetInputConnection(geometry.GetOutputPort())
shrink.SetShrinkFactor(0.8)

# Lookup table
lut = vtkLookupTable()
lut.SetHueRange(0.66, 0)
lut.Build()

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(shrink.GetOutputPort())
shrink.Update()
data_range = shrink.GetOutput().GetCellData().GetArray('scalar').GetRange()
mapper.SetLookupTable(lut)
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray('scalar')
mapper.SetScalarRange(data_range[0], data_range[1])

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetWindowName("uniform hypertree grid2 dy reflection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
bd = shrink.GetOutput().GetBounds()
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
focal = [(bd[2 * i] + bd[2 * i + 1]) / 2.0 for i in range(3)]
camera.SetFocalPoint(focal)
camera.SetPosition(focal[0], focal[1], focal[2] + 4.0)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
