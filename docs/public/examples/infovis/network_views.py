#!/usr/bin/env python
# Demonstrate network hierarchy tree ring with graph overlay using explicit pipeline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkNetworkHierarchy, vtkTableToGraph
from vtkmodules.vtkInfovisLayout import (
    vtkAreaLayout,
    vtkGraphLayout,
    vtkSimple2DLayoutStrategy,
    vtkSquarifyLayoutStrategy,
    vtkTreeRingToPolyData,
)
from vtkmodules.vtkIOSQL import vtkSQLDatabaseTableSource
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
db_file = os.path.join(data_dir, "ports_protocols.db")

# Pull edges from database.
database_to_edge_table = vtkSQLDatabaseTableSource()
database_to_edge_table.SetURL("sqlite://" + db_file)
database_to_edge_table.SetQuery(
    "select src, dst, dport, protocol, port_protocol from tcp"
)

# Pull vertices from database.
database_to_vertex_table = vtkSQLDatabaseTableSource()
database_to_vertex_table.SetURL("sqlite://" + db_file)
database_to_vertex_table.SetQuery("select ip, hostname from dnsnames")

# Make a graph.
graph = vtkTableToGraph()
graph.AddInputConnection(0, database_to_edge_table.GetOutputPort())
graph.AddInputConnection(1, database_to_vertex_table.GetOutputPort())
graph.AddLinkVertex("src", "ip", False)
graph.AddLinkVertex("dst", "ip", False)
graph.AddLinkEdge("src", "dst")

# Make a tree out of IP addresses.
network_hierarchy = vtkNetworkHierarchy()
network_hierarchy.AddInputConnection(graph.GetOutputPort())

# Area layout with squarify strategy for tree ring.
area_layout = vtkAreaLayout()
area_layout.SetInputConnection(network_hierarchy.GetOutputPort())
squarify_strategy = vtkSquarifyLayoutStrategy()
area_layout.SetLayoutStrategy(squarify_strategy)
area_layout.SetSizeArrayName("VertexDegree")
area_layout.Update()

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
area_label_mapper.SetFieldDataName("ip")
area_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
area_label_mapper.GetLabelTextProperty().SetFontSize(10)
area_label_mapper.GetLabelTextProperty().ShadowOn()
area_label_actor = vtkActor2D()
area_label_actor.SetMapper(area_label_mapper)

# Graph overlay layout and edges (colored by "dport").
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(graph.GetOutputPort())
simple_2d_strategy = vtkSimple2DLayoutStrategy()
graph_layout.SetLayoutStrategy(simple_2d_strategy)

graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

graph_edge_mapper = vtkPolyDataMapper()
graph_edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
graph_edge_mapper.SetScalarModeToUseCellFieldData()
graph_edge_mapper.SelectColorArray("dport")
graph_edge_mapper.SetScalarVisibility(True)
graph_edge_actor = vtkActor()
graph_edge_actor.SetMapper(graph_edge_mapper)
graph_edge_actor.GetProperty().SetOpacity(0.5)

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
render_window.SetWindowName("network views")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
