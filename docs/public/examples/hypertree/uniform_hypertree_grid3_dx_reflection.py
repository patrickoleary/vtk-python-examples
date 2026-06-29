#!/usr/bin/env python

# Demonstrate vtkHyperTreeGridAxisReflection on a 3D uniform
# HyperTreeGrid reflected along the X axis.

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

# Create 3D uniform HyperTreeGrid
htg = vtkUniformHyperTreeGrid()
htg.Initialize()

scalar_array = vtkDoubleArray()
scalar_array.SetName('scalar')
scalar_array.SetNumberOfValues(0)
htg.GetCellData().AddArray(scalar_array)
htg.GetCellData().SetActiveScalars('scalar')

htg.SetDimensions([4, 3, 3])
htg.SetBranchFactor(2)

# Rectilinear grid coordinates
x_values = vtkDoubleArray()
x_values.SetNumberOfValues(4)
x_values.SetValue(0, -1)
x_values.SetValue(1, 0)
x_values.SetValue(2, 1)
x_values.SetValue(3, 2)
htg.SetXCoordinates(x_values)

y_values = vtkDoubleArray()
y_values.SetNumberOfValues(3)
y_values.SetValue(0, -1)
y_values.SetValue(1, 0)
y_values.SetValue(2, 1)
htg.SetYCoordinates(y_values)

z_values = vtkDoubleArray()
z_values.SetNumberOfValues(4)
z_values.SetValue(0, -1)
z_values.SetValue(1, 0)
z_values.SetValue(2, 1)
z_values.SetValue(3, 2)
htg.SetZCoordinates(z_values)

# Build the trees
cursor = vtkHyperTreeGridNonOrientedCursor()
offset_index = 0

# ROOT CELL 0-5
for i_ht in range(6):
    htg.InitializeNonOrientedCursor(cursor, i_ht, True)
    cursor.SetGlobalIndexStart(offset_index)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, i_ht + 1)
    offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 6
htg.InitializeNonOrientedCursor(cursor, 6, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 7)
cursor.SubdivideLeaf()

for ichild in range(8):
    cursor.ToChild(ichild)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, 13 + ichild)
    cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 7
htg.InitializeNonOrientedCursor(cursor, 7, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 8)
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 8
htg.InitializeNonOrientedCursor(cursor, 8, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 9)
cursor.SubdivideLeaf()

for ichild in range(8):
    cursor.ToChild(ichild)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, 21 + ichild)
    cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 9
htg.InitializeNonOrientedCursor(cursor, 9, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 10)
offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 10
htg.InitializeNonOrientedCursor(cursor, 10, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 11)
cursor.SubdivideLeaf()

for ichild in range(8):
    cursor.ToChild(ichild)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, 29 + ichild)
    cursor.ToParent()

cursor.ToChild(7)
cursor.SubdivideLeaf()

for ichild in range(8):
    cursor.ToChild(ichild)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, 37 + ichild)
    cursor.ToParent()

cursor.ToChild(4)
cursor.SubdivideLeaf()

for ichild in range(8):
    cursor.ToChild(ichild)
    idx = cursor.GetGlobalNodeIndex()
    scalar_array.InsertTuple1(idx, 46 + ichild)
    cursor.ToParent()

offset_index += cursor.GetTree().GetNumberOfVertices()

# ROOT CELL 11
htg.InitializeNonOrientedCursor(cursor, 11, True)
cursor.SetGlobalIndexStart(offset_index)
idx = cursor.GetGlobalNodeIndex()
scalar_array.InsertTuple1(idx, 12)

# Axis reflection along X
reflection = vtkHyperTreeGridAxisReflection()
reflection.SetInputData(htg)
reflection.SetPlaneToX()
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
lut.UsingLogScale()
lut.Build()

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetLookupTable(lut)
mapper.SetColorModeToMapScalars()
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray('scalar')
data_range = [1, 53]
mapper.SetScalarRange(data_range[0], data_range[1])

# Actors
actor_solid = vtkActor()
actor_solid.SetMapper(mapper)

actor_wireframe = vtkActor()
actor_wireframe.SetMapper(mapper)
actor_wireframe.GetProperty().SetColor(0, 0, 0)
actor_wireframe.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_solid)
renderer.AddActor(actor_wireframe)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetWindowName("uniform hypertree grid3 dx reflection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
shrink.Update()
bd = shrink.GetOutput().GetBounds()
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
focal = [(bd[2 * i] + bd[2 * i + 1]) / 2.0 for i in range(3)]
camera.SetFocalPoint(focal)
camera.SetPosition(focal[0] + 4, focal[1] + 3, focal[2] + 6.0)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
