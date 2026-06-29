#!/usr/bin/env python

# Visualize spatial decomposition of an STL model using three different
# locators: vtkPointLocator, vtkCellLocator, and vtkOBBTree via
# vtkSpatialRepresentationFilter.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellLocator,
    vtkPointLocator,
)
from vtkmodules.vtkFiltersGeneral import (
    vtkOBBTree,
    vtkSpatialRepresentationFilter,
)
from vtkmodules.vtkIOGeometry import vtkSTLReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read STL model
reader = vtkSTLReader()
reader.SetFileName(os.path.join(data_dir, "42400-IDGH.stl"))

data_mapper = vtkPolyDataMapper()
data_mapper.SetInputConnection(reader.GetOutputPort())

model_actor = vtkActor()
model_actor.SetMapper(data_mapper)
model_actor.GetProperty().SetColor(1, 0, 0)
model_actor.VisibilityOn()

# vtkPointLocator decomposition
point_locator = vtkPointLocator()
point_locator.AutomaticOff()
point_locator.SetMaxLevel(3)

point_boxes = vtkSpatialRepresentationFilter()
point_boxes.SetInputConnection(reader.GetOutputPort())
point_boxes.SetSpatialRepresentation(point_locator)
point_boxes.SetGenerateLeaves(1)
point_boxes.Update()

point_output = point_boxes.GetOutput().GetBlock(point_boxes.GetMaximumLevel() + 1)

point_box_mapper = vtkPolyDataMapper()
point_box_mapper.SetInputData(point_output)

point_box_actor = vtkActor()
point_box_actor.SetMapper(point_box_mapper)
point_box_actor.AddPosition(15, 0, 0)

# vtkCellLocator decomposition
cell_locator = vtkCellLocator()
cell_locator.AutomaticOff()
cell_locator.SetMaxLevel(3)

cell_boxes = vtkSpatialRepresentationFilter()
cell_boxes.SetInputConnection(reader.GetOutputPort())
cell_boxes.SetSpatialRepresentation(cell_locator)
cell_boxes.SetGenerateLeaves(1)
cell_boxes.Update()

cell_output = cell_boxes.GetOutput().GetBlock(cell_boxes.GetMaximumLevel() + 1)

cell_box_mapper = vtkPolyDataMapper()
cell_box_mapper.SetInputData(cell_output)

cell_box_actor = vtkActor()
cell_box_actor.SetMapper(cell_box_mapper)
cell_box_actor.AddPosition(30, 0, 0)

# vtkOBBTree decomposition
obb_tree = vtkOBBTree()
obb_tree.AutomaticOff()
obb_tree.SetMaxLevel(3)

obb_boxes = vtkSpatialRepresentationFilter()
obb_boxes.SetInputConnection(reader.GetOutputPort())
obb_boxes.SetSpatialRepresentation(obb_tree)
obb_boxes.SetGenerateLeaves(1)
obb_boxes.Update()

obb_output = obb_boxes.GetOutput().GetBlock(obb_boxes.GetMaximumLevel() + 1)

obb_box_mapper = vtkPolyDataMapper()
obb_box_mapper.SetInputData(obb_output)

obb_box_actor = vtkActor()
obb_box_actor.SetMapper(obb_box_mapper)
obb_box_actor.AddPosition(45, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(model_actor)
renderer.AddActor(point_box_actor)
renderer.AddActor(cell_box_actor)
renderer.AddActor(obb_box_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(400, 160)
render_window.SetWindowName("spatial rep all")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetPosition(148.579, 136.352, 214.961)
camera.SetFocalPoint(151.889, 86.3178, 223.333)
camera.SetViewAngle(30)
camera.SetViewUp(0, 0, -1)
camera.SetClippingRange(1, 100)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
