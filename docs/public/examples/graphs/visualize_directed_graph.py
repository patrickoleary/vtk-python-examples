#!/usr/bin/env python

# Visualize a directed graph with edge arrows. The graph is laid out with a
# Simple2D strategy, then arrow glyphs are placed near each edge endpoint
# using vtkGlyph3D on the edge glyph output of vtkGraphToPolyData.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkMutableDirectedGraph
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkGlyphSource2D,
    vtkGraphToPolyData,
)
from vtkmodules.vtkInfovisLayout import (
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Graph: three vertices forming a directed cycle
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()
graph.AddEdge(v1, v2)
graph.AddEdge(v2, v3)
graph.AddEdge(v3, v1)

# Filter: layout the graph with a Simple2D strategy
graph_layout = vtkGraphLayout()
graph_layout.SetInputData(graph)
layout_strategy = vtkSimple2DLayoutStrategy()
graph_layout.SetLayoutStrategy(layout_strategy)

# Filter: convert graph to polydata for rendering (edges + edge glyph output)
graph_to_poly = vtkGraphToPolyData()
graph_to_poly.SetInputConnection(graph_layout.GetOutputPort())
graph_to_poly.EdgeGlyphOutputOn()
graph_to_poly.SetEdgeGlyphPosition(0.98)

# Mapper: map edge lines to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_poly.GetOutputPort())
edge_mapper.ScalarVisibilityOff()

# Actor: assign the edge geometry
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Arrow glyphs: place edge arrows near the endpoints
arrow_source = vtkGlyphSource2D()
arrow_source.SetGlyphTypeToEdgeArrow()
arrow_source.SetScale(0.1)
arrow_source.Update()

arrow_glyph = vtkGlyph3D()
arrow_glyph.SetInputConnection(0, graph_to_poly.GetOutputPort(1))
arrow_glyph.SetInputConnection(1, arrow_source.GetOutputPort())

arrow_mapper = vtkPolyDataMapper()
arrow_mapper.SetInputConnection(arrow_glyph.GetOutputPort())

arrow_actor = vtkActor()
arrow_actor.SetMapper(arrow_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(arrow_actor)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("visualize directed graph")
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
