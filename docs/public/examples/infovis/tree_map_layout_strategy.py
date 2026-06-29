#!/usr/bin/env python
# Demonstrate vtkTreeMapLayout with box, slice-and-dice, and squarify strategies.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkInfovisCore import vtkTreeFieldAggregator
from vtkmodules.vtkInfovisLayout import (
    vtkBoxLayoutStrategy,
    vtkSliceAndDiceLayoutStrategy,
    vtkSquarifyLayoutStrategy,
    vtkTreeMapLayout,
    vtkTreeMapToPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build tree with size attribute.
builder = vtkMutableDirectedGraph()
size_arr = vtkIntArray()
size_arr.SetName("size")
builder.GetVertexData().AddArray(size_arr)

builder.AddVertex()
size_arr.InsertNextValue(0)
builder.AddChild(0)
size_arr.InsertNextValue(15)
builder.AddChild(0)
size_arr.InsertNextValue(50)
builder.AddChild(0)
size_arr.InsertNextValue(0)
builder.AddChild(3)
size_arr.InsertNextValue(2)
builder.AddChild(3)
size_arr.InsertNextValue(12)
builder.AddChild(3)
size_arr.InsertNextValue(10)
builder.AddChild(3)
size_arr.InsertNextValue(8)
builder.AddChild(3)
size_arr.InsertNextValue(6)
builder.AddChild(3)
size_arr.InsertNextValue(4)

tree = vtkTree()
tree.CheckedShallowCopy(builder)

# Aggregate field.
aggregator = vtkTreeFieldAggregator()
aggregator.SetInputData(tree)
aggregator.SetField("size")
aggregator.SetLeafVertexUnitSize(False)

# Box layout strategy.
box = vtkBoxLayoutStrategy()
box.SetShrinkPercentage(0.1)
box_layout = vtkTreeMapLayout()
box_layout.SetLayoutStrategy(box)
box_layout.SetInputConnection(aggregator.GetOutputPort())
box_poly = vtkTreeMapToPolyData()
box_poly.SetInputConnection(box_layout.GetOutputPort())

box_mapper = vtkPolyDataMapper()
box_mapper.SetInputConnection(box_poly.GetOutputPort())
box_mapper.SetScalarRange(0, 100)
box_mapper.SetScalarModeToUseCellFieldData()
box_mapper.SelectColorArray("size")

box_actor = vtkActor()
box_actor.SetMapper(box_mapper)
box_actor.SetPosition(0, 0, 0)

# Slice and dice layout strategy.
slice_and_dice = vtkSliceAndDiceLayoutStrategy()
slice_and_dice.SetShrinkPercentage(0.1)
slice_and_dice_layout = vtkTreeMapLayout()
slice_and_dice_layout.SetLayoutStrategy(slice_and_dice)
slice_and_dice_layout.SetInputConnection(aggregator.GetOutputPort())
slice_and_dice_poly = vtkTreeMapToPolyData()
slice_and_dice_poly.SetInputConnection(slice_and_dice_layout.GetOutputPort())

slice_and_dice_mapper = vtkPolyDataMapper()
slice_and_dice_mapper.SetInputConnection(slice_and_dice_poly.GetOutputPort())
slice_and_dice_mapper.SetScalarRange(0, 100)
slice_and_dice_mapper.SetScalarModeToUseCellFieldData()
slice_and_dice_mapper.SelectColorArray("size")

slice_and_dice_actor = vtkActor()
slice_and_dice_actor.SetMapper(slice_and_dice_mapper)
slice_and_dice_actor.SetPosition(0, 1.1, 0)

# Squarify layout strategy.
squarify = vtkSquarifyLayoutStrategy()
squarify.SetShrinkPercentage(0.1)
squarify_layout = vtkTreeMapLayout()
squarify_layout.SetLayoutStrategy(squarify)
squarify_layout.SetInputConnection(aggregator.GetOutputPort())
squarify_poly = vtkTreeMapToPolyData()
squarify_poly.SetInputConnection(squarify_layout.GetOutputPort())

squarify_mapper = vtkPolyDataMapper()
squarify_mapper.SetInputConnection(squarify_poly.GetOutputPort())
squarify_mapper.SetScalarRange(0, 100)
squarify_mapper.SetScalarModeToUseCellFieldData()
squarify_mapper.SelectColorArray("size")

squarify_actor = vtkActor()
squarify_actor.SetMapper(squarify_mapper)
squarify_actor.SetPosition(1.1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(box_actor)
renderer.AddActor(slice_and_dice_actor)
renderer.AddActor(squarify_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tree map layout strategy")

# Scene
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
