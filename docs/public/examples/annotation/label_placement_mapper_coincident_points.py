#!/usr/bin/env python

# Test vtkLabelPlacementMapper with coincident points (all at origin except one).

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLabel import (
    vtkLabelHierarchy,
    vtkLabelPlacementMapper,
    vtkPointSetToLabelHierarchy,
)

# Parameters
max_levels = 5
target_labels = 7
label_ratio = 1.0
iterator_type = vtkLabelHierarchy.QUEUE

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

# Text property
text_property = vtkTextProperty()
text_property.SetFontSize(12)
text_property.SetFontFamilyToArial()
text_property.SetColor(0.0, 0.8, 0.2)

# Build label hierarchy
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputData(poly_data)
label_hierarchy.SetTextProperty(text_property)
label_hierarchy.SetPriorityArrayName("Priority")
label_hierarchy.SetLabelArrayName("PlaceNames")
label_hierarchy.SetMaximumDepth(max_levels)
label_hierarchy.SetTargetLabelCount(target_labels)

# Place labels
label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())
label_mapper.SetIteratorType(iterator_type)
label_mapper.SetMaximumLabelFraction(label_ratio)

text_actor = vtkActor2D()
text_actor.SetMapper(label_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(text_actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placement mapper coincident points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
