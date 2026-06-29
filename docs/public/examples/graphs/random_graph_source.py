#!/usr/bin/env python

# Generate a random graph with vtkRandomGraphSource and display it using a
# force-directed layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
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

# Source: generate a random graph with 5 vertices and 4 edges
random_graph_source = vtkRandomGraphSource()
random_graph_source.SetNumberOfVertices(5)
random_graph_source.SetNumberOfEdges(4)
random_graph_source.SetSeed(123)

# Filter: layout the graph vertices in 2D
force_directed_layout_strategy = vtkForceDirectedLayoutStrategy()
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(random_graph_source.GetOutputPort())
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
render_window.SetWindowName("random graph source")
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
