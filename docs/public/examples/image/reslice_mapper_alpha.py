#!/usr/bin/env python

# Test alpha blending with vtkImageResliceMapper: RGBA, LA, Opacity, lookup table.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingSources import vtkImageGridSource
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
reader.SetDataOrigin(2.5, -13.6, 2.8)
reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Grid source for overlay
grid = vtkImageGridSource()
grid.SetDataExtent(0, 60, 0, 60, 1, 93)
grid.SetDataSpacing(3.2, 3.2, 1.5)
grid.SetDataOrigin(0, 0, 0)
grid.SetDataScalarTypeToUnsignedChar()
grid.SetLineValue(255)

# Lookup table: grayscale with alpha ramp
table = vtkLookupTable()
table.SetRampToLinear()
table.SetRange(0.0, 255.0)
table.SetValueRange(1.0, 1.0)
table.SetSaturationRange(0.0, 0.0)
table.SetAlphaRange(0.0, 1.0)
table.Build()

# Lookup table 2: green with alpha ramp
table_2 = vtkLookupTable()
table_2.SetRampToLinear()
table_2.SetRange(0.0, 255.0)
table_2.SetValueRange(1.0, 1.0)
table_2.SetHueRange(0.2, 0.4)
table_2.SetSaturationRange(1.0, 1.0)
table_2.SetAlphaRange(0.5, 1.0)
table_2.Build()

# Map grid to LA
colors = vtkImageMapToColors()
colors.SetInputConnection(grid.GetOutputPort())
colors.SetLookupTable(table)
colors.PassAlphaToOutputOn()
colors.SetOutputFormatToLuminanceAlpha()

# Map grid to RGB
colors_2 = vtkImageMapToColors()
colors_2.SetInputConnection(grid.GetOutputPort())
colors_2.SetLookupTable(table_2)
colors_2.SetOutputFormatToRGB()

# Viewport 0: base image + grid overlay with opacity 0.5
base_mapper_0 = vtkImageResliceMapper()
base_mapper_0.SetInputConnection(reader.GetOutputPort())
base_mapper_0.SliceFacesCameraOn()
base_mapper_0.SliceAtFocalPointOn()

base_image_0 = vtkImageSlice()
base_image_0.SetMapper(base_mapper_0)
base_image_0.GetProperty().SetColorWindow(2000.0)
base_image_0.GetProperty().SetColorLevel(1000.0)

overlay_mapper_0 = vtkImageResliceMapper()
overlay_mapper_0.SetInputConnection(grid.GetOutputPort())
overlay_mapper_0.SliceFacesCameraOn()
overlay_mapper_0.SliceAtFocalPointOn()

overlay_image_0 = vtkImageSlice()
overlay_image_0.SetMapper(overlay_mapper_0)
overlay_image_0.GetProperty().SetOpacity(0.5)

# Viewport 1: base image + LA overlay with elevation
base_mapper_1 = vtkImageResliceMapper()
base_mapper_1.SetInputConnection(reader.GetOutputPort())
base_mapper_1.SliceFacesCameraOn()
base_mapper_1.SliceAtFocalPointOn()

base_image_1 = vtkImageSlice()
base_image_1.SetMapper(base_mapper_1)
base_image_1.GetProperty().SetColorWindow(2000.0)
base_image_1.GetProperty().SetColorLevel(1000.0)

overlay_mapper_1 = vtkImageResliceMapper()
overlay_mapper_1.SetInputConnection(colors.GetOutputPort())
overlay_mapper_1.SliceFacesCameraOn()
overlay_mapper_1.SliceAtFocalPointOn()

overlay_image_1 = vtkImageSlice()
overlay_image_1.SetMapper(overlay_mapper_1)

# Viewport 2: base image + RGB overlay with opacity 0.5
base_mapper_2 = vtkImageResliceMapper()
base_mapper_2.SetInputConnection(reader.GetOutputPort())
base_mapper_2.SliceFacesCameraOn()
base_mapper_2.SliceAtFocalPointOn()

base_image_2 = vtkImageSlice()
base_image_2.SetMapper(base_mapper_2)
base_image_2.GetProperty().SetColorWindow(2000.0)
base_image_2.GetProperty().SetColorLevel(1000.0)

overlay_mapper_2 = vtkImageResliceMapper()
overlay_mapper_2.SetInputConnection(colors_2.GetOutputPort())
overlay_mapper_2.SliceFacesCameraOn()
overlay_mapper_2.SliceAtFocalPointOn()

overlay_image_2 = vtkImageSlice()
overlay_image_2.SetMapper(overlay_mapper_2)
overlay_image_2.GetProperty().SetOpacity(0.5)

# Viewport 3: rotated base image + grid overlay with lookup table
base_mapper_3 = vtkImageResliceMapper()
base_mapper_3.SetInputConnection(reader.GetOutputPort())
base_mapper_3.SliceFacesCameraOn()
base_mapper_3.SliceAtFocalPointOn()

base_image_3 = vtkImageSlice()
base_image_3.SetMapper(base_mapper_3)
base_image_3.GetProperty().SetColorWindow(2000.0)
base_image_3.GetProperty().SetColorLevel(1000.0)
base_image_3.RotateWXYZ(30, 1, 0.5, 0)

overlay_mapper_3 = vtkImageResliceMapper()
overlay_mapper_3.SetInputConnection(grid.GetOutputPort())
overlay_mapper_3.SliceFacesCameraOn()
overlay_mapper_3.SliceAtFocalPointOn()

overlay_image_3 = vtkImageSlice()
overlay_image_3.SetMapper(overlay_mapper_3)
overlay_image_3.GetProperty().SetLookupTable(table_2)
overlay_image_3.GetProperty().SetOpacity(0.9)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_0.AddViewProp(base_image_0)
renderer_0.AddViewProp(overlay_image_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_1.AddViewProp(base_image_1)
renderer_1.AddViewProp(overlay_image_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.AddViewProp(base_image_2)
renderer_2.AddViewProp(overlay_image_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddViewProp(base_image_3)
renderer_3.AddViewProp(overlay_image_3)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("reslice mapper alpha")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
renderer_0.ResetCamera()
camera_0.SetParallelScale(110.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.Elevation(30)
camera_1.ParallelProjectionOn()
renderer_1.ResetCamera()
camera_1.SetParallelScale(110.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
renderer_2.ResetCamera()
camera_2.SetParallelScale(110.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
renderer_3.ResetCamera()
camera_3.SetParallelScale(110.0)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
