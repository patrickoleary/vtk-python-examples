#!/usr/bin/env python
# Demonstrate vtkTreeHeatmapItem with a column tree using vtkContextActor.

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

tree = vtkTree()
tree.ShallowCopy(graph)

# Column tree (deep copy of the same tree).
tree2 = vtkTree()
tree2.DeepCopy(tree)

# Table data.
table = vtkTable()
table_names = vtkStringArray()
table_names.SetNumberOfTuples(3)
table_names.SetValue(0, "c")
table_names.SetValue(1, "b")
table_names.SetValue(2, "a")
table_names.SetName("name")

column_a = vtkDoubleArray()
column_a.SetNumberOfTuples(3)
column_a.SetName("a")
column_a.SetValue(0, 1.0)
column_a.SetValue(1, 3.0)
column_a.SetValue(2, 1.0)

column_b = vtkDoubleArray()
column_b.SetNumberOfTuples(3)
column_b.SetName("b")
column_b.SetValue(0, 2.0)
column_b.SetValue(1, 2.0)
column_b.SetValue(2, 2.0)

column_c = vtkDoubleArray()
column_c.SetNumberOfTuples(3)
column_c.SetName("c")
column_c.SetValue(0, 3.0)
column_c.SetValue(1, 1.0)
column_c.SetValue(2, 3.0)

table.AddColumn(table_names)
table.AddColumn(column_a)
table.AddColumn(column_b)
table.AddColumn(column_c)

# Tree heatmap item with column tree.
tree_item = vtkTreeHeatmapItem()
tree_item.SetTree(tree)
tree_item.SetColumnTree(tree2)
tree_item.SetTable(table)

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.AddItem(tree_item)
context_transform.Translate(80, 25)
context_transform.Scale(1.5, 1.5)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("column tree")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
