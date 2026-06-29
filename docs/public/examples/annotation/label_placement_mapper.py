#!/usr/bin/env python

# Test vtkLabelPlacementMapper in World, NormalizedViewport, and Display coordinates.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOXML import vtkXMLPolyDataReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
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

# Window size (non-unit aspect ratio to capture more potential errors)
window_width = 200
window_height = 600

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Shared text property
text_property = vtkTextProperty()
text_property.SetFontSize(12)
text_property.SetFontFamilyToArial()
text_property.SetColor(0.0, 0.8, 0.2)

# --- World coordinate labels ---
center = [12.0, 8.0, 30.0]

sphere = vtkSphereSource()
sphere.SetRadius(5.0)
sphere.SetCenter(center)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Read label data and translate to center
reader = vtkXMLPolyDataReader()
reader.SetFileName(os.path.join(data_dir, "uniform-001371-5x5x5.vtp"))

center_transform = vtkTransform()
center_transform.Translate(center)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetInputConnection(reader.GetOutputPort())
transform_filter.SetTransform(center_transform)

world_hierarchy = vtkPointSetToLabelHierarchy()
world_hierarchy.SetTextProperty(text_property)
world_hierarchy.AddInputConnection(transform_filter.GetOutputPort())
world_hierarchy.SetPriorityArrayName("Priority")
world_hierarchy.SetLabelArrayName("PlaceNames")
world_hierarchy.SetMaximumDepth(5)
world_hierarchy.SetTargetLabelCount(32)

world_label_mapper = vtkLabelPlacementMapper()
world_label_mapper.SetInputConnection(world_hierarchy.GetOutputPort())
world_label_mapper.SetIteratorType(vtkLabelHierarchy.QUEUE)
world_label_mapper.SetMaximumLabelFraction(0.05)
world_label_mapper.UseDepthBufferOn()

world_label_actor = vtkActor2D()
world_label_actor.SetMapper(world_label_mapper)

# --- NormalizedViewport coordinate labels ---
nv_points = vtkPoints()
nv_points.InsertNextPoint(0.05, 0.25, 0)
nv_points.InsertNextPoint(0.75, 0.75, 0)
nv_points.InsertNextPoint(0.50, 0.05, 0)
nv_points.InsertNextPoint(0.50, 0.95, 0)

nv_poly = vtkPolyData()
nv_poly.SetPoints(nv_points)

nv_labels = vtkStringArray()
nv_labels.SetName("labels")
nv_labels.InsertNextValue("NV-left")
nv_labels.InsertNextValue("NV-right")
nv_labels.InsertNextValue("NV-bottom")
nv_labels.InsertNextValue("NV-top")

nv_priority = vtkStringArray()
nv_priority.SetName("priority")
nv_priority.InsertNextValue("1")
nv_priority.InsertNextValue("1")
nv_priority.InsertNextValue("1")
nv_priority.InsertNextValue("1")

nv_poly.GetPointData().AddArray(nv_labels)
nv_poly.GetPointData().AddArray(nv_priority)

nv_hierarchy = vtkPointSetToLabelHierarchy()
nv_hierarchy.SetTextProperty(text_property)
nv_hierarchy.AddInputData(nv_poly)
nv_hierarchy.SetPriorityArrayName("priority")
nv_hierarchy.SetLabelArrayName("labels")

nv_label_mapper = vtkLabelPlacementMapper()
nv_label_mapper.SetInputConnection(nv_hierarchy.GetOutputPort())
nv_label_mapper.PlaceAllLabelsOn()
nv_label_mapper.GetAnchorTransform().SetCoordinateSystemToNormalizedViewport()
nv_label_mapper.UseDepthBufferOff()

nv_label_actor = vtkActor2D()
nv_label_actor.SetMapper(nv_label_mapper)

# --- Display coordinate labels ---
display_points = vtkPoints()
display_points.InsertNextPoint(window_width * 0.01, window_height * 0.01, 0)
display_points.InsertNextPoint(window_width * 0.90, window_height * 0.01, 0)
display_points.InsertNextPoint(window_width * 0.01, window_height * 0.97, 0)
display_points.InsertNextPoint(window_width * 0.90, window_height * 0.97, 0)

display_poly = vtkPolyData()
display_poly.SetPoints(display_points)

display_labels = vtkStringArray()
display_labels.SetName("labels")
display_labels.InsertNextValue("D-bottom-left")
display_labels.InsertNextValue("D-bottom-right")
display_labels.InsertNextValue("D-top-left")
display_labels.InsertNextValue("D-top-right")

display_priority = vtkStringArray()
display_priority.SetName("priority")
display_priority.InsertNextValue("1")
display_priority.InsertNextValue("1")
display_priority.InsertNextValue("1")
display_priority.InsertNextValue("1")

display_poly.GetPointData().AddArray(display_labels)
display_poly.GetPointData().AddArray(display_priority)

display_hierarchy = vtkPointSetToLabelHierarchy()
display_hierarchy.SetTextProperty(text_property)
display_hierarchy.AddInputData(display_poly)
display_hierarchy.SetPriorityArrayName("priority")
display_hierarchy.SetLabelArrayName("labels")

display_label_mapper = vtkLabelPlacementMapper()
display_label_mapper.SetInputConnection(display_hierarchy.GetOutputPort())
display_label_mapper.PlaceAllLabelsOn()
display_label_mapper.GetAnchorTransform().SetCoordinateSystemToDisplay()
display_label_mapper.UseDepthBufferOff()

display_label_actor = vtkActor2D()
display_label_actor.SetMapper(display_label_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(sphere_actor)
renderer.AddActor(world_label_actor)
renderer.AddActor(nv_label_actor)
renderer.AddActor(display_label_actor)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(window_width, window_height)
render_window.AddRenderer(renderer)
render_window.SetWindowName("label placement mapper")

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
