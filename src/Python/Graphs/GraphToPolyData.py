#!/usr/bin/env python

# Convert an undirected graph with explicit vertex positions to vtkPolyData
# and render it using the standard 3D pipeline (mapper → actor → renderer).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
green_rgb = (0.0, 0.502, 0.0)

# Graph: four vertices with three edges (star topology)
graph = vtkMutableUndirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()
v4 = graph.AddVertex()

graph.AddEdge(v1, v2)
graph.AddEdge(v1, v3)
graph.AddEdge(v1, v4)

# Points: position each vertex in 3D space
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 1.0)
graph.SetPoints(points)

# Filter: convert the graph to polydata (lines connecting vertices)
graph_to_poly = vtkGraphToPolyData()
graph_to_poly.SetInputData(graph)

# Mapper: map polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(graph_to_poly.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("GraphToPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
