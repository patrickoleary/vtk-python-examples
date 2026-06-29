#!/usr/bin/env python

# Demonstrate vtkPassThrough by creating a directed graph with vertex
# data arrays, passing it through the filter, and rendering the graph
# using an explicit layout pipeline.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkFiltersCore import vtkPassThrough
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkGraphLayout, vtkSimple2DLayoutStrategy
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

# Create a directed graph with vertex data
graph = vtkMutableDirectedGraph()
x_arr = vtkDoubleArray()
x_arr.SetName("x")
y_arr = vtkDoubleArray()
y_arr.SetName("y")
z_arr = vtkDoubleArray()
z_arr.SetName("z")

for i in range(10):
    for j in range(10):
        graph.AddVertex()
        x_arr.InsertNextValue(float(i))
        y_arr.InsertNextValue(float(j))
        z_arr.InsertNextValue(1.0)

graph.GetVertexData().AddArray(x_arr)
graph.GetVertexData().AddArray(y_arr)
graph.GetVertexData().AddArray(z_arr)

# Add some edges
for i in range(0, 90):
    graph.AddEdge(i, i + 10)

# Pass through filter
pass_filter = vtkPassThrough()
pass_filter.SetInputData(graph)
pass_filter.Update()

# Layout with simple 2D strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(pass_filter.GetOutputPort())
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

# Vertex glyphs.
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.ScalarVisibilityOff()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
vertex_actor.GetProperty().SetPointSize(6)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pass through")

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
