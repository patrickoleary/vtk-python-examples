#!/usr/bin/env python
# Demonstrate coincident graph layout with pass-through strategy, vertex and edge labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIdTypeArray, vtkPoints, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
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

# Colors (normalized RGB).
navy_rgb = (0.0, 0.0, 0.502)

# Build graph with coincident vertices and explicit point positions.
graph = vtkMutableUndirectedGraph()
point_data = vtkDoubleArray()
point_data.SetNumberOfComponents(3)
points = vtkPoints()
points.SetData(point_data)
graph.SetPoints(points)

# 10 vertices at origin.
for _ in range(10):
    graph.AddVertex()
    points.InsertNextPoint(0.0, 0.0, 0.0)

# 8 vertices at various positions.
extra_positions = [
    (0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (3.0, 0.0, 0.0), (2.0, 2.5, 0.0),
    (0.0, -2.0, 0.0), (2.0, -1.5, 0.0), (-1.0, 2.0, 0.0), (3.0, 0.0, 0.0),
]
for pos in extra_positions:
    graph.AddVertex()
    points.InsertNextPoint(pos)

# Edges from vertex 0 to 1..9.
for i in range(1, 10):
    graph.AddEdge(0, i)

# Chain edges 10->11->...->17 plus closing edge 0->10.
for i in range(10, 17):
    graph.AddEdge(i, i + 1)
graph.AddEdge(0, 10)

# Vertex name array.
vertex_names = vtkStringArray()
vertex_names.SetName("name")
for i in range(graph.GetNumberOfVertices()):
    vertex_names.InsertNextValue(f"Vert{i}")
graph.GetVertexData().AddArray(vertex_names)

# Edge arrays.
edge_labels = vtkStringArray()
edge_labels.SetName("edge label")
edge_distance = vtkIdTypeArray()
edge_distance.SetName("distance")
labels = ["a", "b", "c", "d"]
for i in range(graph.GetNumberOfEdges()):
    edge_distance.InsertNextValue(i)
    edge_labels.InsertNextValue(labels[i % 4])
graph.GetEdgeData().AddArray(edge_distance)
graph.GetEdgeData().AddArray(edge_labels)

# Layout with pass-through strategy (keeps explicit positions).
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
pass_through_layout_strategy = vtkPassThroughLayoutStrategy()
graph_layout.SetLayoutStrategy(pass_through_layout_strategy)

# Convert graph to polydata.
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

# Edge mapper and actor (colored by "distance").
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.SetScalarModeToUseCellFieldData()
edge_mapper.SelectColorArray("distance")
edge_mapper.SetScalarVisibility(True)
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Edge labels.
edge_label_mapper = vtkLabeledDataMapper()
edge_label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_label_mapper.SetLabelModeToLabelFieldData()
edge_label_mapper.SetFieldDataName("edge label")
edge_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 0.0)
edge_label_actor = vtkActor2D()
edge_label_actor.SetMapper(edge_label_mapper)

# Vertex glyphs.
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.ScalarVisibilityOff()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
vertex_actor.GetProperty().SetPointSize(8)

# Vertex labels.
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_label_mapper.SetLabelModeToLabelFieldData()
vertex_label_mapper.SetFieldDataName("name")
vertex_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(edge_label_actor)
renderer.AddActor(vertex_label_actor)
renderer.SetBackground(navy_rgb)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("coincident graph layout view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
