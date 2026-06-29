#!/usr/bin/env python

# Test vtkLabelPlacer with a label hierarchy on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
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
target_labels = 32
label_ratio = 0.05
iterator_type = vtkLabelHierarchy.QUEUE
show_bounds = False

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Sphere geometry
sphere = vtkSphereSource()
sphere.SetRadius(5.0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Read label data
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "uniform-001371-5x5x5.vtp"))

# Calculate label sizes
label_size_calculator = vtkLabelSizeCalculator()
label_size_calculator.SetInputConnection(reader.GetOutputPort())
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
label_placer.UseDepthBufferOn()

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
renderer.AddActor(sphere_actor)
renderer.AddActor(text_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placer")

# Functional render: establish viewport for label placement
render_window.Render()

# Scene
renderer.ResetCamera()
renderer.ResetCamera()
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
