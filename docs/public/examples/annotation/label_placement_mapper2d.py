#!/usr/bin/env python

# Test vtkLabelPlacementMapper in 2D with a large set of randomly placed ship-name labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import json
import os

from vtkmodules.vtkCommonCore import (
    vtkIdTypeArray,
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLabel import (
    vtkLabelPlacementMapper,
    vtkPointSetToLabelHierarchy,
)

# Grid layout constants
PTSMULT = 10
TXTMULT = PTSMULT * PTSMULT

# Load label data from JSON files
data_dir = os.environ.get("VPE_DATA_DIR", os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data"))
with open(os.path.join(data_dir, "label_list_2d.json")) as f:
    label_list = json.load(f)
with open(os.path.join(data_dir, "label_points_2d.json")) as f:
    point_coords = json.load(f)

num_labels = len(label_list)
total_points = TXTMULT * num_labels

# Build point set
label_points = vtkPoints()
label_points.SetNumberOfPoints(total_points)

label_text = vtkStringArray()
label_text.SetName("LabelText")
label_text.SetNumberOfValues(total_points)

priorities = vtkIdTypeArray()
priorities.SetName("Priorities")
priorities.SetNumberOfComponents(1)
priorities.SetNumberOfTuples(total_points)

pt_idx = 0
for i in range(total_points):
    label_text.SetValue(i, label_list[i % num_labels])
    priorities.SetValue(i, i)
    if i % num_labels == 0:
        pt_idx = 0
    x = point_coords[pt_idx * 2] + float((i // num_labels) % PTSMULT)
    y = point_coords[pt_idx * 2 + 1] + float((i // num_labels) // PTSMULT)
    label_points.SetPoint(i, x, y, -1.0)
    pt_idx += 1

poly_data = vtkPolyData()
poly_data.SetPoints(label_points)
poly_data.GetPointData().AddArray(label_text)
poly_data.GetPointData().AddArray(priorities)

# Text property
text_property = vtkTextProperty()
text_property.SetFontSize(12)
text_property.SetFontFamilyToArial()

# Build label hierarchy
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputData(poly_data)
label_hierarchy.SetTextProperty(text_property)
label_hierarchy.SetPriorityArrayName("Priorities")
label_hierarchy.SetLabelArrayName("LabelText")

# Place labels
label_mapper = vtkLabelPlacementMapper()
label_mapper.SetInputConnection(label_hierarchy.GetOutputPort())
label_mapper.GeneratePerturbedLabelSpokesOn()
label_mapper.OutputTraversedBoundsOn()

text_actor = vtkActor2D()
text_actor.SetMapper(label_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(text_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placement mapper2d")

# Functional render: establish viewport for label placement
render_window.Render()

# Scene
camera = renderer.GetActiveCamera()
camera.SetClippingRange(0.0106829, 10.6829)
camera.SetFocalPoint(5.00016, 4.99974, -1.0)
camera.SetPosition(4.91977, 4.45127, -0.859406)
camera.SetViewUp(-0.0373979, 0.253276, 0.966671)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
