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
)
from vtkmodules.vtkViewsInfovis import vtkGraphLayoutView

# Graph: three vertices forming a directed cycle
graph = vtkMutableDirectedGraph()
v1 = graph.AddVertex()
v2 = graph.AddVertex()
v3 = graph.AddVertex()
graph.AddEdge(v1, v2)
graph.AddEdge(v2, v3)
graph.AddEdge(v3, v1)

# Layout: compute vertex positions with a Simple2D strategy
layout = vtkGraphLayout()
layout.SetInputData(graph)
strategy = vtkSimple2DLayoutStrategy()
layout.SetLayoutStrategy(strategy)

# View: use pass-through layout since positions are pre-computed
view = vtkGraphLayoutView()
view.SetLayoutStrategyToPassThrough()
view.SetEdgeLayoutStrategyToPassThrough()
view.AddRepresentationFromInputConnection(layout.GetOutputPort())

# Arrow glyphs: place edge arrows near the endpoints
graph_to_poly = vtkGraphToPolyData()
graph_to_poly.SetInputConnection(layout.GetOutputPort())
graph_to_poly.EdgeGlyphOutputOn()
graph_to_poly.SetEdgeGlyphPosition(0.98)

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
view.GetRenderer().AddActor(arrow_actor)

view.ResetCamera()
render_window = view.GetRenderWindow()
render_window.SetWindowName("VisualizeDirectedGraph")

# Launch the interactive visualization
view.GetInteractor().Initialize()
view.GetInteractor().Start()
