#!/usr/bin/env python

# Test vtkLabelPlacer with coincident points (all at origin except one).

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkDataObject,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import (
    vtkLabelHierarchy,
    vtkLabelPlacer,
    vtkLabelSizeCalculator,
    vtkLabeledDataMapper,
    vtkPointSetToLabelHierarchy,
)

# Parameters
max_levels = 5
target_labels = 7
label_ratio = 1.0
iterator_type = vtkLabelHierarchy.QUEUE
show_bounds = True

# Create points — 29 at the origin, 1 offset
points = vtkPoints()
for i in range(29):
    points.InsertPoint(i, 0.0, 0.0, 0.0)
points.InsertPoint(29, 2.2, 2.2, 0.0)

# Vertex cells
vertex_cells = vtkCellArray()
vertex_cells.InsertNextCell(30)
for i in range(30):
    vertex_cells.InsertCellPoint(i)

# Build polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetVerts(vertex_cells)

# Label strings
place_names = [
    "Abu Dhabi", "Amsterdam", "Beijing", "Berlin", "Cairo",
    "Caracas", "Dublin", "Georgetown", "The Hague", "Hanoi",
    "Islamabad", "Jakarta", "Kiev", "Kingston", "Lima",
    "London", "Luxembourg City", "Madrid", "Moscow", "Nairobi",
    "New Delhi", "Ottawa", "Paris", "Prague", "Rome",
    "Seoul", "Tehran", "Tokyo", "Warsaw", "Washington",
]

string_data = vtkStringArray()
string_data.SetName("PlaceNames")
for name in place_names:
    string_data.InsertNextValue(name)
poly_data.GetPointData().AddArray(string_data)

# Calculate label sizes
label_size_calculator = vtkLabelSizeCalculator()
label_size_calculator.SetInputData(poly_data)
label_size_calculator.GetFontProperty().SetFontSize(12)
label_size_calculator.GetFontProperty().SetFontFamilyToArial()
label_size_calculator.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "PlaceNames")
label_size_calculator.SetLabelSizeArrayName("LabelSize")

# Build label hierarchy
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.AddInputConnection(label_size_calculator.GetOutputPort())
label_hierarchy.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Priority")
label_hierarchy.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "LabelSize")
label_hierarchy.SetInputArrayToProcess(
    2, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "PlaceNames")
label_hierarchy.SetMaximumDepth(max_levels)
label_hierarchy.SetTargetLabelCount(target_labels)

# Renderer (functional exception: needed by vtkLabelPlacer.SetRenderer)
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)

# Place labels
label_placer = vtkLabelPlacer()
label_placer.SetInputConnection(label_hierarchy.GetOutputPort())
label_placer.SetIteratorType(iterator_type)
label_placer.SetOutputTraversedBounds(show_bounds)
label_placer.SetRenderer(renderer)
label_placer.SetMaximumLabelFraction(label_ratio)

# Display labels
labeled_mapper = vtkLabeledDataMapper()
labeled_mapper.SetInputConnection(label_placer.GetOutputPort())
labeled_mapper.SetLabelTextProperty(label_size_calculator.GetFontProperty())
labeled_mapper.SetFieldDataName("LabelText")
labeled_mapper.SetLabelModeToLabelFieldData()
labeled_mapper.GetLabelTextProperty().SetColor(0.0, 0.8, 0.2)

text_actor = vtkActor2D()
text_actor.SetMapper(labeled_mapper)

# Add actors
renderer.AddActor(text_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placer coincident points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
