#!/usr/bin/env python
# Demonstrate vtkDendrogramItem rendering a weighted tree with vtkContextActor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkDendrogramItem
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

# Edge weights.
weights = vtkDoubleArray()
weights.SetNumberOfTuples(5)
weights.SetValue(graph.GetEdgeId(root, internal_one), 1.0)
weights.SetValue(graph.GetEdgeId(internal_one, internal_two), 2.0)
weights.SetValue(graph.GetEdgeId(internal_two, a), 1.0)
weights.SetValue(graph.GetEdgeId(internal_two, b), 1.0)
weights.SetValue(graph.GetEdgeId(internal_one, c), 3.0)
weights.SetName("weight")
graph.GetEdgeData().AddArray(weights)

# Vertex names.
names = vtkStringArray()
names.SetNumberOfTuples(6)
names.SetValue(a, "a")
names.SetValue(b, "b")
names.SetValue(c, "c")
names.SetName("node name")
graph.GetVertexData().AddArray(names)

# Node weights.
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

# Dendrogram item.
dendrogram = vtkDendrogramItem()
dendrogram.SetTree(tree)
dendrogram.SetPosition(40, 15)

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.AddItem(dendrogram)
context_transform.Scale(3, 3)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dendrogram item")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
