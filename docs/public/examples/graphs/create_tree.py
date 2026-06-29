#!/usr/bin/env python

# Create a labelled tree with vertex and edge labels displayed using a
# hierarchical tree layout.

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
from vtkmodules.vtkFiltersCore import vtkCellCenters
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkTreeLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

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

# Filter: layout the tree with a hierarchical tree strategy
tree_layout_strategy = vtkTreeLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(tree)
graph_layout.SetLayoutStrategy(tree_layout_strategy)

# Filter: convert graph to polydata for rendering
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())

# Mapper: map edge lines to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.ScalarVisibilityOff()

# Actor: assign the edge geometry
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Vertex labels: display the VertexLabel array as text at each vertex
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
vertex_label_mapper.SetLabelModeToLabelFieldData()
vertex_label_mapper.SetFieldDataName("VertexLabel")

vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Edge labels: compute edge midpoints with vtkCellCenters, then label them
edge_centers = vtkCellCenters()
edge_centers.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_centers.CopyArraysOn()

edge_label_mapper = vtkLabeledDataMapper()
edge_label_mapper.SetInputConnection(edge_centers.GetOutputPort())
edge_label_mapper.SetLabelModeToLabelFieldData()
edge_label_mapper.SetFieldDataName("EdgeLabel")

edge_label_actor = vtkActor2D()
edge_label_actor.SetMapper(edge_label_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_label_actor)
renderer.AddActor(edge_label_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("create tree")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: reset camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
