#!/usr/bin/env python

# Test vtkImageSincInterpolator SlidingWindow on 3D volume with multiple views.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import VTK_DOUBLE, VTK_FLOAT
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingCore import (
    vtkImageInterpolator,
    vtkImageReslice,
    vtkImageSincInterpolator,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read 3D volume
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Sinc interpolation with sliding window
interpolator = vtkImageSincInterpolator()
interpolator.SlidingWindowOn()

reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputSpacing(0.80, 0.80, 1.5001)
reslice.SetInterpolator(interpolator)
reslice.SetOutputScalarType(VTK_DOUBLE)
reslice.Update()

# Nearest-neighbor with sliding window for lower-right viewport
nearest = vtkImageInterpolator()
nearest.SetInterpolationModeToNearest()
nearest.SlidingWindowOn()

reslice2 = vtkImageReslice()
reslice2.SetInputConnection(reader.GetOutputPort())
reslice2.SetOutputSpacing(0.80, 0.80, 1.5)
reslice2.SetOutputScalarType(VTK_FLOAT)
reslice2.SetInterpolator(nearest)
reslice2.Update()

color_range = [0, 4095]

# Viewport 0 (lower-left): sinc reslice, orientation 0
image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reslice.GetOutputPort())
image_mapper_0.SetOrientation(0)
image_mapper_0.SliceAtFocalPointOn()

image_slice_0 = vtkImageSlice()
image_slice_0.SetMapper(image_mapper_0)
image_slice_0.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_0.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_0.GetProperty().SetInterpolationTypeToNearest()

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(image_slice_0)
renderer_0.SetBackground(0.0, 0.0, 0.0)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# Viewport 1 (lower-right): sinc reslice, orientation 1
image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reslice.GetOutputPort())
image_mapper_1.SetOrientation(1)
image_mapper_1.SliceAtFocalPointOn()

image_slice_1 = vtkImageSlice()
image_slice_1.SetMapper(image_mapper_1)
image_slice_1.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_1.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_1.GetProperty().SetInterpolationTypeToNearest()

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(image_slice_1)
renderer_1.SetBackground(0.0, 0.0, 0.0)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# Viewport 2 (upper-left): sinc reslice, orientation 2
image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(reslice.GetOutputPort())
image_mapper_2.SetOrientation(2)
image_mapper_2.SliceAtFocalPointOn()

image_slice_2 = vtkImageSlice()
image_slice_2.SetMapper(image_mapper_2)
image_slice_2.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_2.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_2.GetProperty().SetInterpolationTypeToNearest()

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(image_slice_2)
renderer_2.SetBackground(0.0, 0.0, 0.0)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# Viewport 3 (upper-right): nearest reslice2, orientation 0
image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(reslice2.GetOutputPort())
image_mapper_3.SetOrientation(0)
image_mapper_3.SliceAtFocalPointOn()

image_slice_3 = vtkImageSlice()
image_slice_3.SetMapper(image_mapper_3)
image_slice_3.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_3.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_3.GetProperty().SetInterpolationTypeToNearest()

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(image_slice_3)
renderer_3.SetBackground(0.0, 0.0, 0.0)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(512, 512)
render_window.SetWindowName("image interpolate sliding window3d")

# Scene
bounds_0 = image_mapper_0.GetBounds()
point_0 = [0.5 * (bounds_0[0] + bounds_0[1]), 0.5 * (bounds_0[2] + bounds_0[3]), 0.5 * (bounds_0[4] + bounds_0[5])]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[image_mapper_0.GetOrientation()] += 500.0
camera_0.SetPosition(point_0)
camera_0.SetViewUp(0.0, 0.0, -1.0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(0.8 * 128)

bounds_1 = image_mapper_1.GetBounds()
point_1 = [0.5 * (bounds_1[0] + bounds_1[1]), 0.5 * (bounds_1[2] + bounds_1[3]), 0.5 * (bounds_1[4] + bounds_1[5])]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[image_mapper_1.GetOrientation()] += 500.0
camera_1.SetPosition(point_1)
camera_1.SetViewUp(0.0, 0.0, -1.0)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.8 * 128)

bounds_2 = image_mapper_2.GetBounds()
point_2 = [0.5 * (bounds_2[0] + bounds_2[1]), 0.5 * (bounds_2[2] + bounds_2[3]), 0.5 * (bounds_2[4] + bounds_2[5])]
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(point_2)
point_2[image_mapper_2.GetOrientation()] += 500.0
camera_2.SetPosition(point_2)
camera_2.SetViewUp(0.0, 1.0, 0.0)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(0.8 * 128)

bounds_3 = image_mapper_3.GetBounds()
point_3 = [0.5 * (bounds_3[0] + bounds_3[1]), 0.5 * (bounds_3[2] + bounds_3[3]), 0.5 * (bounds_3[4] + bounds_3[5])]
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(point_3)
point_3[image_mapper_3.GetOrientation()] += 500.0
camera_3.SetPosition(point_3)
camera_3.SetViewUp(0.0, 0.0, -1.0)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(0.8 * 128)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
