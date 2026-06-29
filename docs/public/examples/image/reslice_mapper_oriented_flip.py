#!/usr/bin/env python

# Test images with Direction that has negative determinant (flip) with vtkImageResliceMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingImage import vtkImageResliceMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Compute a direction matrix with a flip for testing
trans = vtkTransform()
trans.RotateWXYZ(20, 0.7071067811865476, 0.0, 0.7071067811865476)
# apply an anterior-posterior flip to the orientation
trans.Scale(1.0, -1.0, 1.0)

column_0 = list(trans.TransformVector(1.0, 0.0, 0.0))
column_1 = list(trans.TransformVector(0.0, 1.0, 0.0))
column_2 = list(trans.TransformVector(0.0, 0.0, 1.0))

direction = [
    column_0[0], column_1[0], column_2[0],
    column_0[1], column_1[1], column_2[1],
    column_0[2], column_1[2], column_2[2],
]

# Read headsq data with flipped direction
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataDirection(direction)
reader.SetDataOrigin(2.5, -13.6, 2.8)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.Update()

# Viewport 0: texture interpolation, camera along X axis
image_mapper_0 = vtkImageResliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())
image_mapper_0.SliceAtFocalPointOn()
image_mapper_0.SliceFacesCameraOn()
image_mapper_0.ResampleToScreenPixelsOff()

image_0 = vtkImageSlice()
image_0.SetMapper(image_mapper_0)
image_0.GetProperty().SetColorWindow(2000)
image_0.GetProperty().SetColorLevel(1000)

# Viewport 1: texture interpolation, camera along Y axis
image_mapper_1 = vtkImageResliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())
image_mapper_1.SliceAtFocalPointOn()
image_mapper_1.SliceFacesCameraOn()
image_mapper_1.ResampleToScreenPixelsOff()

image_1 = vtkImageSlice()
image_1.SetMapper(image_mapper_1)
image_1.GetProperty().SetColorWindow(2000)
image_1.GetProperty().SetColorLevel(1000)

# Viewport 2: reslice interpolation, camera along Z axis
image_mapper_2 = vtkImageResliceMapper()
image_mapper_2.SetInputConnection(reader.GetOutputPort())
image_mapper_2.SliceAtFocalPointOn()
image_mapper_2.SliceFacesCameraOn()
image_mapper_2.ResampleToScreenPixelsOn()

image_2 = vtkImageSlice()
image_2.SetMapper(image_mapper_2)
image_2.GetProperty().SetColorWindow(2000)
image_2.GetProperty().SetColorLevel(1000)

# Viewport 3: reslice interpolation, camera along X axis, oblique view
image_mapper_3 = vtkImageResliceMapper()
image_mapper_3.SetInputConnection(reader.GetOutputPort())
image_mapper_3.SliceAtFocalPointOn()
image_mapper_3.SliceFacesCameraOn()
image_mapper_3.ResampleToScreenPixelsOn()

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
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("reslice mapper oriented flip")

# Scene
bounds_0 = image_mapper_0.GetBounds()
point_0 = [0.5 * (bounds_0[0] + bounds_0[1]), 0.5 * (bounds_0[2] + bounds_0[3]), 0.5 * (bounds_0[4] + bounds_0[5])]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[0] += 500.0
camera_0.SetPosition(point_0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(120.0)
camera_0.SetViewUp(0.0, 0.0, -1.0)

bounds_1 = image_mapper_1.GetBounds()
point_1 = [0.5 * (bounds_1[0] + bounds_1[1]), 0.5 * (bounds_1[2] + bounds_1[3]), 0.5 * (bounds_1[4] + bounds_1[5])]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[1] += 500.0
camera_1.SetPosition(point_1)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(120.0)
camera_1.SetViewUp(0.0, 0.0, -1.0)

bounds_2 = image_mapper_2.GetBounds()
point_2 = [0.5 * (bounds_2[0] + bounds_2[1]), 0.5 * (bounds_2[2] + bounds_2[3]), 0.5 * (bounds_2[4] + bounds_2[5])]
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(point_2)
point_2[2] += 500.0
camera_2.SetPosition(point_2)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(120.0)

bounds_3 = image_mapper_3.GetBounds()
point_3 = [0.5 * (bounds_3[0] + bounds_3[1]), 0.5 * (bounds_3[2] + bounds_3[3]), 0.5 * (bounds_3[4] + bounds_3[5])]
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(point_3)
point_3[0] += 500.0
camera_3.SetPosition(point_3)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(120.0)
camera_3.SetViewUp(0.0, 0.0, -1.0)
camera_3.Azimuth(30)
camera_3.Elevation(40)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
