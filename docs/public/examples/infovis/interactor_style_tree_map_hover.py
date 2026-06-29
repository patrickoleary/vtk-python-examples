#!/usr/bin/env python
# Demonstrate vtkInteractorStyleTreeMapHover with a squarify layout on a tree.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkInfovisCore import vtkTreeFieldAggregator
from vtkmodules.vtkInfovisLayout import vtkSquarifyLayoutStrategy, vtkTreeMapLayout, vtkTreeMapToPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkViewsInfovis import vtkInteractorStyleTreeMapHover

# Build tree with size data.
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

# Aggregate field values.
field_aggregator = vtkTreeFieldAggregator()
field_aggregator.SetInputData(tree)
field_aggregator.SetField("size")
field_aggregator.SetLeafVertexUnitSize(False)

# Tree map layout with squarify strategy.
layout = vtkTreeMapLayout()
squarify_strategy = vtkSquarifyLayoutStrategy()
squarify_strategy.SetShrinkPercentage(0.1)
layout.SetInputConnection(field_aggregator.GetOutputPort())
layout.SetLayoutStrategy(squarify_strategy)

# Convert tree map to polydata.
tree_map_to_polydata = vtkTreeMapToPolyData()
tree_map_to_polydata.SetInputConnection(layout.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tree_map_to_polydata.GetOutputPort())
mapper.SetScalarModeToUseCellFieldData()
mapper.SelectColorArray("size")
mapper.SetScalarRange(0, 100)

actor = vtkActor()
actor.SetMapper(mapper)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("interactor style tree map hover")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()

# Tree map hover interactor style.
tree_map_hover_style = vtkInteractorStyleTreeMapHover()
tree_map_hover_style.SetLabelField("size")
tree_map_hover_style.SetTreeMapToPolyData(tree_map_to_polydata)
tree_map_hover_style.SetLayout(layout)

render_window.SetInteractor(interactor)
interactor.SetInteractorStyle(tree_map_hover_style)

interactor.Initialize()
interactor.Start()
