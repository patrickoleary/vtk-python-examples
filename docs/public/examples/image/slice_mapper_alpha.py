#!/usr/bin/env python

# Test alpha blending with vtkImageSliceMapper: RGBA, LA, Opacity, lookup table.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read images
reader = vtkPNGReader()
reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

reader_2 = vtkPNGReader()
reader_2.SetFileName(os.path.join(data_dir, "alphachannel.png"))

# Grayscale lookup table
table = vtkLookupTable()
table.SetRampToLinear()
table.SetRange(0.0, 255.0)
table.SetValueRange(0.0, 1.0)
table.SetSaturationRange(0.0, 0.0)
table.SetVectorModeToRGBColors()
table.Build()

# Green lookup table with alpha from component 3
table_2 = vtkLookupTable()
table_2.SetRampToLinear()
table_2.SetRange(0, 255)
table_2.SetHueRange(0.3, 0.3)
table_2.SetValueRange(0.0, 1.0)
table_2.SetSaturationRange(1.0, 1.0)
table_2.SetAlphaRange(0.0, 1.0)
table_2.SetVectorModeToComponent()
table_2.SetVectorComponent(3)
table_2.Build()

# Map to LA
colors = vtkImageMapToColors()
colors.SetInputConnection(reader_2.GetOutputPort())
colors.SetLookupTable(table)
colors.PassAlphaToOutputOn()
colors.SetOutputFormatToLuminanceAlpha()

# Map to RGB
colors_2 = vtkImageMapToColors()
colors_2.SetInputConnection(reader_2.GetOutputPort())
colors_2.SetLookupTable(table)
colors_2.SetOutputFormatToRGB()

# Viewport 0: base image + RGBA overlay
base_mapper_0 = vtkImageSliceMapper()
base_mapper_0.SetInputConnection(reader.GetOutputPort())

base_image_0 = vtkImageSlice()
base_image_0.SetMapper(base_mapper_0)
base_image_0.GetProperty().SetColorWindow(2000.0)
base_image_0.GetProperty().SetColorLevel(1000.0)

overlay_mapper_0 = vtkImageSliceMapper()
overlay_mapper_0.SetInputConnection(reader_2.GetOutputPort())

overlay_image_0 = vtkImageSlice()
overlay_image_0.SetMapper(overlay_mapper_0)

# Viewport 1: base image + LA overlay
base_mapper_1 = vtkImageSliceMapper()
base_mapper_1.SetInputConnection(reader.GetOutputPort())

base_image_1 = vtkImageSlice()
base_image_1.SetMapper(base_mapper_1)
base_image_1.GetProperty().SetColorWindow(2000.0)
base_image_1.GetProperty().SetColorLevel(1000.0)

overlay_mapper_1 = vtkImageSliceMapper()
overlay_mapper_1.SetInputConnection(colors.GetOutputPort())

overlay_image_1 = vtkImageSlice()
overlay_image_1.SetMapper(overlay_mapper_1)

# Viewport 2: base image + RGB overlay with opacity 0.5
base_mapper_2 = vtkImageSliceMapper()
base_mapper_2.SetInputConnection(reader.GetOutputPort())

base_image_2 = vtkImageSlice()
base_image_2.SetMapper(base_mapper_2)
base_image_2.GetProperty().SetColorWindow(2000.0)
base_image_2.GetProperty().SetColorLevel(1000.0)

overlay_mapper_2 = vtkImageSliceMapper()
overlay_mapper_2.SetInputConnection(colors_2.GetOutputPort())

overlay_image_2 = vtkImageSlice()
overlay_image_2.SetMapper(overlay_mapper_2)
overlay_image_2.GetProperty().SetOpacity(0.5)

# Viewport 3: base image + RGBA overlay with green lookup table
base_mapper_3 = vtkImageSliceMapper()
base_mapper_3.SetInputConnection(reader.GetOutputPort())

base_image_3 = vtkImageSlice()
base_image_3.SetMapper(base_mapper_3)
base_image_3.GetProperty().SetColorWindow(2000.0)
base_image_3.GetProperty().SetColorLevel(1000.0)

overlay_mapper_3 = vtkImageSliceMapper()
overlay_mapper_3.SetInputConnection(reader_2.GetOutputPort())

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
render_window.SetWindowName("slice mapper alpha")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
renderer_0.ResetCamera()
camera_0.SetParallelScale(200.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
renderer_1.ResetCamera()
camera_1.SetParallelScale(200.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
renderer_2.ResetCamera()
camera_2.SetParallelScale(200.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
renderer_3.ResetCamera()
camera_3.SetParallelScale(200.0)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
