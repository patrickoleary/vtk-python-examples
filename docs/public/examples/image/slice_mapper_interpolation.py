#!/usr/bin/env python

# Test nearest, linear, and cubic interpolation with vtkImageSliceMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read image
reader = vtkPNGReader()
reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Viewport 0: nearest interpolation
image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())

image_0 = vtkImageSlice()
image_0.SetMapper(image_mapper_0)
image_0.GetProperty().SetColorWindow(1000)
image_0.GetProperty().SetColorLevel(1500)
image_0.GetProperty().SetInterpolationType(0)

# Viewport 1: linear interpolation
image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())

image_1 = vtkImageSlice()
image_1.SetMapper(image_mapper_1)
image_1.GetProperty().SetColorWindow(1000)
image_1.GetProperty().SetColorLevel(1500)
image_1.GetProperty().SetInterpolationType(1)

# Viewport 2: cubic interpolation
image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(reader.GetOutputPort())

image_2 = vtkImageSlice()
image_2.SetMapper(image_mapper_2)
image_2.GetProperty().SetColorWindow(1000)
image_2.GetProperty().SetColorLevel(1500)
image_2.GetProperty().SetInterpolationType(2)

# Viewport 3: lookup table
lookup_table = vtkLookupTable()
lookup_table.Build()
lookup_table.SetRange(1000, 2000)

image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(reader.GetOutputPort())

image_3 = vtkImageSlice()
image_3.SetMapper(image_mapper_3)
image_3.GetProperty().SetLookupTable(lookup_table)
image_3.GetProperty().UseLookupTableScalarRangeOn()

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
render_window.SetWindowName("slice mapper interpolation")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
renderer_0.ResetCamera()
camera_0.SetParallelScale(10.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
renderer_1.ResetCamera()
camera_1.SetParallelScale(10.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
renderer_2.ResetCamera()
camera_2.SetParallelScale(10.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
renderer_3.ResetCamera()
camera_3.SetParallelScale(10.0)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
