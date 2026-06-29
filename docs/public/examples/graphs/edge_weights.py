#!/usr/bin/env python

# Display edge weights on a fully connected directed graph. The
# force-directed layout uses the weight values to influence spacing.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkFiltersCore import vtkCellCenters
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkForceDirectedLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

# Colors (normalized RGB)
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Graph: three vertices, fully connected
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()

graph.AddGraphEdge(v1, v2)
graph.AddGraphEdge(v2, v3)
graph.AddGraphEdge(v1, v3)

# Edge weight array
weights = vtkDoubleArray()
weights.SetNumberOfComponents(1)
weights.SetName("Weights")
weights.InsertNextValue(1.0)
weights.InsertNextValue(1.0)
weights.InsertNextValue(2.0)
graph.GetEdgeData().AddArray(weights)

print("Number of edges:", graph.GetNumberOfEdges())

# Filter: layout the graph with a force-directed strategy weighted by edges
layout_strategy = vtkForceDirectedLayoutStrategy()
layout_strategy.SetEdgeWeightField("Weights")
layout_strategy.SetWeightEdges(True)
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

# Edge labels: compute edge midpoints with vtkCellCenters, then label them
edge_centers = vtkCellCenters()
edge_centers.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_centers.CopyArraysOn()

edge_label_mapper = vtkLabeledDataMapper()
edge_label_mapper.SetInputConnection(edge_centers.GetOutputPort())
edge_label_mapper.SetLabelModeToLabelFieldData()
edge_label_mapper.SetFieldDataName("Weights")

edge_label_actor = vtkActor2D()
edge_label_actor.SetMapper(edge_label_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(edge_label_actor)
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("edge weights")
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
