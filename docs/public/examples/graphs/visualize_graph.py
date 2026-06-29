#!/usr/bin/env python

# Visualize a minimal directed graph with two vertices and two parallel edges
# using a Simple 2D layout strategy.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Graph: two vertices with two parallel directed edges
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
graph.AddGraphEdge(v1, v2)
graph.AddGraphEdge(v1, v2)

# Filter: layout the graph vertices in 2D
layout_strategy = vtkSimple2DLayoutStrategy()
layout_strategy.SetRandomSeed(0)
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
graph_layout.SetLayoutStrategy(layout_strategy)

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
render_window.SetWindowName("visualize graph")
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
