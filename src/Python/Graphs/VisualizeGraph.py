#!/usr/bin/env python

# Visualize a minimal directed graph with two vertices and two parallel edges
# using a Simple 2D layout strategy.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkInfovisLayout import vtkSimple2DLayoutStrategy
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Graph: two vertices with two parallel directed edges
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
graph.AddGraphEdge(v1, v2)
graph.AddGraphEdge(v1, v2)

# View: display the graph with a Simple 2D layout
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(graph)
layout_strategy = vtkSimple2DLayoutStrategy()
layout_strategy.SetRandomSeed(0)
view.SetLayoutStrategy(layout_strategy)
view.ResetCamera()
render_window = view.GetRenderWindow()
render_window.SetWindowName("VisualizeGraph")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
