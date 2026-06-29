#!/usr/bin/env python
# Demonstrate vtkTreeHeatmapItem with automatic collapse to a target number of leaf nodes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTable, vtkTree
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkTreeHeatmapItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build a directed graph and convert to tree.
graph = vtkMutableDirectedGraph()
root = graph.AddVertex()
internal_one = graph.AddChild(root)
internal_two = graph.AddChild(internal_one)
a = graph.AddChild(internal_two)
b = graph.AddChild(internal_two)
c = graph.AddChild(internal_one)

weights = vtkDoubleArray()
weights.SetNumberOfTuples(5)
weights.SetValue(graph.GetEdgeId(root, internal_one), 1.0)
weights.SetValue(graph.GetEdgeId(internal_one, internal_two), 2.0)
weights.SetValue(graph.GetEdgeId(internal_two, a), 1.0)
weights.SetValue(graph.GetEdgeId(internal_two, b), 1.0)
weights.SetValue(graph.GetEdgeId(internal_one, c), 3.0)
weights.SetName("weight")
graph.GetEdgeData().AddArray(weights)

names = vtkStringArray()
names.SetNumberOfTuples(6)
names.SetValue(a, "a")
names.SetValue(b, "b")
names.SetValue(c, "c")
names.SetName("node name")
graph.GetVertexData().AddArray(names)

node_weights = vtkDoubleArray()
node_weights.SetNumberOfTuples(6)
node_weights.SetValue(root, 0.0)
node_weights.SetValue(internal_one, 1.0)
node_weights.SetValue(internal_two, 3.0)
node_weights.SetValue(a, 4.0)
node_weights.SetValue(b, 4.0)
node_weights.SetValue(c, 4.0)
node_weights.SetName("node weight")
graph.GetVertexData().AddArray(node_weights)

# Table data.
table = vtkTable()
table_names = vtkStringArray()
table_names.SetNumberOfTuples(3)
table_names.SetValue(0, "c")
table_names.SetValue(1, "b")
table_names.SetValue(2, "a")
table_names.SetName("name")

column_m1 = vtkDoubleArray()
column_m1.SetNumberOfTuples(3)
column_m1.SetName("m1")
column_m1.SetValue(0, 1.0)
column_m1.SetValue(1, 3.0)
column_m1.SetValue(2, 1.0)

column_m2 = vtkDoubleArray()
column_m2.SetNumberOfTuples(3)
column_m2.SetName("m2")
column_m2.SetValue(0, 2.0)
column_m2.SetValue(1, 2.0)
column_m2.SetValue(2, 2.0)

column_m3 = vtkDoubleArray()
column_m3.SetNumberOfTuples(3)
column_m3.SetName("m3")
column_m3.SetValue(0, 3.0)
column_m3.SetValue(1, 1.0)
column_m3.SetValue(2, 3.0)

table.AddColumn(table_names)
table.AddColumn(column_m1)
table.AddColumn(column_m2)
table.AddColumn(column_m3)

tree = vtkTree()
tree.ShallowCopy(graph)

# Tree heatmap item.
tree_item = vtkTreeHeatmapItem()
tree_item.SetTree(tree)
tree_item.SetTable(table)
tree_item.GetDendrogram().DisplayNumberOfCollapsedLeafNodesOff()

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.Translate(20, 30)
context_transform.Scale(2.5, 2.5)
context_transform.AddItem(tree_item)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tree heatmap auto collapse")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# Automatically collapse down to two leaf nodes closest to the root.
tree_item.CollapseToNumberOfLeafNodes(2)

render_window.Render()
interactor.Initialize()
interactor.Start()
