#!/usr/bin/env python

# Test slab modes (min, max, mean, sum) of vtkImageResliceMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

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

# Read headsq data
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
reader.SetDataOrigin(-100.8, -100.9, -69.0)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Viewport 0: slab min, oblique view
image_mapper_0 = vtkImageResliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())
image_mapper_0.SetSlabThickness(20)
image_mapper_0.SliceFacesCameraOn()
image_mapper_0.SetSlabTypeToMin()

image_0 = vtkImageSlice()
image_0.SetMapper(image_mapper_0)
image_0.GetProperty().SetInterpolationTypeToLinear()
image_0.GetProperty().SetColorWindow(2000)
image_0.GetProperty().SetColorLevel(1000)

# Viewport 1: slab max, oblique view
image_mapper_1 = vtkImageResliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())
image_mapper_1.SetSlabThickness(20)
image_mapper_1.SliceFacesCameraOn()
image_mapper_1.SetSlabTypeToMax()

image_1 = vtkImageSlice()
image_1.SetMapper(image_mapper_1)
image_1.GetProperty().SetInterpolationTypeToLinear()
image_1.GetProperty().SetColorWindow(2000)
image_1.GetProperty().SetColorLevel(1000)

# Viewport 2: slab mean, front view
image_mapper_2 = vtkImageResliceMapper()
image_mapper_2.SetInputConnection(reader.GetOutputPort())
image_mapper_2.SetSlabThickness(20)
image_mapper_2.SliceFacesCameraOn()
image_mapper_2.SetSlabTypeToMean()

image_2 = vtkImageSlice()
image_2.SetMapper(image_mapper_2)
image_2.GetProperty().SetInterpolationTypeToLinear()
image_2.GetProperty().SetColorWindow(2000)
image_2.GetProperty().SetColorLevel(1000)

# Viewport 3: slab sum, thick slab, rotated view
image_mapper_3 = vtkImageResliceMapper()
image_mapper_3.SetInputConnection(reader.GetOutputPort())
image_mapper_3.SetSlabThickness(100)
image_mapper_3.SliceFacesCameraOn()
image_mapper_3.ResampleToScreenPixelsOff()
image_mapper_3.SetSlabTypeToSum()

image_3 = vtkImageSlice()
image_3.SetMapper(image_mapper_3)
image_3.GetProperty().SetInterpolationTypeToLinear()
image_3.GetProperty().SetColorWindow(2000 * 100)
image_3.GetProperty().SetColorLevel(1000 * 100)

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
render_window.SetWindowName("reslice mapper slab")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.Azimuth(90)
camera_0.Roll(85)
camera_0.Azimuth(40)
camera_0.Elevation(30)
camera_0.ParallelProjectionOn()
renderer_0.ResetCamera()
camera_0.SetParallelScale(120.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.Azimuth(90)
camera_1.Roll(85)
camera_1.Azimuth(40)
camera_1.Elevation(30)
camera_1.ParallelProjectionOn()
renderer_1.ResetCamera()
camera_1.SetParallelScale(120.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
renderer_2.ResetCamera()
camera_2.SetParallelScale(120.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.Azimuth(91)
camera_3.Roll(90)
camera_3.ParallelProjectionOn()
renderer_3.ResetCamera()
camera_3.SetParallelScale(120.0)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
