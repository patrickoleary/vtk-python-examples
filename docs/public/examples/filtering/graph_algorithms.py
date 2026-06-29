#!/usr/bin/env python
# Demonstrate vtkVertexDegree graph algorithm with glyph visualization.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkGlyphSource2D, vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkVertexDegree
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build undirected graph with positioned vertices.
graph = vtkMutableUndirectedGraph()

points = vtkPoints()
graph.AddVertex()
points.InsertNextPoint(0, 1, 0)
graph.AddVertex()
points.InsertNextPoint(0.5, 1, 0)
graph.AddVertex()
points.InsertNextPoint(0.25, 0.5, 0)
graph.AddVertex()
points.InsertNextPoint(0, 0, 0)
graph.AddVertex()
points.InsertNextPoint(0.5, 0, 0)
graph.AddVertex()
points.InsertNextPoint(1, 0, 0)
graph.AddVertex()
points.InsertNextPoint(0.75, 0.5, 0)
graph.SetPoints(points)

graph.AddEdge(0, 1)
graph.AddEdge(0, 2)
graph.AddEdge(1, 2)
graph.AddEdge(2, 3)
graph.AddEdge(2, 4)
graph.AddEdge(3, 4)

# Vertex degree algorithm.
degree = vtkVertexDegree()
degree.SetInputData(graph)

# Convert graph to polydata for rendering.
graph_to_poly = vtkGraphToPolyData()
graph_to_poly.SetInputConnection(degree.GetOutputPort())

# Vertex glyphs.
glyph_source = vtkGlyphSource2D()
glyph_source.SetGlyphTypeToVertex()

vertex_glyph = vtkGlyph3D()
vertex_glyph.SetInputConnection(0, graph_to_poly.GetOutputPort())
vertex_glyph.SetInputConnection(1, glyph_source.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("VertexDegree")
vertex_mapper.SetScalarRange(0, 4)

vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetPointSize(10.0)
vertex_actor.SetPosition(0, 0, 0.001)

# Edge lines.
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_poly.GetOutputPort())
edge_mapper.SetScalarModeToUseCellFieldData()

edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.SetPosition(0, 0, 0)

# Rendering pipeline.
renderer = vtkRenderer()
renderer.AddActor(vertex_actor)
renderer.AddActor(edge_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("graph algorithms")

# Scene
renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
