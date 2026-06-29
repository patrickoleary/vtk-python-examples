#!/usr/bin/env python

# Demonstrate vtkGraphWeightEuclideanDistanceFilter by creating a simple
# undirected graph with 4 vertices and 3 edges, computing edge weights
# based on Euclidean distance, and rendering the graph layout.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersGeneral import vtkGraphWeightEuclideanDistanceFilter, vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkGraphLayout, vtkPassThroughLayoutStrategy
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

# Create graph with 4 vertices and 3 edges
graph = vtkMutableUndirectedGraph()
v0 = graph.AddVertex()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()

graph.AddEdge(v0, v1)
graph.AddEdge(v0, v2)
graph.AddEdge(v0, v3)

# Assign 3D coordinates to vertices
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 2.0)
graph.SetPoints(points)

# Compute Euclidean distance weights
weight_filter = vtkGraphWeightEuclideanDistanceFilter()
weight_filter.SetInputData(graph)
weight_filter.Update()

# Layout: pass-through keeps explicit vertex positions
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(weight_filter.GetOutputPort())
pass_through_layout_strategy = vtkPassThroughLayoutStrategy()
graph_layout.SetLayoutStrategy(pass_through_layout_strategy)

# Convert graph edges to polydata lines
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

# Edge mapper and actor
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.ScalarVisibilityOff()
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Edge labels (show "Weights" array on edges)
edge_label_mapper = vtkLabeledDataMapper()
edge_label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_label_mapper.SetLabelModeToLabelFieldData()
edge_label_mapper.SetFieldDataName("Weights")
edge_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 0.0)
edge_label_actor = vtkActor2D()
edge_label_actor.SetMapper(edge_label_mapper)

# Vertex glyphs
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.ScalarVisibilityOff()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
vertex_actor.GetProperty().SetPointSize(10)

# Vertex labels
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(edge_label_actor)
renderer.AddActor(vertex_label_actor)
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()
renderer.ResetCamera()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("graph weight euclidean distance")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
