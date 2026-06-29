#!/usr/bin/env python
# Demonstrate vtkTableToGraph with multiple link configurations on author data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkBitArray, vtkIntArray, vtkPoints, vtkStringArray
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkMutableUndirectedGraph,
    vtkTable,
    vtkUndirectedGraph,
)
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import vtkGlyphSource2D, vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import (
    vtkMergeTables,
    vtkStringToCategory,
    vtkTableToGraph,
)
from vtkmodules.vtkInfovisLayout import (
    vtkCircularLayoutStrategy,
    vtkGraphLayout,
)
from vtkmodules.vtkIOInfovis import vtkDelimitedTextReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read edge table from CSV.
reader = vtkDelimitedTextReader()
reader.SetFileName(os.path.join(data_dir, "authors-tabletographtest.csv"))
reader.SetHaveHeaders(True)

# Person table.
person_table = vtkTable()
name_arr = vtkStringArray()
name_arr.SetName("name")
pet_arr = vtkStringArray()
pet_arr.SetName("pet")
for name, pet in [("Biff", "cat"), ("Bob", "bird"), ("Baz", "dog"),
                  ("Bippity", "lizard"), ("Boppity", "chinchilla"), ("Boo", "rabbit")]:
    name_arr.InsertNextValue(name)
    pet_arr.InsertNextValue(pet)
person_table.AddColumn(name_arr)
person_table.AddColumn(pet_arr)

# Organization table.
org_table = vtkTable()
org_name_arr = vtkStringArray()
org_name_arr.SetName("name")
size_arr = vtkIntArray()
size_arr.SetName("size")
for org_name, size in [("NASA", 10000), ("Bob's Supermarket", 100), ("Oil Changes 'R' Us", 20)]:
    org_name_arr.InsertNextValue(org_name)
    size_arr.InsertNextValue(size)
org_table.AddColumn(org_name_arr)
org_table.AddColumn(size_arr)

# Merge tables.
merge = vtkMergeTables()
merge.SetInputData(0, person_table)
merge.SetFirstTablePrefix("person.")
merge.SetInputData(1, org_table)
merge.SetSecondTablePrefix("organization.")
merge.MergeColumnsByNameOff()
merge.PrefixAllButMergedOn()

# Table to graph with various configurations.
table_to_graph = vtkTableToGraph()
table_to_graph.SetInputConnection(0, reader.GetOutputPort())

# --- Pipeline 0: Path configuration (offset 0, 0) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person")
table_to_graph.AddLinkVertex("Boss", "person")
table_to_graph.AddLinkVertex("Affiliation", "organization")
table_to_graph.AddLinkVertex("Alma Mater", "school")
table_to_graph.AddLinkVertex("Categories", "interest")
table_to_graph.AddLinkEdge("Author", "Boss")
table_to_graph.AddLinkEdge("Boss", "Affiliation")
table_to_graph.AddLinkEdge("Affiliation", "Alma Mater")
table_to_graph.AddLinkEdge("Alma Mater", "Categories")

category_0 = vtkStringToCategory()
category_0.SetInputConnection(table_to_graph.GetOutputPort())
category_0.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_0.Update()
graph_0 = vtkUndirectedGraph()
graph_0.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_0.GetOutput()))
layout_0 = vtkGraphLayout()
layout_0.SetInputData(graph_0)
circular_layout_strategy_0 = vtkCircularLayoutStrategy()
layout_0.SetLayoutStrategy(circular_layout_strategy_0)
graph_to_poly_0 = vtkGraphToPolyData()
graph_to_poly_0.SetInputConnection(layout_0.GetOutputPort())
glyph_source_0 = vtkGlyphSource2D()
glyph_source_0.SetGlyphTypeToVertex()
vertex_glyph_0 = vtkGlyph3D()
vertex_glyph_0.SetInputConnection(0, graph_to_poly_0.GetOutputPort())
vertex_glyph_0.SetInputConnection(1, glyph_source_0.GetOutputPort())

vertex_mapper_0 = vtkPolyDataMapper()
vertex_mapper_0.SetInputConnection(vertex_glyph_0.GetOutputPort())
vertex_mapper_0.SetScalarModeToUsePointFieldData()
vertex_mapper_0.SelectColorArray("category")
range_0 = graph_0.GetVertexData().GetArray("category").GetRange()
vertex_mapper_0.SetScalarRange(range_0[0], range_0[1])

vertex_actor_0 = vtkActor()
vertex_actor_0.SetMapper(vertex_mapper_0)
vertex_actor_0.GetProperty().SetPointSize(7.0)
vertex_actor_0.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_0.SetPosition(0, 0, 0.001)

edge_mapper_0 = vtkPolyDataMapper()
edge_mapper_0.SetInputConnection(graph_to_poly_0.GetOutputPort())
edge_mapper_0.ScalarVisibilityOff()

edge_actor_0 = vtkActor()
edge_actor_0.SetMapper(edge_mapper_0)
edge_actor_0.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_0.SetPosition(0, 0, 0)

# --- Pipeline 1: Star configuration (offset 2.5, 0) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person")
table_to_graph.AddLinkVertex("Boss", "person")
table_to_graph.AddLinkVertex("Affiliation", "organization")
table_to_graph.AddLinkVertex("Alma Mater", "school")
table_to_graph.AddLinkVertex("Categories", "interest")
table_to_graph.AddLinkEdge("Author", "Boss")
table_to_graph.AddLinkEdge("Author", "Affiliation")
table_to_graph.AddLinkEdge("Author", "Alma Mater")
table_to_graph.AddLinkEdge("Author", "Categories")

category_1 = vtkStringToCategory()
category_1.SetInputConnection(table_to_graph.GetOutputPort())
category_1.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_1.Update()
graph_1 = vtkUndirectedGraph()
graph_1.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_1.GetOutput()))
layout_1 = vtkGraphLayout()
layout_1.SetInputData(graph_1)
circular_layout_strategy_1 = vtkCircularLayoutStrategy()
layout_1.SetLayoutStrategy(circular_layout_strategy_1)
graph_to_poly_1 = vtkGraphToPolyData()
graph_to_poly_1.SetInputConnection(layout_1.GetOutputPort())
glyph_source_1 = vtkGlyphSource2D()
glyph_source_1.SetGlyphTypeToVertex()
vertex_glyph_1 = vtkGlyph3D()
vertex_glyph_1.SetInputConnection(0, graph_to_poly_1.GetOutputPort())
vertex_glyph_1.SetInputConnection(1, glyph_source_1.GetOutputPort())

vertex_mapper_1 = vtkPolyDataMapper()
vertex_mapper_1.SetInputConnection(vertex_glyph_1.GetOutputPort())
vertex_mapper_1.SetScalarModeToUsePointFieldData()
vertex_mapper_1.SelectColorArray("category")
range_1 = graph_1.GetVertexData().GetArray("category").GetRange()
vertex_mapper_1.SetScalarRange(range_1[0], range_1[1])

vertex_actor_1 = vtkActor()
vertex_actor_1.SetMapper(vertex_mapper_1)
vertex_actor_1.GetProperty().SetPointSize(7.0)
vertex_actor_1.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_1.SetPosition(2.5, 0, 0.001)

edge_mapper_1 = vtkPolyDataMapper()
edge_mapper_1.SetInputConnection(graph_to_poly_1.GetOutputPort())
edge_mapper_1.ScalarVisibilityOff()

edge_actor_1 = vtkActor()
edge_actor_1.SetMapper(edge_mapper_1)
edge_actor_1.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_1.SetPosition(2.5, 0, 0)

# --- Pipeline 2: Affiliation (offset 5.0, 0) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person")
table_to_graph.AddLinkVertex("Affiliation", "organization")
table_to_graph.AddLinkEdge("Author", "Affiliation")

category_2 = vtkStringToCategory()
category_2.SetInputConnection(table_to_graph.GetOutputPort())
category_2.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_2.Update()
graph_2 = vtkUndirectedGraph()
graph_2.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_2.GetOutput()))
layout_2 = vtkGraphLayout()
layout_2.SetInputData(graph_2)
circular_layout_strategy_2 = vtkCircularLayoutStrategy()
layout_2.SetLayoutStrategy(circular_layout_strategy_2)
graph_to_poly_2 = vtkGraphToPolyData()
graph_to_poly_2.SetInputConnection(layout_2.GetOutputPort())
glyph_source_2 = vtkGlyphSource2D()
glyph_source_2.SetGlyphTypeToVertex()
vertex_glyph_2 = vtkGlyph3D()
vertex_glyph_2.SetInputConnection(0, graph_to_poly_2.GetOutputPort())
vertex_glyph_2.SetInputConnection(1, glyph_source_2.GetOutputPort())

vertex_mapper_2 = vtkPolyDataMapper()
vertex_mapper_2.SetInputConnection(vertex_glyph_2.GetOutputPort())
vertex_mapper_2.SetScalarModeToUsePointFieldData()
vertex_mapper_2.SelectColorArray("category")
range_2 = graph_2.GetVertexData().GetArray("category").GetRange()
vertex_mapper_2.SetScalarRange(range_2[0], range_2[1])

vertex_actor_2 = vtkActor()
vertex_actor_2.SetMapper(vertex_mapper_2)
vertex_actor_2.GetProperty().SetPointSize(7.0)
vertex_actor_2.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_2.SetPosition(5.0, 0, 0.001)

edge_mapper_2 = vtkPolyDataMapper()
edge_mapper_2.SetInputConnection(graph_to_poly_2.GetOutputPort())
edge_mapper_2.ScalarVisibilityOff()

edge_actor_2 = vtkActor()
edge_actor_2.SetMapper(edge_mapper_2)
edge_actor_2.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_2.SetPosition(5.0, 0, 0)

# --- Pipeline 3: Group by affiliation (offset 0, -2.5) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person", 0)
table_to_graph.AddLinkVertex("Affiliation", "organization", 1)
table_to_graph.AddLinkEdge("Author", "Affiliation")
table_to_graph.AddLinkEdge("Affiliation", "Author")

category_3 = vtkStringToCategory()
category_3.SetInputConnection(table_to_graph.GetOutputPort())
category_3.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_3.Update()
graph_3 = vtkUndirectedGraph()
graph_3.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_3.GetOutput()))
layout_3 = vtkGraphLayout()
layout_3.SetInputData(graph_3)
circular_layout_strategy_3 = vtkCircularLayoutStrategy()
layout_3.SetLayoutStrategy(circular_layout_strategy_3)
graph_to_poly_3 = vtkGraphToPolyData()
graph_to_poly_3.SetInputConnection(layout_3.GetOutputPort())
glyph_source_3 = vtkGlyphSource2D()
glyph_source_3.SetGlyphTypeToVertex()
vertex_glyph_3 = vtkGlyph3D()
vertex_glyph_3.SetInputConnection(0, graph_to_poly_3.GetOutputPort())
vertex_glyph_3.SetInputConnection(1, glyph_source_3.GetOutputPort())

vertex_mapper_3 = vtkPolyDataMapper()
vertex_mapper_3.SetInputConnection(vertex_glyph_3.GetOutputPort())
vertex_mapper_3.SetScalarModeToUsePointFieldData()
vertex_mapper_3.SelectColorArray("category")
range_3 = graph_3.GetVertexData().GetArray("category").GetRange()
vertex_mapper_3.SetScalarRange(range_3[0], range_3[1])

vertex_actor_3 = vtkActor()
vertex_actor_3.SetMapper(vertex_mapper_3)
vertex_actor_3.GetProperty().SetPointSize(7.0)
vertex_actor_3.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_3.SetPosition(0, -2.5, 0.001)

edge_mapper_3 = vtkPolyDataMapper()
edge_mapper_3.SetInputConnection(graph_to_poly_3.GetOutputPort())
edge_mapper_3.ScalarVisibilityOff()

edge_actor_3 = vtkActor()
edge_actor_3.SetMapper(edge_mapper_3)
edge_actor_3.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_3.SetPosition(0, -2.5, 0)

# --- Pipeline 4: Boss (offset 2.5, -2.5) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person")
table_to_graph.AddLinkVertex("Boss", "person")
table_to_graph.AddLinkEdge("Author", "Boss")

category_4 = vtkStringToCategory()
category_4.SetInputConnection(table_to_graph.GetOutputPort())
category_4.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_4.Update()
graph_4 = vtkUndirectedGraph()
graph_4.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_4.GetOutput()))
layout_4 = vtkGraphLayout()
layout_4.SetInputData(graph_4)
circular_layout_strategy_4 = vtkCircularLayoutStrategy()
layout_4.SetLayoutStrategy(circular_layout_strategy_4)
graph_to_poly_4 = vtkGraphToPolyData()
graph_to_poly_4.SetInputConnection(layout_4.GetOutputPort())
glyph_source_4 = vtkGlyphSource2D()
glyph_source_4.SetGlyphTypeToVertex()
vertex_glyph_4 = vtkGlyph3D()
vertex_glyph_4.SetInputConnection(0, graph_to_poly_4.GetOutputPort())
vertex_glyph_4.SetInputConnection(1, glyph_source_4.GetOutputPort())

vertex_mapper_4 = vtkPolyDataMapper()
vertex_mapper_4.SetInputConnection(vertex_glyph_4.GetOutputPort())
vertex_mapper_4.SetScalarModeToUsePointFieldData()
vertex_mapper_4.SelectColorArray("category")
range_4 = graph_4.GetVertexData().GetArray("category").GetRange()
vertex_mapper_4.SetScalarRange(range_4[0], range_4[1])

vertex_actor_4 = vtkActor()
vertex_actor_4.SetMapper(vertex_mapper_4)
vertex_actor_4.GetProperty().SetPointSize(7.0)
vertex_actor_4.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_4.SetPosition(2.5, -2.5, 0.001)

edge_mapper_4 = vtkPolyDataMapper()
edge_mapper_4.SetInputConnection(graph_to_poly_4.GetOutputPort())
edge_mapper_4.ScalarVisibilityOff()

edge_actor_4 = vtkActor()
edge_actor_4.SetMapper(edge_mapper_4)
edge_actor_4.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_4.SetPosition(2.5, -2.5, 0)

# --- Pipeline 5: Boss in different domain (offset 5.0, -2.5) ---
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person")
table_to_graph.AddLinkVertex("Boss", "boss")
table_to_graph.AddLinkEdge("Author", "Boss")

category_5 = vtkStringToCategory()
category_5.SetInputConnection(table_to_graph.GetOutputPort())
category_5.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_5.Update()
graph_5 = vtkUndirectedGraph()
graph_5.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_5.GetOutput()))
layout_5 = vtkGraphLayout()
layout_5.SetInputData(graph_5)
circular_layout_strategy_5 = vtkCircularLayoutStrategy()
layout_5.SetLayoutStrategy(circular_layout_strategy_5)
graph_to_poly_5 = vtkGraphToPolyData()
graph_to_poly_5.SetInputConnection(layout_5.GetOutputPort())
glyph_source_5 = vtkGlyphSource2D()
glyph_source_5.SetGlyphTypeToVertex()
vertex_glyph_5 = vtkGlyph3D()
vertex_glyph_5.SetInputConnection(0, graph_to_poly_5.GetOutputPort())
vertex_glyph_5.SetInputConnection(1, glyph_source_5.GetOutputPort())

vertex_mapper_5 = vtkPolyDataMapper()
vertex_mapper_5.SetInputConnection(vertex_glyph_5.GetOutputPort())
vertex_mapper_5.SetScalarModeToUsePointFieldData()
vertex_mapper_5.SelectColorArray("category")
range_5 = graph_5.GetVertexData().GetArray("category").GetRange()
vertex_mapper_5.SetScalarRange(range_5[0], range_5[1])

vertex_actor_5 = vtkActor()
vertex_actor_5.SetMapper(vertex_mapper_5)
vertex_actor_5.GetProperty().SetPointSize(7.0)
vertex_actor_5.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_5.SetPosition(5.0, -2.5, 0.001)

edge_mapper_5 = vtkPolyDataMapper()
edge_mapper_5.SetInputConnection(graph_to_poly_5.GetOutputPort())
edge_mapper_5.ScalarVisibilityOff()

edge_actor_5 = vtkActor()
edge_actor_5.SetMapper(edge_mapper_5)
edge_actor_5.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_5.SetPosition(5.0, -2.5, 0)

# --- Pipeline 6: Column path linking (offset 0, -5.0) ---
table_to_graph.ClearLinkVertices()
path_column = vtkStringArray()
path_domain = vtkStringArray()
path_hidden = vtkBitArray()
for col_name in ["Author", "Boss", "Affiliation", "Alma Mater", "Categories"]:
    path_column.InsertNextValue(col_name)
    path_hidden.InsertNextValue(0)
path_domain.DeepCopy(path_column)
path_domain.SetValue(0, "person")
path_domain.SetValue(1, "person")
table_to_graph.LinkColumnPath(path_column, path_domain, path_hidden)

category_6 = vtkStringToCategory()
category_6.SetInputConnection(table_to_graph.GetOutputPort())
category_6.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_6.Update()
graph_6 = vtkUndirectedGraph()
graph_6.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_6.GetOutput()))
layout_6 = vtkGraphLayout()
layout_6.SetInputData(graph_6)
circular_layout_strategy_6 = vtkCircularLayoutStrategy()
layout_6.SetLayoutStrategy(circular_layout_strategy_6)
graph_to_poly_6 = vtkGraphToPolyData()
graph_to_poly_6.SetInputConnection(layout_6.GetOutputPort())
glyph_source_6 = vtkGlyphSource2D()
glyph_source_6.SetGlyphTypeToVertex()
vertex_glyph_6 = vtkGlyph3D()
vertex_glyph_6.SetInputConnection(0, graph_to_poly_6.GetOutputPort())
vertex_glyph_6.SetInputConnection(1, glyph_source_6.GetOutputPort())

vertex_mapper_6 = vtkPolyDataMapper()
vertex_mapper_6.SetInputConnection(vertex_glyph_6.GetOutputPort())
vertex_mapper_6.SetScalarModeToUsePointFieldData()
vertex_mapper_6.SelectColorArray("category")
range_6 = graph_6.GetVertexData().GetArray("category").GetRange()
vertex_mapper_6.SetScalarRange(range_6[0], range_6[1])

vertex_actor_6 = vtkActor()
vertex_actor_6.SetMapper(vertex_mapper_6)
vertex_actor_6.GetProperty().SetPointSize(7.0)
vertex_actor_6.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_6.SetPosition(0, -5.0, 0.001)

edge_mapper_6 = vtkPolyDataMapper()
edge_mapper_6.SetInputConnection(graph_to_poly_6.GetOutputPort())
edge_mapper_6.ScalarVisibilityOff()

edge_actor_6 = vtkActor()
edge_actor_6.SetMapper(edge_mapper_6)
edge_actor_6.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_6.SetPosition(0, -5.0, 0)

# --- Pipeline 7: Vertex table (offset 2.5, -5.0) ---
table_to_graph.SetInputConnection(1, merge.GetOutputPort())
table_to_graph.ClearLinkVertices()
table_to_graph.AddLinkVertex("Author", "person.name", 0)
table_to_graph.AddLinkVertex("Affiliation", "organization.name", 0)
table_to_graph.AddLinkEdge("Author", "Affiliation")

category_7 = vtkStringToCategory()
category_7.SetInputConnection(table_to_graph.GetOutputPort())
category_7.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_VERTICES, "domain")
category_7.Update()
graph_7 = vtkUndirectedGraph()
graph_7.DeepCopy(vtkUndirectedGraph.SafeDownCast(category_7.GetOutput()))
layout_7 = vtkGraphLayout()
layout_7.SetInputData(graph_7)
circular_layout_strategy_7 = vtkCircularLayoutStrategy()
layout_7.SetLayoutStrategy(circular_layout_strategy_7)
graph_to_poly_7 = vtkGraphToPolyData()
graph_to_poly_7.SetInputConnection(layout_7.GetOutputPort())
glyph_source_7 = vtkGlyphSource2D()
glyph_source_7.SetGlyphTypeToVertex()
vertex_glyph_7 = vtkGlyph3D()
vertex_glyph_7.SetInputConnection(0, graph_to_poly_7.GetOutputPort())
vertex_glyph_7.SetInputConnection(1, glyph_source_7.GetOutputPort())

vertex_mapper_7 = vtkPolyDataMapper()
vertex_mapper_7.SetInputConnection(vertex_glyph_7.GetOutputPort())
vertex_mapper_7.SetScalarModeToUsePointFieldData()
vertex_mapper_7.SelectColorArray("category")
range_7 = graph_7.GetVertexData().GetArray("category").GetRange()
vertex_mapper_7.SetScalarRange(range_7[0], range_7[1])

vertex_actor_7 = vtkActor()
vertex_actor_7.SetMapper(vertex_mapper_7)
vertex_actor_7.GetProperty().SetPointSize(7.0)
vertex_actor_7.GetProperty().SetColor(0.7, 0.7, 0.7)
vertex_actor_7.SetPosition(2.5, -5.0, 0.001)

edge_mapper_7 = vtkPolyDataMapper()
edge_mapper_7.SetInputConnection(graph_to_poly_7.GetOutputPort())
edge_mapper_7.ScalarVisibilityOff()

edge_actor_7 = vtkActor()
edge_actor_7.SetMapper(edge_mapper_7)
edge_actor_7.GetProperty().SetColor(0.6, 0.6, 0.6)
edge_actor_7.SetPosition(2.5, -5.0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(vertex_actor_0)
renderer.AddActor(edge_actor_0)
renderer.AddActor(vertex_actor_1)
renderer.AddActor(edge_actor_1)
renderer.AddActor(vertex_actor_2)
renderer.AddActor(edge_actor_2)
renderer.AddActor(vertex_actor_3)
renderer.AddActor(edge_actor_3)
renderer.AddActor(vertex_actor_4)
renderer.AddActor(edge_actor_4)
renderer.AddActor(vertex_actor_5)
renderer.AddActor(edge_actor_5)
renderer.AddActor(vertex_actor_6)
renderer.AddActor(edge_actor_6)
renderer.AddActor(vertex_actor_7)
renderer.AddActor(edge_actor_7)
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("table to graph")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
