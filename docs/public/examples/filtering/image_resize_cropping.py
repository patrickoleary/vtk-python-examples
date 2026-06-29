#!/usr/bin/env python

# Test vtkImageResize cropping with border on/off in four viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkOutlineSource
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkImagingCore import vtkImageResize
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read image
reader = vtkTIFFReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "beach.tif"))
reader.SetOrientationType(4)

color_range = [0, 255]
cropping = [
    [0, 199, 0, 199, 0, 0],
    [10, 149, 50, 199, 0, 0],
    [-0.5, 199.5, -0.5, 199.5, 0, 0],
    [9.5, 149.5, 199.5, 49.5, 0, 0],
]

# Outline showing crop region
outline = vtkOutlineSource()
outline.SetBounds(10, 149, 50, 199, -1, 1)

outline_mapper = vtkDataSetMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Viewport 0 (lower-left): no crop, no border
resize_0 = vtkImageResize()
resize_0.SetNumberOfThreads(1)
resize_0.SetInputConnection(reader.GetOutputPort())
resize_0.SetOutputDimensions(256, 256, 1)

image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(resize_0.GetOutputPort())

image_slice_0 = vtkImageSlice()
image_slice_0.SetMapper(image_mapper_0)
image_slice_0.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_0.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(image_slice_0)
renderer_0.AddViewProp(outline_actor)
renderer_0.SetBackground(0.0, 0.0, 0.0)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)

# Viewport 1 (lower-right): crop, no border
resize_1 = vtkImageResize()
resize_1.SetNumberOfThreads(1)
resize_1.SetInputConnection(reader.GetOutputPort())
resize_1.SetOutputDimensions(256, 256, 1)
resize_1.CroppingOn()
resize_1.SetCroppingRegion(cropping[1])

image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(resize_1.GetOutputPort())

image_slice_1 = vtkImageSlice()
image_slice_1.SetMapper(image_mapper_1)
image_slice_1.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_1.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(image_slice_1)
renderer_1.SetBackground(0.0, 0.0, 0.0)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)

# Viewport 2 (upper-left): no crop, border on
resize_2 = vtkImageResize()
resize_2.SetNumberOfThreads(1)
resize_2.SetInputConnection(reader.GetOutputPort())
resize_2.SetOutputDimensions(256, 256, 1)
resize_2.BorderOn()

image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(resize_2.GetOutputPort())
image_mapper_2.BorderOn()

image_slice_2 = vtkImageSlice()
image_slice_2.SetMapper(image_mapper_2)
image_slice_2.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_2.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(image_slice_2)
renderer_2.SetBackground(0.0, 0.0, 0.0)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)

# Viewport 3 (upper-right): crop, border on
resize_3 = vtkImageResize()
resize_3.SetNumberOfThreads(1)
resize_3.SetInputConnection(reader.GetOutputPort())
resize_3.SetOutputDimensions(256, 256, 1)
resize_3.CroppingOn()
resize_3.SetCroppingRegion(cropping[3])
resize_3.BorderOn()

image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(resize_3.GetOutputPort())
image_mapper_3.BorderOn()

image_slice_3 = vtkImageSlice()
image_slice_3.SetMapper(image_mapper_3)
image_slice_3.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice_3.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))

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
render_window.SetMultiSamples(0)
render_window.SetWindowName("image resize cropping")

# Scene
point_0 = [99.5, 99.5, 0.0]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[2] += 500.0
camera_0.SetPosition(point_0)
camera_0.SetViewUp(0.0, 1.0, 0.0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(100)

point_1 = [99.5, 99.5, 0.0]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[2] += 500.0
camera_1.SetPosition(point_1)
camera_1.SetViewUp(0.0, 1.0, 0.0)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(100)

point_2 = [99.5, 99.5, 0.0]
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(point_2)
point_2[2] += 500.0
camera_2.SetPosition(point_2)
camera_2.SetViewUp(0.0, 1.0, 0.0)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(100)

point_3 = [99.5, 99.5, 0.0]
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(point_3)
point_3[2] += 500.0
camera_3.SetPosition(point_3)
camera_3.SetViewUp(0.0, 1.0, 0.0)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(100)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
