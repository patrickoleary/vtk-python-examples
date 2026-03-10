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
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

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

# Window: single render window for both views
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("SideBySideGraphs")

render_window_interactor = vtkRenderWindowInteractor()

# View 0: left viewport — triangle graph
view0 = vtkGraphLayoutView()
view0.SetRenderWindow(render_window)
view0.SetInteractor(render_window_interactor)
view0.GetRenderer().SetViewport(0.0, 0.0, 0.5, 1.0)
view0.AddRepresentationFromInput(g0)
view0.SetLayoutStrategyToForceDirected()
view0.GetRenderer().SetBackground(navy_rgb)
view0.GetRenderer().SetBackground2(midnight_blue_rgb)
view0.Render()
view0.ResetCamera()

# View 1: right viewport — single-edge graph
view1 = vtkGraphLayoutView()
view1.SetRenderWindow(render_window)
view1.SetInteractor(render_window_interactor)
view1.GetRenderer().SetViewport(0.5, 0.0, 1.0, 1.0)
view1.AddRepresentationFromInput(g1)
view1.SetLayoutStrategyToForceDirected()
view1.GetRenderer().SetBackground(dark_green_rgb)
view1.GetRenderer().SetBackground2(forest_green_rgb)
view1.Render()
view1.ResetCamera()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
