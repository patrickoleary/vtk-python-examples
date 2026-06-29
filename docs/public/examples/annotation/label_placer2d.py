#!/usr/bin/env python

# Test vtkLabelPlacer in 2D with a large set of randomly placed ship-name labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import json
import os

from vtkmodules.vtkCommonCore import (
    vtkIdTypeArray,
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import (
    vtkLabelPlacer,
    vtkLabelSizeCalculator,
    vtkLabeledDataMapper,
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

# Calculate label sizes
label_size_calculator = vtkLabelSizeCalculator()
label_size_calculator.SetInputData(poly_data)
label_size_calculator.GetFontProperty().SetFontSize(12)
label_size_calculator.GetFontProperty().SetFontFamilyToArial()
label_size_calculator.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "LabelText")

# Build label hierarchy
label_hierarchy = vtkPointSetToLabelHierarchy()
label_hierarchy.SetInputConnection(label_size_calculator.GetOutputPort())
label_hierarchy.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Priorities")
label_hierarchy.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "LabelSize")
label_hierarchy.SetInputArrayToProcess(
    2, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "LabelText")

# Renderer (functional exception: needed by vtkLabelPlacer.SetRenderer)
renderer = vtkRenderer()

# Place labels
label_placer = vtkLabelPlacer()
label_placer.SetInputConnection(label_hierarchy.GetOutputPort())
label_placer.GeneratePerturbedLabelSpokesOn()
label_placer.OutputTraversedBoundsOn()
label_placer.SetRenderer(renderer)

# Label text display
labeled_mapper = vtkLabeledDataMapper()
labeled_mapper.SetInputConnection(label_placer.GetOutputPort(0))
labeled_mapper.SetLabelTextProperty(label_size_calculator.GetFontProperty())
labeled_mapper.SetFieldDataName("LabelText")
labeled_mapper.SetLabelModeToLabelFieldData()

text_actor = vtkActor2D()
text_actor.SetMapper(labeled_mapper)

# Bounds display
bounds_mapper = vtkPolyDataMapper()
bounds_mapper.SetInputConnection(label_placer.GetOutputPort(2))

bounds_actor = vtkActor()
bounds_actor.SetMapper(bounds_mapper)

# Spokes display
spokes_mapper = vtkPolyDataMapper()
spokes_mapper.SetInputConnection(label_placer.GetOutputPort(3))

spokes_actor = vtkActor()
spokes_actor.SetMapper(spokes_mapper)

# Add actors
renderer.AddActor(text_actor)
renderer.AddActor(bounds_actor)
renderer.AddActor(spokes_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placer2d")

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
