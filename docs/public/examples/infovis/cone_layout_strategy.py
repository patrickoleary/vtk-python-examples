#!/usr/bin/env python
# Demonstrate vtkConeLayoutStrategy with a tree read from XML, showing vertex and edge labels.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkIdTypeArray, vtkStringArray
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkFiltersSources import vtkGraphToPolyData
from vtkmodules.vtkInfovisCore import vtkStringToNumeric
from vtkmodules.vtkInfovisLayout import vtkConeLayoutStrategy, vtkGraphLayout
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

# Colors (normalized RGB).
navy_rgb = (0.0, 0.0, 0.502)
midnight_blue_rgb = (0.098, 0.098, 0.439)

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

# Layout with cone strategy.
graph_layout = vtkGraphLayout()
graph_layout.SetInputConnection(string_to_numeric.GetOutputPort())
strategy = vtkConeLayoutStrategy()
strategy.SetSpacing(0.3)
graph_layout.SetLayoutStrategy(strategy)

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

# Vertex glyphs.
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.SetInputConnection(graph_to_polydata.GetOutputPort())

vertex_mapper = vtkPolyDataMapper()
vertex_mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())
vertex_mapper.ScalarVisibilityOff()
vertex_actor = vtkActor()
vertex_actor.SetMapper(vertex_mapper)
vertex_actor.GetProperty().SetColor(1.0, 0.5, 0.0)
vertex_actor.GetProperty().SetPointSize(6)

# Non-overlapping vertex labels using label placement.
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputConnection(vertex_glyph_filter.GetOutputPort())
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

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(vertex_actor)
renderer.AddActor(label_actor)
renderer.SetBackground(navy_rgb)
renderer.SetBackground2(midnight_blue_rgb)
renderer.GradientBackgroundOn()
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cone layout strategy")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
