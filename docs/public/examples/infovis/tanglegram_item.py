#!/usr/bin/env python
# Demonstrate vtkTanglegramItem comparing two trees with a correspondence table.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTable, vtkTree
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene, vtkContextTransform
from vtkmodules.vtkViewsInfovis import vtkTanglegramItem
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# --- Tree 1 ---
graph1 = vtkMutableDirectedGraph()
root = graph1.AddVertex()
internal_one = graph1.AddChild(root)
internal_two = graph1.AddChild(internal_one)
a = graph1.AddChild(internal_two)
b = graph1.AddChild(internal_two)
c = graph1.AddChild(internal_one)

weights = vtkDoubleArray()
weights.SetNumberOfTuples(5)
weights.SetValue(graph1.GetEdgeId(root, internal_one), 1.0)
weights.SetValue(graph1.GetEdgeId(internal_one, internal_two), 2.0)
weights.SetValue(graph1.GetEdgeId(internal_two, a), 1.0)
weights.SetValue(graph1.GetEdgeId(internal_two, b), 1.0)
weights.SetValue(graph1.GetEdgeId(internal_one, c), 3.0)
weights.SetName("weight")
graph1.GetEdgeData().AddArray(weights)

names1 = vtkStringArray()
names1.SetNumberOfTuples(6)
names1.SetValue(a, "cat")
names1.SetValue(b, "dog")
names1.SetValue(c, "human")
names1.SetName("node name")
graph1.GetVertexData().AddArray(names1)

node_weights = vtkDoubleArray()
node_weights.SetNumberOfTuples(6)
node_weights.SetValue(root, 0.0)
node_weights.SetValue(internal_one, 1.0)
node_weights.SetValue(internal_two, 3.0)
node_weights.SetValue(a, 4.0)
node_weights.SetValue(b, 4.0)
node_weights.SetValue(c, 4.0)
node_weights.SetName("node weight")
graph1.GetVertexData().AddArray(node_weights)

# --- Tree 2 ---
graph2 = vtkMutableDirectedGraph()
root = graph2.AddVertex()
internal_one = graph2.AddChild(root)
internal_two = graph2.AddChild(internal_one)
a = graph2.AddChild(internal_two)
b = graph2.AddChild(internal_two)
c = graph2.AddChild(internal_one)

graph2.GetEdgeData().AddArray(weights)

names2 = vtkStringArray()
names2.SetNumberOfTuples(6)
names2.SetValue(a, "dog food")
names2.SetValue(b, "cat food")
names2.SetValue(c, "steak")
names2.SetName("node name")
graph2.GetVertexData().AddArray(names2)
graph2.GetVertexData().AddArray(node_weights)

# --- Correspondence table ---
table = vtkTable()
eaters = vtkStringArray()
eaters.SetNumberOfTuples(3)
eaters.SetValue(0, "human")
eaters.SetValue(1, "dog")
eaters.SetValue(2, "cat")

hunger_steak = vtkDoubleArray()
hunger_steak.SetName("steak")
hunger_steak.SetNumberOfTuples(3)
hunger_steak.SetValue(0, 2.0)
hunger_steak.SetValue(1, 1.0)
hunger_steak.SetValue(2, 1.0)

hunger_dog_food = vtkDoubleArray()
hunger_dog_food.SetName("dog food")
hunger_dog_food.SetNumberOfTuples(3)
hunger_dog_food.SetValue(0, 0.0)
hunger_dog_food.SetValue(1, 2.0)
hunger_dog_food.SetValue(2, 0.0)

hunger_cat_food = vtkDoubleArray()
hunger_cat_food.SetName("cat food")
hunger_cat_food.SetNumberOfTuples(3)
hunger_cat_food.SetValue(0, 0.0)
hunger_cat_food.SetValue(1, 1.0)
hunger_cat_food.SetValue(2, 2.0)

table.AddColumn(eaters)
table.AddColumn(hunger_steak)
table.AddColumn(hunger_dog_food)
table.AddColumn(hunger_cat_food)

# Convert to trees.
tree1 = vtkTree()
tree1.ShallowCopy(graph1)
tree2 = vtkTree()
tree2.ShallowCopy(graph2)

# Tanglegram item.
tanglegram = vtkTanglegramItem()
tanglegram.SetTree1(tree1)
tanglegram.SetTree2(tree2)
tanglegram.SetTable(table)
tanglegram.SetTree1Label("Diners")
tanglegram.SetTree2Label("Meals")

# Context actor pipeline.
context_actor = vtkContextActor()
context_transform = vtkContextTransform()
context_transform.SetInteractive(True)
context_transform.AddItem(tanglegram)
context_transform.Translate(20, 75)
context_transform.Scale(1.25, 1.25)
context_actor.GetScene().AddItem(context_transform)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tanglegram item")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 200)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
