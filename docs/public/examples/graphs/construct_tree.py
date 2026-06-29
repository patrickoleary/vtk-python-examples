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
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkTreeLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

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

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("construct tree")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: reset camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
