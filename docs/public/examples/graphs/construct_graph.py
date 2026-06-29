#!/usr/bin/env python

# Construct a simple undirected graph with two vertices and two parallel edges,
# then display it using a force-directed layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkForceDirectedLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Graph: two vertices with two parallel edges
graph = vtkMutableUndirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()

graph.AddEdge(v1, v2)
print("Number of vertices:", graph.GetNumberOfVertices())
print("Number of edges:", graph.GetNumberOfEdges())

graph.AddEdge(v1, v2)
print("Number of vertices:", graph.GetNumberOfVertices())
print("Number of edges:", graph.GetNumberOfEdges())

# Filter: layout the graph vertices in 2D
force_directed_layout_strategy = vtkForceDirectedLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(force_directed_layout_strategy)

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
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("construct graph")
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
