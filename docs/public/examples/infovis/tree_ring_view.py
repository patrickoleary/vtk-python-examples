#!/usr/bin/env python
# Demonstrate tree ring layout with graph overlay using explicit pipeline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisLayout import (
    vtkAreaLayout,
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
    vtkSquarifyLayoutStrategy,
    vtkTreeRingToPolyData,
)
from vtkmodules.vtkIOInfovis import vtkXMLTreeReader
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

# Read tree (used for area layout).
reader_tree = vtkXMLTreeReader()
reader_tree.SetFileName(os.path.join(data_dir, "vtklibrary.xml"))
reader_tree.SetEdgePedigreeIdArrayName("tree edge")
reader_tree.GenerateVertexPedigreeIdsOff()
reader_tree.SetVertexPedigreeIdArrayName("id")

# Read graph (edges overlay).
reader_graph = vtkXMLTreeReader()
reader_graph.SetFileName(os.path.join(data_dir, "vtkclasses.xml"))
reader_graph.SetEdgePedigreeIdArrayName("graph edge")
reader_graph.GenerateVertexPedigreeIdsOff()
reader_graph.SetVertexPedigreeIdArrayName("id")

reader_tree.Update()
reader_graph.Update()

# Area layout with squarify strategy for the tree ring.
area_layout = vtkAreaLayout()
area_layout.SetInputConnection(reader_tree.GetOutputPort())
squarify_strategy = vtkSquarifyLayoutStrategy()
area_layout.SetLayoutStrategy(squarify_strategy)
area_layout.SetSizeArrayName("VertexDegree")
area_layout.Update()

# Rename 'area' array to 'sectors' so vtkTreeRingToPolyData can find it.
area_arr = area_layout.GetOutput().GetVertexData().GetArray("area")
if area_arr:
    area_arr.SetName("sectors")

# Convert tree areas to ring polydata.
tree_ring_to_polydata = vtkTreeRingToPolyData()
tree_ring_to_polydata.SetInputConnection(area_layout.GetOutputPort())
tree_ring_to_polydata.Update()

# Area mapper and actor (colored by "VertexDegree").
area_mapper = vtkPolyDataMapper()
area_mapper.SetInputConnection(tree_ring_to_polydata.GetOutputPort())
area_mapper.SetScalarModeToUseCellFieldData()
area_mapper.SelectColorArray("VertexDegree")
area_mapper.SetScalarVisibility(True)
area_actor = vtkActor()
area_actor.SetMapper(area_mapper)

# Area labels.
area_label_mapper = vtkLabeledDataMapper()
area_label_mapper.SetInputConnection(tree_ring_to_polydata.GetOutputPort())
area_label_mapper.SetLabelModeToLabelFieldData()
area_label_mapper.SetFieldDataName("id")
area_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
area_label_mapper.GetLabelTextProperty().SetFontSize(10)
area_label_mapper.GetLabelTextProperty().ShadowOn()
area_label_actor = vtkActor2D()
area_label_actor.SetMapper(area_label_mapper)

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
graph_edge_actor.GetProperty().SetOpacity(0.5)
graph_edge_actor.GetProperty().SetLineWidth(1)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(area_actor)
renderer.AddActor(area_label_actor)
renderer.AddActor(graph_edge_actor)
renderer.SetBackground(0.2, 0.2, 0.3)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tree ring view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
