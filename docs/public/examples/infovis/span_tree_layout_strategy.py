#!/usr/bin/env python
# Demonstrate vtkSpanTreeLayoutStrategy with a graph read from XGML format.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkGraphLayout, vtkSpanTreeLayoutStrategy
from vtkmodules.vtkIOInfovis import vtkXGMLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabeledDataMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Colors (normalized RGB).
navy_rgb = (0.0, 0.0, 0.502)

# Read graph from XGML.
reader = vtkXGMLReader()
reader.SetFileName(os.path.join(data_dir, "fsm.gml"))
reader.Update()

# Layout with span tree strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(reader.GetOutputPort())
span_tree_layout_strategy = vtkSpanTreeLayoutStrategy()
graph_layout.SetLayoutStrategy(span_tree_layout_strategy)

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

# Vertex glyphs with color by "vertex id".
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("vertex id")
vertex_mapper.SetScalarVisibility(True)
vertex_mapper.Update()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetPointSize(10)

# Vertex labels.
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_label_mapper.SetLabelModeToLabelFieldData()
vertex_label_mapper.SetFieldDataName("vertex id")
vertex_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
vertex_label_mapper.GetLabelTextProperty().SetFontSize(12)
vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(vertex_label_actor)
renderer.SetBackground(navy_rgb)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("span tree layout strategy")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
