#!/usr/bin/env python
# Demonstrate vtkGraphLayout with circular layout, vertex/edge coloring and labels.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIdTypeArray, vtkStringArray
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkStringToNumeric
from vtkmodules.vtkInfovisLayout import vtkCircularLayoutStrategy, vtkGraphLayout
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

# Colors (normalized RGB).
navy_rgb = (0.0, 0.0, 0.502)

# Read tree from XML.
reader = vtkXMLTreeReader()
reader.SetFileName(os.path.join(data_dir, "vtkclasses.xml"))
reader.SetMaskArrays(True)
reader.Update()

tree = reader.GetOutput()

# Add edge arrays.
edge_labels = vtkStringArray()
edge_labels.SetName("edge label")
edge_distance = vtkIdTypeArray()
edge_distance.SetName("distance")
labels = ["a", "b", "c"]
for i in range(tree.GetNumberOfEdges()):
    edge_distance.InsertNextValue(i)
    edge_labels.InsertNextValue(labels[i % 3])
tree.GetEdgeData().AddArray(edge_distance)
tree.GetEdgeData().AddArray(edge_labels)

# Convert string columns to numeric.
string_to_numeric = vtkStringToNumeric()
string_to_numeric.SetInputData(tree)

# Layout with circular strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(string_to_numeric.GetOutputPort())
circular_layout_strategy = vtkCircularLayoutStrategy()
graph_layout.SetLayoutStrategy(circular_layout_strategy)

# Convert graph to polydata.
graph_to_polydata = vtkGraphToPolyData()
graph_to_polydata.SetInputConnection(graph_layout.GetOutputPort())
graph_to_polydata.Update()

# Edge mapper and actor (colored by "distance").
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_mapper.SetScalarModeToUseCellFieldData()
edge_mapper.SelectColorArray("distance")
edge_mapper.SetScalarVisibility(True)
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Edge labels.
edge_label_mapper = vtkLabeledDataMapper()
edge_label_mapper.SetInputConnection(graph_to_polydata.GetOutputPort())
edge_label_mapper.SetLabelModeToLabelFieldData()
edge_label_mapper.SetFieldDataName("edge label")
edge_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 0.0)
edge_label_actor = vtkActor2D()
edge_label_actor.SetMapper(edge_label_mapper)

# Vertex glyphs (colored by "size").
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.SetScalarModeToUsePointFieldData()
vertex_mapper.SelectColorArray("size")
vertex_mapper.SetScalarVisibility(True)
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetPointSize(8)

# Vertex labels.
vertex_label_mapper = vtkLabeledDataMapper()
vertex_label_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_label_mapper.SetLabelModeToLabelFieldData()
vertex_label_mapper.SetFieldDataName("name")
vertex_label_mapper.GetLabelTextProperty().SetColor(1.0, 1.0, 1.0)
vertex_label_mapper.GetLabelTextProperty().SetFontSize(10)
vertex_label_actor = vtkActor2D()
vertex_label_actor.SetMapper(vertex_label_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(edge_label_actor)
renderer.AddActor(vertex_label_actor)
renderer.SetBackground(navy_rgb)
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("graph layout view")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
