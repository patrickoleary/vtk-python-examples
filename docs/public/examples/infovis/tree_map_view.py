#!/usr/bin/env python
# Demonstrate tree map layout with graph overlay using explicit pipeline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkGraphLayout, vtkSimple2DLayoutStrategy
from vtkmodules.vtkIOInfovis import vtkXMLTreeReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkLabelPlacementMapper, vtkPointSetToLabelHierarchy

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read tree.
reader_tree = vtkXMLTreeReader()
reader_tree.SetFileName(os.path.join(data_dir, "vtklibrary.xml"))
reader_tree.SetEdgePedigreeIdArrayName("graph edge")
reader_tree.GenerateVertexPedigreeIdsOff()
reader_tree.SetVertexPedigreeIdArrayName("id")

# Read graph (edges overlay).
reader_graph = vtkXMLTreeReader()
reader_graph.SetFileName(os.path.join(data_dir, "vtkclasses.xml"))
reader_graph.SetEdgePedigreeIdArrayName("tree edge")
reader_graph.GenerateVertexPedigreeIdsOff()
reader_graph.SetVertexPedigreeIdArrayName("id")

reader_tree.Update()
reader_graph.Update()

# Layout tree with Simple2D strategy.
tree_layout = vtkGraphLayout()
tree_layout.SetInputConnection(reader_tree.GetOutputPort())
tree_strategy = vtkSimple2DLayoutStrategy()
tree_layout.SetLayoutStrategy(tree_strategy)

# Convert tree to polydata.
tree_to_polydata = vtkGraphToPolyData()
tree_to_polydata.SetInputConnection(tree_layout.GetOutputPort())
tree_to_polydata.Update()

# Tree edge mapper and actor.
tree_edge_mapper = vtkPolyDataMapper()
tree_edge_mapper.SetInputConnection(tree_to_polydata.GetOutputPort())
tree_edge_mapper.ScalarVisibilityOff()
tree_edge_actor = vtkActor()
tree_edge_actor.SetMapper(tree_edge_mapper)
tree_edge_actor.GetProperty().SetColor(0.4, 0.4, 0.6)
tree_edge_actor.GetProperty().SetOpacity(0.3)

# Vertex glyphs for tree.
tree_vertex_glyph = vtkVertexGlyphFilter()
tree_vertex_glyph.SetInputConnection(tree_to_polydata.GetOutputPort())

tree_vertex_mapper = vtkPolyDataMapper()
tree_vertex_mapper.SetInputConnection(tree_vertex_glyph.GetOutputPort())
tree_vertex_mapper.ScalarVisibilityOff()
tree_vertex_actor = vtkActor()
tree_vertex_actor.SetMapper(tree_vertex_mapper)
tree_vertex_actor.GetProperty().SetColor(0.3, 0.8, 0.3)
tree_vertex_actor.GetProperty().SetPointSize(4)

# Graph overlay layout and edges.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(reader_graph.GetOutputPort())
simple_2d_strategy = vtkSimple2DLayoutStrategy()
graph_layout.SetLayoutStrategy(simple_2d_strategy)

graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

graph_edge_mapper = vtkPolyDataMapper()
graph_edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
graph_edge_mapper.ScalarVisibilityOff()
graph_edge_actor = vtkActor()
graph_edge_actor.SetMapper(graph_edge_mapper)
graph_edge_actor.GetProperty().SetColor(1.0, 0.5, 0.0)
graph_edge_actor.GetProperty().SetOpacity(0.7)

# Graph vertex glyphs.
graph_vertex_glyph = vtkVertexGlyphFilter()
graph_vertex_glyph.SetInputConnection(graph_to_polydata.GetOutputPort())

graph_vertex_mapper = vtkPolyDataMapper()
graph_vertex_mapper.SetInputConnection(graph_vertex_glyph.GetOutputPort())
graph_vertex_mapper.ScalarVisibilityOff()
graph_vertex_actor = vtkActor()
graph_vertex_actor.SetMapper(graph_vertex_mapper)
graph_vertex_actor.GetProperty().SetColor(1.0, 0.8, 0.0)
graph_vertex_actor.GetProperty().SetPointSize(5)

# Non-overlapping labels for graph vertices.
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputConnection(graph_vertex_glyph.GetOutputPort())
label_hierarchy.SetLabelArrayName("id")
label_hierarchy.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_hierarchy.GetTextProperty().SetFontSize(10)

label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())
label_mapper.SetShapeToNone()
label_mapper.SetBackgroundOpacity(0.0)
label_mapper.SetMaximumLabelFraction(0.3)
label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(tree_edge_actor)
renderer.AddActor(tree_vertex_actor)
renderer.AddActor(graph_edge_actor)
renderer.AddActor(graph_vertex_actor)
renderer.AddActor(label_actor)
renderer.SetBackground(0.2, 0.2, 0.3)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tree map view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
