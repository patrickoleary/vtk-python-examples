#!/usr/bin/env python
# Demonstrate icon glyphs on graph vertices using explicit pipeline with vtkGraphLayout.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIntArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkMutableUndirectedGraph
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkGraphLayout, vtkSimple2DLayoutStrategy
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Colors (normalized RGB).
navy_rgb = (0.0, 0.0, 0.502)

# Read icon sheet.
image_reader = vtkPNGReader()
image_reader.SetFileName(os.path.join(data_dir, "TangoIcons.png"))
image_reader.Update()

# Build graph with explicit point positions.
graph = vtkMutableUndirectedGraph()
point_data = vtkDoubleArray()
point_data.SetNumberOfComponents(3)
points = vtkPoints()
points.SetData(point_data)
graph.SetPoints(points)

icon_index = vtkIntArray()
icon_index.SetName("IconIndex")
icon_index.SetNumberOfComponents(1)
graph.GetVertexData().SetScalars(icon_index)

positions = [
    (0.0, 0.0, 0.0), (2.0, 0.0, 0.0), (3.0, 0.0, 0.0), (2.0, 2.5, 0.0),
    (0.0, -2.0, 0.0), (2.0, -1.5, 0.0), (-1.0, 2.0, 0.0), (3.0, 0.0, 0.0),
]
for pos in positions:
    graph.AddVertex()
    points.InsertNextPoint(pos)

edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (6, 7), (7, 0)]
for src, dst in edges:
    graph.AddEdge(src, dst)

icon_values = [1, 4, 26, 17, 0, 5, 1, 29]
for val in icon_values:
    icon_index.InsertNextTuple1(val)

# Layout with Simple2D strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
simple_2d_layout_strategy = vtkSimple2DLayoutStrategy()
graph_layout.SetLayoutStrategy(simple_2d_layout_strategy)

# Convert graph to polydata.
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

# Edge mapper and actor.
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.ScalarVisibilityOff()
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(0.7, 0.7, 0.7)

# Vertex glyphs with icon texture.
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

texture = vtkTexture()
texture.SetInputConnection(image_reader.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.ScalarVisibilityOff()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.SetTexture(texture)
vertex_actor.GetProperty().SetColor(1.0, 0.5, 0.0)
vertex_actor.GetProperty().SetPointSize(12)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.SetBackground(navy_rgb)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("icon glyph filter")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
