#!/usr/bin/env python

# Create a labelled tree with vertex and edge labels displayed using a mellow
# theme and a hierarchical tree layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkStringArray
from vtkmodules.vtkCommonDataModel import (
    vtkMutableDirectedGraph,
    vtkTree,
)
from vtkmodules.vtkViewsCore import vtkViewTheme
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Graph: build a tree with six vertices (a-f)
graph = vtkMutableDirectedGraph()
a = graph.AddVertex()
b = graph.AddChild(a)
c = graph.AddChild(a)
d = graph.AddChild(b)
e = graph.AddChild(c)
f = graph.AddChild(c)

# Vertex labels
vertex_labels = vtkStringArray()
vertex_labels.SetName("VertexLabel")
vertex_labels.InsertValue(a, "a")
vertex_labels.InsertValue(b, "b")
vertex_labels.InsertValue(c, "c")
vertex_labels.InsertValue(d, "d")
vertex_labels.InsertValue(e, "e")
vertex_labels.InsertValue(f, "f")
graph.GetVertexData().AddArray(vertex_labels)

# Edge labels
edge_labels = vtkStringArray()
edge_labels.SetName("EdgeLabel")
edge_labels.InsertValue(graph.GetEdgeId(a, b), "a -> b")
edge_labels.InsertValue(graph.GetEdgeId(a, c), "a -> c")
edge_labels.InsertValue(graph.GetEdgeId(b, d), "b -> d")
edge_labels.InsertValue(graph.GetEdgeId(c, e), "c -> e")
edge_labels.InsertValue(graph.GetEdgeId(c, f), "c -> f")
graph.GetEdgeData().AddArray(edge_labels)

# Tree: convert the directed graph to a vtkTree
tree = vtkTree()
valid_tree = tree.CheckedShallowCopy(graph)
if not valid_tree:
    raise RuntimeError("Invalid tree structure")

# Theme: apply a mellow color scheme
theme = vtkViewTheme()

# View: display the labelled tree
view = vtkGraphLayoutView()
view.SetRepresentationFromInput(tree)
view.ApplyViewTheme(theme.CreateMellowTheme())
view.SetVertexColorArrayName("VertexDegree")
view.SetColorVertices(True)
view.SetVertexLabelArrayName("VertexLabel")
view.SetVertexLabelVisibility(True)
view.SetEdgeLabelArrayName("EdgeLabel")
view.SetEdgeLabelVisibility(True)
view.SetLayoutStrategyToTree()
view.ResetCamera()
render_window = view.GetRenderWindow()
render_window.SetSize(600, 600)
render_window.SetWindowName("CreateTree")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
