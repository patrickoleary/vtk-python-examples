#!/usr/bin/env python

# Construct a simple undirected graph with two vertices and two parallel edges,
# then display it using a force-directed layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

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

# View: display the graph with a force-directed layout
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
view.SetLayoutStrategyToForceDirected()
view.ResetCamera()
view.GetRenderer().SetBackground(navy_rgb)
view.GetRenderer().SetBackground2(midnight_blue_rgb)
render_window = view.GetRenderWindow()
render_window.SetWindowName("ConstructGraph")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
