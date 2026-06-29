#!/usr/bin/env python

# Test picking of images with vtkCellPicker across multiple orientations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkDataSetMapper,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read headsq data
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
# use negative spacing to strengthen the testing
reader.SetDataSpacing(3.2, 3.2, -1.5)
# a nice random-ish origin for testing
reader.SetDataOrigin(2.5, -13.6, 2.8)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.Update()

# Cone source for pick markers
cone_source = vtkConeSource()
cone_source.CappingOn()
cone_source.SetHeight(24)
cone_source.SetRadius(8)
cone_source.SetResolution(31)
cone_source.SetCenter(12, 0, 0)
cone_source.SetDirection(-1, 0, 0)

# Viewport 0: orientation 0 (YZ plane)
image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())
image_mapper_0.SliceAtFocalPointOn()
image_mapper_0.SetOrientation(0)

image_0 = vtkImageSlice()
image_0.SetMapper(image_mapper_0)
image_0.GetProperty().SetColorWindow(2000)
image_0.GetProperty().SetColorLevel(1000)

# Viewport 1: orientation 1 (XZ plane)
image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())
image_mapper_1.SliceAtFocalPointOn()
image_mapper_1.SetOrientation(1)

image_1 = vtkImageSlice()
image_1.SetMapper(image_mapper_1)
image_1.GetProperty().SetColorWindow(2000)
image_1.GetProperty().SetColorLevel(1000)

# Viewport 2: orientation 2 (XY plane)
image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(reader.GetOutputPort())
image_mapper_2.SliceAtFocalPointOn()
image_mapper_2.SetOrientation(2)

image_2 = vtkImageSlice()
image_2.SetMapper(image_mapper_2)
image_2.GetProperty().SetColorWindow(2000)
image_2.GetProperty().SetColorLevel(1000)

# Viewport 3: default orientation (2), oblique view
image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(reader.GetOutputPort())
image_mapper_3.SliceAtFocalPointOn()

image_3 = vtkImageSlice()
image_3.SetMapper(image_mapper_3)
image_3.GetProperty().SetColorWindow(2000)
image_3.GetProperty().SetColorLevel(1000)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_0.AddViewProp(image_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_1.AddViewProp(image_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.AddViewProp(image_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddViewProp(image_3)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("cell picker")

# Scene
bounds_0 = image_mapper_0.GetBounds()
point_0 = [0.5 * (bounds_0[0] + bounds_0[1]), 0.5 * (bounds_0[2] + bounds_0[3]), 0.5 * (bounds_0[4] + bounds_0[5])]
point_0[0] += 30.0
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[0] += 470.0
camera_0.SetPosition(point_0)
camera_0.SetClippingRange(250, 750)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(120.0)
camera_0.SetViewUp(0.0, 0.0, 1.0)

bounds_1 = image_mapper_1.GetBounds()
point_1 = [0.5 * (bounds_1[0] + bounds_1[1]), 0.5 * (bounds_1[2] + bounds_1[3]), 0.5 * (bounds_1[4] + bounds_1[5])]
point_1[1] += 30.0
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[1] += 470.0
camera_1.SetPosition(point_1)
camera_1.SetClippingRange(250, 750)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(120.0)
camera_1.SetViewUp(0.0, 0.0, 1.0)

bounds_2 = image_mapper_2.GetBounds()
point_2 = [0.5 * (bounds_2[0] + bounds_2[1]), 0.5 * (bounds_2[2] + bounds_2[3]), 0.5 * (bounds_2[4] + bounds_2[5])]
point_2[2] += 30.0
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(point_2)
point_2[2] += 470.0
camera_2.SetPosition(point_2)
camera_2.SetClippingRange(250, 750)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(120.0)

bounds_3 = image_mapper_3.GetBounds()
point_3 = [0.5 * (bounds_3[0] + bounds_3[1]), 0.5 * (bounds_3[2] + bounds_3[3]), 0.5 * (bounds_3[4] + bounds_3[5])]
point_3[image_mapper_3.GetOrientation()] += 30.0
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(point_3)
point_3[image_mapper_3.GetOrientation()] += 470.0
camera_3.SetPosition(point_3)
camera_3.SetClippingRange(250, 750)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(120.0)
camera_3.Azimuth(30)
camera_3.Elevation(40)

# Functional render: required to populate image data before picking
render_window.Render()

# Pick at specific positions and place cone markers
picker = vtkCellPicker()
picker.SetTolerance(1e-6)

# Pick viewport 0
picker.Pick(120, 90, 0.0, renderer_0)
pick_pos_0 = picker.GetPickPosition()
pick_normal_0 = picker.GetPickNormal()

cone_mapper_0 = vtkDataSetMapper()
cone_mapper_0.SetInputConnection(cone_source.GetOutputPort())

cone_actor_0 = vtkActor()
cone_actor_0.PickableOff()
cone_actor_0.SetMapper(cone_mapper_0)
cone_actor_0.GetProperty().SetColor(1, 0, 0)
cone_actor_0.SetPosition(pick_pos_0[0], pick_pos_0[1], pick_pos_0[2])
if pick_normal_0[0] < 0.0:
    cone_actor_0.RotateWXYZ(180, 0, 1, 0)
    cone_actor_0.RotateWXYZ(180, (pick_normal_0[0] - 1.0) * 0.5, pick_normal_0[1] * 0.5, pick_normal_0[2] * 0.5)
else:
    cone_actor_0.RotateWXYZ(180, (pick_normal_0[0] + 1.0) * 0.5, pick_normal_0[1] * 0.5, pick_normal_0[2] * 0.5)

renderer_0.AddViewProp(cone_actor_0)

# Pick viewport 1
picker.Pick(278, 99, 0.0, renderer_1)
pick_pos_1 = picker.GetPickPosition()
pick_normal_1 = picker.GetPickNormal()

cone_mapper_1 = vtkDataSetMapper()
cone_mapper_1.SetInputConnection(cone_source.GetOutputPort())

cone_actor_1 = vtkActor()
cone_actor_1.PickableOff()
cone_actor_1.SetMapper(cone_mapper_1)
cone_actor_1.GetProperty().SetColor(1, 0, 0)
cone_actor_1.SetPosition(pick_pos_1[0], pick_pos_1[1], pick_pos_1[2])
if pick_normal_1[0] < 0.0:
    cone_actor_1.RotateWXYZ(180, 0, 1, 0)
    cone_actor_1.RotateWXYZ(180, (pick_normal_1[0] - 1.0) * 0.5, pick_normal_1[1] * 0.5, pick_normal_1[2] * 0.5)
else:
    cone_actor_1.RotateWXYZ(180, (pick_normal_1[0] + 1.0) * 0.5, pick_normal_1[1] * 0.5, pick_normal_1[2] * 0.5)

renderer_1.AddViewProp(cone_actor_1)

# Pick viewport 2
picker.Pick(90, 310, 0.0, renderer_2)
pick_pos_2 = picker.GetPickPosition()
pick_normal_2 = picker.GetPickNormal()

cone_mapper_2 = vtkDataSetMapper()
cone_mapper_2.SetInputConnection(cone_source.GetOutputPort())

cone_actor_2 = vtkActor()
cone_actor_2.PickableOff()
cone_actor_2.SetMapper(cone_mapper_2)
cone_actor_2.GetProperty().SetColor(1, 0, 0)
cone_actor_2.SetPosition(pick_pos_2[0], pick_pos_2[1], pick_pos_2[2])
if pick_normal_2[0] < 0.0:
    cone_actor_2.RotateWXYZ(180, 0, 1, 0)
    cone_actor_2.RotateWXYZ(180, (pick_normal_2[0] - 1.0) * 0.5, pick_normal_2[1] * 0.5, pick_normal_2[2] * 0.5)
else:
    cone_actor_2.RotateWXYZ(180, (pick_normal_2[0] + 1.0) * 0.5, pick_normal_2[1] * 0.5, pick_normal_2[2] * 0.5)

renderer_2.AddViewProp(cone_actor_2)

# Pick viewport 3
picker.Pick(250, 260, 0.0, renderer_3)
pick_pos_3 = picker.GetPickPosition()
pick_normal_3 = picker.GetPickNormal()

cone_mapper_3 = vtkDataSetMapper()
cone_mapper_3.SetInputConnection(cone_source.GetOutputPort())

cone_actor_3 = vtkActor()
cone_actor_3.PickableOff()
cone_actor_3.SetMapper(cone_mapper_3)
cone_actor_3.GetProperty().SetColor(1, 0, 0)
cone_actor_3.SetPosition(pick_pos_3[0], pick_pos_3[1], pick_pos_3[2])
if pick_normal_3[0] < 0.0:
    cone_actor_3.RotateWXYZ(180, 0, 1, 0)
    cone_actor_3.RotateWXYZ(180, (pick_normal_3[0] - 1.0) * 0.5, pick_normal_3[1] * 0.5, pick_normal_3[2] * 0.5)
else:
    cone_actor_3.RotateWXYZ(180, (pick_normal_3[0] + 1.0) * 0.5, pick_normal_3[1] * 0.5, pick_normal_3[2] * 0.5)

renderer_3.AddViewProp(cone_actor_3)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
