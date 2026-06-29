#!/usr/bin/env python

# Test vtkImageReslice with oriented image input and multiple output directions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonMath import vtkMatrix3x3
from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingCore import vtkImageReslice
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

# Reorient input to a non-identity direction
direction = [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0]

orient = vtkImageReslice()
orient.SetInputConnection(reader.GetOutputPort())
orient.SetOutputDirection(direction)
orient.Update()

color_range = [0.0, 4095.0]

# Direction matrices for four viewports
directions = [
    # lower left: sagittal
    [1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, -1.0, 0.0],
    # lower right: oblique
    [0.3610509009504489, 0.5641239080948949, 0.7425674805959468,
     -0.8708194756386795, 0.48884072076035906, 0.05204027838960906,
     -0.333640057204234, -0.6654314134771782, 0.6677464684942334],
    # upper left: axial
    [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0],
    # upper right: coronal (with flip)
    [0.0, 0.0, 1.0, 1.0, 0.0, 0.0, 0.0, -1.0, 0.0],
]

# Viewport 0 (lower-left): sagittal
reslice_0 = vtkImageReslice()
reslice_0.SetInputConnection(orient.GetOutputPort())
reslice_0.SetOutputSpacing(1.0, 1.0, 1.0)
reslice_0.SetOutputDirection(directions[0])
reslice_0.SetInterpolationModeToLinear()

image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reslice_0.GetOutputPort())
image_mapper_0.SliceAtFocalPointOn()
image_mapper_0.BorderOn()

image_slice_0 = vtkImageSlice()
image_slice_0.SetMapper(image_mapper_0)
image_slice_0.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_0.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_0.GetProperty().SetInterpolationTypeToNearest()

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(image_slice_0)
renderer_0.SetBackground(0.2, 0.2, 0.2)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# Viewport 1 (lower-right): oblique
reslice_1 = vtkImageReslice()
reslice_1.SetInputConnection(orient.GetOutputPort())
reslice_1.SetOutputSpacing(1.0, 1.0, 1.0)
reslice_1.SetOutputDirection(directions[1])
reslice_1.SetInterpolationModeToLinear()

image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reslice_1.GetOutputPort())
image_mapper_1.SliceAtFocalPointOn()
image_mapper_1.BorderOn()

image_slice_1 = vtkImageSlice()
image_slice_1.SetMapper(image_mapper_1)
image_slice_1.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_1.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_1.GetProperty().SetInterpolationTypeToNearest()

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(image_slice_1)
renderer_1.SetBackground(0.2, 0.2, 0.2)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# Viewport 2 (upper-left): axial
reslice_2 = vtkImageReslice()
reslice_2.SetInputConnection(orient.GetOutputPort())
reslice_2.SetOutputSpacing(1.0, 1.0, 1.0)
reslice_2.SetOutputDirection(directions[2])
reslice_2.SetInterpolationModeToLinear()

image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(reslice_2.GetOutputPort())
image_mapper_2.SliceAtFocalPointOn()
image_mapper_2.BorderOn()

image_slice_2 = vtkImageSlice()
image_slice_2.SetMapper(image_mapper_2)
image_slice_2.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_2.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_2.GetProperty().SetInterpolationTypeToNearest()

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(image_slice_2)
renderer_2.SetBackground(0.2, 0.2, 0.2)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# Viewport 3 (upper-right): coronal with flip
reslice_3 = vtkImageReslice()
reslice_3.SetInputConnection(orient.GetOutputPort())
reslice_3.SetOutputSpacing(1.0, 1.0, 1.0)
reslice_3.SetOutputDirection(directions[3])
reslice_3.SetInterpolationModeToLinear()

image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(reslice_3.GetOutputPort())
image_mapper_3.SliceAtFocalPointOn()
image_mapper_3.BorderOn()

image_slice_3 = vtkImageSlice()
image_slice_3.SetMapper(image_mapper_3)
image_slice_3.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_3.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice_3.GetProperty().SetInterpolationTypeToNearest()

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(image_slice_3)
renderer_3.SetBackground(0.2, 0.2, 0.2)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(512, 512)
render_window.SetWindowName("image reslice oriented")

# Scene
bounds_0 = image_mapper_0.GetBounds()
focal_0 = [0.5 * (bounds_0[0] + bounds_0[1]), 0.5 * (bounds_0[2] + bounds_0[3]), 0.5 * (bounds_0[4] + bounds_0[5])]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(focal_0)
offset_0 = [0.0, 0.0, 500.0]
vtkMatrix3x3.MultiplyPoint(directions[0], offset_0, offset_0)
vtkMath.Add(focal_0, offset_0, focal_0)
camera_0.SetPosition(focal_0)
viewup_0 = [0.0, 1.0, 0.0]
vtkMatrix3x3.MultiplyPoint(directions[0], viewup_0, viewup_0)
camera_0.SetViewUp(viewup_0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(128)

bounds_1 = image_mapper_1.GetBounds()
focal_1 = [0.5 * (bounds_1[0] + bounds_1[1]), 0.5 * (bounds_1[2] + bounds_1[3]), 0.5 * (bounds_1[4] + bounds_1[5])]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(focal_1)
offset_1 = [0.0, 0.0, 500.0]
vtkMatrix3x3.MultiplyPoint(directions[1], offset_1, offset_1)
vtkMath.Add(focal_1, offset_1, focal_1)
camera_1.SetPosition(focal_1)
viewup_1 = [0.0, 1.0, 0.0]
vtkMatrix3x3.MultiplyPoint(directions[1], viewup_1, viewup_1)
camera_1.SetViewUp(viewup_1)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(128)

bounds_2 = image_mapper_2.GetBounds()
focal_2 = [0.5 * (bounds_2[0] + bounds_2[1]), 0.5 * (bounds_2[2] + bounds_2[3]), 0.5 * (bounds_2[4] + bounds_2[5])]
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(focal_2)
offset_2 = [0.0, 0.0, 500.0]
vtkMatrix3x3.MultiplyPoint(directions[2], offset_2, offset_2)
vtkMath.Add(focal_2, offset_2, focal_2)
camera_2.SetPosition(focal_2)
viewup_2 = [0.0, 1.0, 0.0]
vtkMatrix3x3.MultiplyPoint(directions[2], viewup_2, viewup_2)
camera_2.SetViewUp(viewup_2)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(128)

bounds_3 = image_mapper_3.GetBounds()
focal_3 = [0.5 * (bounds_3[0] + bounds_3[1]), 0.5 * (bounds_3[2] + bounds_3[3]), 0.5 * (bounds_3[4] + bounds_3[5])]
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(focal_3)
offset_3 = [0.0, 0.0, 500.0]
vtkMatrix3x3.MultiplyPoint(directions[3], offset_3, offset_3)
vtkMath.Add(focal_3, offset_3, focal_3)
camera_3.SetPosition(focal_3)
viewup_3 = [0.0, 1.0, 0.0]
vtkMatrix3x3.MultiplyPoint(directions[3], viewup_3, viewup_3)
camera_3.SetViewUp(viewup_3)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(128)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
