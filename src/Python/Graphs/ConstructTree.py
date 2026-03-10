#!/usr/bin/env python

# Construct a tree from a directed graph using AddChild, convert it to a
# vtkTree, and display it with a tree layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkMutableDirectedGraph,
    vtkTree,
)
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Graph: build a tree using AddChild (root → two children, one grandchild)
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddChild(v1)
graph.AddChild(v1)
graph.AddChild(v2)

# Tree: convert the directed graph to a vtkTree
tree = vtkTree()
success = tree.CheckedShallowCopy(graph)
print("Valid tree?", success)

# View: display the tree with a hierarchical tree layout
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(tree)
view.SetLayoutStrategyToTree()
view.ResetCamera()
render_window = view.GetRenderWindow()
render_window.SetWindowName("ConstructTree")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
