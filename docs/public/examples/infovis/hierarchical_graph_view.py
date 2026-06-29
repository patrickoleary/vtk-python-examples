#!/usr/bin/env python
# Demonstrate cosmic tree layout with graph overlay using explicit pipeline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import vtkCosmicTreeLayoutStrategy, vtkGraphLayout
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

# Read tree from XML.
reader_tree = vtkXMLTreeReader()
reader_tree.SetFileName(os.path.join(data_dir, "vtklibrary.xml"))
reader_tree.SetEdgePedigreeIdArrayName("tree edge")
reader_tree.GenerateVertexPedigreeIdsOff()
reader_tree.SetVertexPedigreeIdArrayName("id")

# Read graph from XML.
reader_graph = vtkXMLTreeReader()
reader_graph.SetFileName(os.path.join(data_dir, "vtkclasses.xml"))
reader_graph.SetEdgePedigreeIdArrayName("graph edge")
reader_graph.GenerateVertexPedigreeIdsOff()
reader_graph.SetVertexPedigreeIdArrayName("id")

reader_tree.Update()
reader_graph.Update()

# Layout tree with cosmic tree strategy.
tree_layout = vtkGraphLayout()
tree_layout.SetInputConnection(reader_tree.GetOutputPort())
cosmic_tree_strategy = vtkCosmicTreeLayoutStrategy()
cosmic_tree_strategy.SetNodeSizeArrayName("VertexDegree")
cosmic_tree_strategy.SetSizeLeafNodesOnly(True)
tree_layout.SetLayoutStrategy(cosmic_tree_strategy)

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
tree_edge_actor.GetProperty().SetColor(0.6, 0.6, 0.6)
tree_edge_actor.GetProperty().SetLineWidth(1)

# Tree vertex glyphs (colored by VertexDegree).
tree_vertex_glyph = vtkVertexGlyphFilter()
tree_vertex_glyph.SetInputConnection(tree_to_polydata.GetOutputPort())

tree_vertex_mapper = vtkPolyDataMapper()
tree_vertex_mapper.SetInputConnection(tree_vertex_glyph.GetOutputPort())
tree_vertex_mapper.SetScalarModeToUsePointFieldData()
tree_vertex_mapper.SelectColorArray("VertexDegree")
tree_vertex_mapper.SetScalarVisibility(True)
tree_vertex_actor = vtkActor()
tree_vertex_actor.SetMapper(tree_vertex_mapper)
tree_vertex_actor.GetProperty().SetPointSize(6)

# Non-overlapping vertex labels using label placement.
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputConnection(tree_vertex_glyph.GetOutputPort())
label_hierarchy.SetLabelArrayName("id")
label_hierarchy.GetTextProperty().SetColor(1.0, 1.0, 1.0)
label_hierarchy.GetTextProperty().SetFontSize(12)

label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())
label_mapper.SetShapeToNone()
label_mapper.SetBackgroundOpacity(0.0)
label_mapper.SetMaximumLabelFraction(0.3)
label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Layout graph overlay with cosmic tree strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(reader_graph.GetOutputPort())
graph_cosmic_strategy = vtkCosmicTreeLayoutStrategy()
graph_cosmic_strategy.SetNodeSizeArrayName("VertexDegree")
graph_cosmic_strategy.SetSizeLeafNodesOnly(True)
graph_layout.SetLayoutStrategy(graph_cosmic_strategy)

# Convert graph to polydata.
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

# Graph edge mapper and actor.
graph_edge_mapper = vtkPolyDataMapper()
graph_edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
graph_edge_mapper.SetScalarModeToUseCellFieldData()
graph_edge_mapper.SelectColorArray("graph edge")
graph_edge_mapper.SetScalarVisibility(True)
graph_edge_actor = vtkActor()
graph_edge_actor.SetMapper(graph_edge_mapper)
graph_edge_actor.GetProperty().SetOpacity(0.5)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(tree_edge_actor)
renderer.AddActor(tree_vertex_actor)
renderer.AddActor(label_actor)
renderer.AddActor(graph_edge_actor)
renderer.SetBackground(0.2, 0.2, 0.3)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("hierarchical graph view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
