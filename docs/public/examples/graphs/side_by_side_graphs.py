#!/usr/bin/env python

# Display two graphs side by side in split viewports within a single render
# window. The left viewport shows a triangle graph and the right shows a
# single-edge graph, both using force-directed layouts.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
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
dark_green_rgb = (0.0, 0.392, 0.0)
forest_green_rgb = (0.133, 0.545, 0.133)

# Graph 0: triangle (three vertices, three edges)
g0 = vtkMutableUndirectedGraph()
v1 = g0.AddVertex()
v2 = g0.AddVertex()
v3 = g0.AddVertex()
g0.AddEdge(v1, v2)
g0.AddEdge(v2, v3)
g0.AddEdge(v1, v3)

points0 = vtkPoints()
points0.InsertNextPoint(0.0, 0.0, 0.0)
points0.InsertNextPoint(1.0, 0.0, 0.0)
points0.InsertNextPoint(0.0, 1.0, 0.0)
g0.SetPoints(points0)

# Graph 1: single edge (two vertices, one edge)
g1 = vtkMutableUndirectedGraph()
v1 = g1.AddVertex()
v2 = g1.AddVertex()
g1.AddEdge(v1, v2)

points1 = vtkPoints()
points1.InsertNextPoint(0.0, 0.0, 0.0)
points1.InsertNextPoint(1.0, 0.0, 0.0)
g1.SetPoints(points1)

# Pipeline 0: layout and convert triangle graph
layout_strategy_0 = vtkForceDirectedLayoutStrategy()
graph_layout_0 = vtkGraphLayout()
graph_layout_0.SetInputData(g0)
graph_layout_0.SetLayoutStrategy(layout_strategy_0)

graph_to_polydata_0 = vtkGraphToPolyData()
graph_to_polydata_0.SetInputConnection(graph_layout_0.GetOutputPort())

edge_mapper_0 = vtkPolyDataMapper()
edge_mapper_0.SetInputConnection(graph_to_polydata_0.GetOutputPort())
edge_mapper_0.ScalarVisibilityOff()

edge_actor_0 = vtkActor()
edge_actor_0.SetMapper(edge_mapper_0)

# Pipeline 1: layout and convert single-edge graph
layout_strategy_1 = vtkForceDirectedLayoutStrategy()
graph_layout_1 = vtkGraphLayout()
graph_layout_1.SetInputData(g1)
graph_layout_1.SetLayoutStrategy(layout_strategy_1)

graph_to_polydata_1 = vtkGraphToPolyData()
graph_to_polydata_1.SetInputConnection(graph_layout_1.GetOutputPort())

edge_mapper_1 = vtkPolyDataMapper()
edge_mapper_1.SetInputConnection(graph_to_polydata_1.GetOutputPort())
edge_mapper_1.ScalarVisibilityOff()

edge_actor_1 = vtkActor()
edge_actor_1.SetMapper(edge_mapper_1)

# Renderer 0: left viewport — triangle graph
renderer_0 = vtkRenderer()
renderer_0.AddActor(edge_actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.SetBackground(navy_rgb)
renderer_0.SetBackground2(midnight_blue_rgb)
renderer_0.GradientBackgroundOn()

# Renderer 1: right viewport — single-edge graph
renderer_1 = vtkRenderer()
renderer_1.AddActor(edge_actor_1)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.SetBackground(dark_green_rgb)
renderer_1.SetBackground2(forest_green_rgb)
renderer_1.GradientBackgroundOn()

# Render window: display both viewports
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("side by side graphs")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: reset cameras
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
