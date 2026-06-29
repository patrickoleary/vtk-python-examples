#!/usr/bin/env python

# Test vtkImageHistogramStatistics auto range vs full range on a medical image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingStatistics import vtkImageHistogramStatistics
from vtkmodules.vtkRenderingCore import (
    vtkImageSliceMapper,
    vtkImageSlice,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read image
reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Compute histogram statistics
statistics = vtkImageHistogramStatistics()
statistics.SetInputConnection(reader.GetOutputPort())
statistics.GenerateHistogramImageOff()
statistics.Update()

# Full data range
data_range = [statistics.GetMinimum(), statistics.GetMaximum()]

# Auto range
auto_range = list(statistics.GetAutoRange())

# Viewport 0: full range
image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())

image_slice_0 = vtkImageSlice()
image_slice_0.SetMapper(image_mapper_0)
image_slice_0.GetProperty().SetColorWindow(data_range[1] - data_range[0])
image_slice_0.GetProperty().SetColorLevel(0.5 * (data_range[0] + data_range[1]))

renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.0, 0.0, 0.0)
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddViewProp(image_slice_0)

# Viewport 1: auto range
image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())

image_slice_1 = vtkImageSlice()
image_slice_1.SetMapper(image_mapper_1)
image_slice_1.GetProperty().SetColorWindow(auto_range[1] - auto_range[0])
image_slice_1.GetProperty().SetColorLevel(0.5 * (auto_range[0] + auto_range[1]))

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.0, 0.0, 0.0)
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.AddViewProp(image_slice_1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(512, 256)
render_window.SetWindowName("image auto range")

# Scene
bounds_0 = image_mapper_0.GetBounds()
point_0 = [
    0.5 * (bounds_0[0] + bounds_0[1]),
    0.5 * (bounds_0[2] + bounds_0[3]),
    0.5 * (bounds_0[4] + bounds_0[5]),
]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[image_mapper_0.GetOrientation()] += 500.0
camera_0.SetPosition(point_0)
camera_0.SetViewUp(0.0, 1.0, 0.0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(128)

bounds_1 = image_mapper_1.GetBounds()
point_1 = [
    0.5 * (bounds_1[0] + bounds_1[1]),
    0.5 * (bounds_1[2] + bounds_1[3]),
    0.5 * (bounds_1[4] + bounds_1[5]),
]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[image_mapper_1.GetOrientation()] += 500.0
camera_1.SetPosition(point_1)
camera_1.SetViewUp(0.0, 1.0, 0.0)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(128)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
