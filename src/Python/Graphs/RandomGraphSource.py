#!/usr/bin/env python

# Generate a random graph with vtkRandomGraphSource and display it using a
# force-directed layout.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkInfovisCore import vtkRandomGraphSource
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Colors (normalized RGB)
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Source: generate a random graph with 5 vertices and 4 edges
random_graph_source = vtkRandomGraphSource()
random_graph_source.SetNumberOfVertices(5)
random_graph_source.SetNumberOfEdges(4)
random_graph_source.SetSeed(123)
random_graph_source.Update()

# View: display the graph with a force-directed layout
view = vtkGraphLayoutView()
view.AddRepresentationFromInput(random_graph_source.GetOutput())
view.SetLayoutStrategyToForceDirected()
view.ResetCamera()
view.GetRenderer().SetBackground(navy_rgb)
view.GetRenderer().SetBackground2(midnight_blue_rgb)
render_window = view.GetRenderWindow()
render_window.SetWindowName("RandomGraphSource")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
