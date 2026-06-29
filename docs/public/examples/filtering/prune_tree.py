#!/usr/bin/env python
# Demonstrate vtkPruneTreeFilter by pruning a subtree from a directed tree.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph, vtkTree
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkPruneTreeFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build tree: root -> internalOne -> internalTwo -> (a, leaf), internalOne -> leaf, a -> (leaf, leaf).
graph = vtkMutableDirectedGraph()
root = graph.AddVertex()
internal_one = graph.AddChild(root)
internal_two = graph.AddChild(internal_one)
vertex_a = graph.AddChild(internal_two)
graph.AddChild(internal_two)
graph.AddChild(internal_one)
graph.AddChild(vertex_a)
graph.AddChild(vertex_a)

# Assign positions to vertices for layout
points = vtkPoints()
points.InsertNextPoint(3, 5, 0)    # root
points.InsertNextPoint(2, 4, 0)    # internal_one
points.InsertNextPoint(1, 3, 0)    # internal_two
points.InsertNextPoint(0, 2, 0)    # vertex_a
points.InsertNextPoint(2, 2, 0)    # leaf
points.InsertNextPoint(4, 3, 0)    # leaf
points.InsertNextPoint(-1, 1, 0)   # leaf
points.InsertNextPoint(1, 1, 0)    # leaf
graph.SetPoints(points)

tree = vtkTree()
tree.ShallowCopy(graph)

# Visualize the original tree (left viewport)
graph_to_poly_0 = vtkGraphToPolyData()
graph_to_poly_0.SetInputData(tree)

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(graph_to_poly_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetPointSize(10.0)
actor_0.GetProperty().SetColor(0.3, 0.7, 0.9)
actor_0.GetProperty().SetLineWidth(3.0)

# Prune at internalTwo.
prune_filter = vtkPruneTreeFilter()
prune_filter.SetInputData(tree)
prune_filter.SetParentVertex(internal_two)
prune_filter.Update()

pruned_tree = prune_filter.GetOutput()

# Visualize the pruned tree (right viewport)
graph_to_poly_1 = vtkGraphToPolyData()
graph_to_poly_1.SetInputData(pruned_tree)

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(graph_to_poly_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetPointSize(10.0)
actor_1.GetProperty().SetColor(0.9, 0.3, 0.2)
actor_1.GetProperty().SetLineWidth(3.0)

# Two viewports: left = original, right = pruned
renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0.2, 0.3, 0.4)
renderer_0.SetViewport(0, 0, 0.5, 1.0)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0.2, 0.3, 0.4)
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("prune tree")

# Scene
renderer_0.ResetCamera()
renderer_0.ResetCameraClippingRange()
renderer_1.ResetCamera()
renderer_1.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
