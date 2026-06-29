#!/usr/bin/env python

# Test off-axis views of 3D images with vtkImageResliceMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkImageProperty,
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
reader.Update()

# Viewport 0: parallel projection, no rotation, resample off
image_property_0 = vtkImageProperty()
image_property_0.SetColorWindow(2000)
image_property_0.SetColorLevel(1000)
image_property_0.SetAmbient(0.0)
image_property_0.SetDiffuse(1.0)
image_property_0.SetInterpolationTypeToLinear()

image_mapper_0_0 = vtkImageResliceMapper()
image_mapper_0_0.SetInputConnection(reader.GetOutputPort())
image_mapper_0_0.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)
image_mapper_0_0.SliceAtFocalPointOn()
image_mapper_0_0.BorderOn()
image_mapper_0_0.SetResampleToScreenPixels(0)

image_0_0 = vtkImageSlice()
image_0_0.SetProperty(image_property_0)
image_0_0.SetMapper(image_mapper_0_0)

outline_filter_0_0 = vtkOutlineFilter()
outline_filter_0_0.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_0 = vtkDataSetMapper()
outline_mapper_0_0.SetInputConnection(outline_filter_0_0.GetOutputPort())

outline_actor_0_0 = vtkActor()
outline_actor_0_0.SetMapper(outline_mapper_0_0)

image_mapper_0_1 = vtkImageResliceMapper()
image_mapper_0_1.SetInputConnection(reader.GetOutputPort())
image_mapper_0_1.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)
image_mapper_0_1.SliceAtFocalPointOn()
image_mapper_0_1.BorderOn()
image_mapper_0_1.SetResampleToScreenPixels(0)

image_0_1 = vtkImageSlice()
image_0_1.SetProperty(image_property_0)
image_0_1.SetMapper(image_mapper_0_1)

outline_filter_0_1 = vtkOutlineFilter()
outline_filter_0_1.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_1 = vtkDataSetMapper()
outline_mapper_0_1.SetInputConnection(outline_filter_0_1.GetOutputPort())

outline_actor_0_1 = vtkActor()
outline_actor_0_1.SetMapper(outline_mapper_0_1)

image_mapper_0_2 = vtkImageResliceMapper()
image_mapper_0_2.SetInputConnection(reader.GetOutputPort())
image_mapper_0_2.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)
image_mapper_0_2.SliceAtFocalPointOn()
image_mapper_0_2.BorderOn()
image_mapper_0_2.SetResampleToScreenPixels(0)

image_0_2 = vtkImageSlice()
image_0_2.SetProperty(image_property_0)
image_0_2.SetMapper(image_mapper_0_2)

outline_filter_0_2 = vtkOutlineFilter()
outline_filter_0_2.SetInputConnection(reader.GetOutputPort())

outline_mapper_0_2 = vtkDataSetMapper()
outline_mapper_0_2.SetInputConnection(outline_filter_0_2.GetOutputPort())

outline_actor_0_2 = vtkActor()
outline_actor_0_2.SetMapper(outline_mapper_0_2)

# Viewport 1: parallel projection, rotated, resample off
image_property_1 = vtkImageProperty()
image_property_1.SetColorWindow(2000)
image_property_1.SetColorLevel(1000)
image_property_1.SetAmbient(0.0)
image_property_1.SetDiffuse(1.0)
image_property_1.SetInterpolationTypeToLinear()

image_mapper_1_0 = vtkImageResliceMapper()
image_mapper_1_0.SetInputConnection(reader.GetOutputPort())
image_mapper_1_0.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)
image_mapper_1_0.SliceAtFocalPointOn()
image_mapper_1_0.BorderOn()
image_mapper_1_0.SetResampleToScreenPixels(0)

image_1_0 = vtkImageSlice()
image_1_0.SetProperty(image_property_1)
image_1_0.SetMapper(image_mapper_1_0)
image_1_0.RotateX(10)
image_1_0.RotateY(5)

outline_filter_1_0 = vtkOutlineFilter()
outline_filter_1_0.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_0 = vtkDataSetMapper()
outline_mapper_1_0.SetInputConnection(outline_filter_1_0.GetOutputPort())

outline_actor_1_0 = vtkActor()
outline_actor_1_0.SetMapper(outline_mapper_1_0)
outline_actor_1_0.RotateX(10)
outline_actor_1_0.RotateY(5)

image_mapper_1_1 = vtkImageResliceMapper()
image_mapper_1_1.SetInputConnection(reader.GetOutputPort())
image_mapper_1_1.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)
image_mapper_1_1.SliceAtFocalPointOn()
image_mapper_1_1.BorderOn()
image_mapper_1_1.SetResampleToScreenPixels(0)

image_1_1 = vtkImageSlice()
image_1_1.SetProperty(image_property_1)
image_1_1.SetMapper(image_mapper_1_1)
image_1_1.RotateX(10)
image_1_1.RotateY(5)

outline_filter_1_1 = vtkOutlineFilter()
outline_filter_1_1.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_1 = vtkDataSetMapper()
outline_mapper_1_1.SetInputConnection(outline_filter_1_1.GetOutputPort())

outline_actor_1_1 = vtkActor()
outline_actor_1_1.SetMapper(outline_mapper_1_1)
outline_actor_1_1.RotateX(10)
outline_actor_1_1.RotateY(5)

image_mapper_1_2 = vtkImageResliceMapper()
image_mapper_1_2.SetInputConnection(reader.GetOutputPort())
image_mapper_1_2.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)
image_mapper_1_2.SliceAtFocalPointOn()
image_mapper_1_2.BorderOn()
image_mapper_1_2.SetResampleToScreenPixels(0)

image_1_2 = vtkImageSlice()
image_1_2.SetProperty(image_property_1)
image_1_2.SetMapper(image_mapper_1_2)
image_1_2.RotateX(10)
image_1_2.RotateY(5)

outline_filter_1_2 = vtkOutlineFilter()
outline_filter_1_2.SetInputConnection(reader.GetOutputPort())

outline_mapper_1_2 = vtkDataSetMapper()
outline_mapper_1_2.SetInputConnection(outline_filter_1_2.GetOutputPort())

outline_actor_1_2 = vtkActor()
outline_actor_1_2.SetMapper(outline_mapper_1_2)
outline_actor_1_2.RotateX(10)
outline_actor_1_2.RotateY(5)

# Viewport 2: perspective, no rotation, resample on
image_property_2 = vtkImageProperty()
image_property_2.SetColorWindow(2000)
image_property_2.SetColorLevel(1000)
image_property_2.SetAmbient(0.0)
image_property_2.SetDiffuse(1.0)
image_property_2.SetInterpolationTypeToLinear()

image_mapper_2_0 = vtkImageResliceMapper()
image_mapper_2_0.SetInputConnection(reader.GetOutputPort())
image_mapper_2_0.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)
image_mapper_2_0.SliceAtFocalPointOn()
image_mapper_2_0.BorderOn()
image_mapper_2_0.SetResampleToScreenPixels(1)

image_2_0 = vtkImageSlice()
image_2_0.SetProperty(image_property_2)
image_2_0.SetMapper(image_mapper_2_0)

outline_filter_2_0 = vtkOutlineFilter()
outline_filter_2_0.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_0 = vtkDataSetMapper()
outline_mapper_2_0.SetInputConnection(outline_filter_2_0.GetOutputPort())

outline_actor_2_0 = vtkActor()
outline_actor_2_0.SetMapper(outline_mapper_2_0)

image_mapper_2_1 = vtkImageResliceMapper()
image_mapper_2_1.SetInputConnection(reader.GetOutputPort())
image_mapper_2_1.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)
image_mapper_2_1.SliceAtFocalPointOn()
image_mapper_2_1.BorderOn()
image_mapper_2_1.SetResampleToScreenPixels(1)

image_2_1 = vtkImageSlice()
image_2_1.SetProperty(image_property_2)
image_2_1.SetMapper(image_mapper_2_1)

outline_filter_2_1 = vtkOutlineFilter()
outline_filter_2_1.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_1 = vtkDataSetMapper()
outline_mapper_2_1.SetInputConnection(outline_filter_2_1.GetOutputPort())

outline_actor_2_1 = vtkActor()
outline_actor_2_1.SetMapper(outline_mapper_2_1)

image_mapper_2_2 = vtkImageResliceMapper()
image_mapper_2_2.SetInputConnection(reader.GetOutputPort())
image_mapper_2_2.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)
image_mapper_2_2.SliceAtFocalPointOn()
image_mapper_2_2.BorderOn()
image_mapper_2_2.SetResampleToScreenPixels(1)

image_2_2 = vtkImageSlice()
image_2_2.SetProperty(image_property_2)
image_2_2.SetMapper(image_mapper_2_2)

outline_filter_2_2 = vtkOutlineFilter()
outline_filter_2_2.SetInputConnection(reader.GetOutputPort())

outline_mapper_2_2 = vtkDataSetMapper()
outline_mapper_2_2.SetInputConnection(outline_filter_2_2.GetOutputPort())

outline_actor_2_2 = vtkActor()
outline_actor_2_2.SetMapper(outline_mapper_2_2)

# Viewport 3: perspective, rotated, resample on
image_property_3 = vtkImageProperty()
image_property_3.SetColorWindow(2000)
image_property_3.SetColorLevel(1000)
image_property_3.SetAmbient(0.0)
image_property_3.SetDiffuse(1.0)
image_property_3.SetInterpolationTypeToLinear()

image_mapper_3_0 = vtkImageResliceMapper()
image_mapper_3_0.SetInputConnection(reader.GetOutputPort())
image_mapper_3_0.GetSlicePlane().SetNormal(1.0, 0.0, 0.0)
image_mapper_3_0.SliceAtFocalPointOn()
image_mapper_3_0.BorderOn()
image_mapper_3_0.SetResampleToScreenPixels(1)

image_3_0 = vtkImageSlice()
image_3_0.SetProperty(image_property_3)
image_3_0.SetMapper(image_mapper_3_0)
image_3_0.RotateX(10)
image_3_0.RotateY(5)

outline_filter_3_0 = vtkOutlineFilter()
outline_filter_3_0.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_0 = vtkDataSetMapper()
outline_mapper_3_0.SetInputConnection(outline_filter_3_0.GetOutputPort())

outline_actor_3_0 = vtkActor()
outline_actor_3_0.SetMapper(outline_mapper_3_0)
outline_actor_3_0.RotateX(10)
outline_actor_3_0.RotateY(5)

image_mapper_3_1 = vtkImageResliceMapper()
image_mapper_3_1.SetInputConnection(reader.GetOutputPort())
image_mapper_3_1.GetSlicePlane().SetNormal(0.0, 1.0, 0.0)
image_mapper_3_1.SliceAtFocalPointOn()
image_mapper_3_1.BorderOn()
image_mapper_3_1.SetResampleToScreenPixels(1)

image_3_1 = vtkImageSlice()
image_3_1.SetProperty(image_property_3)
image_3_1.SetMapper(image_mapper_3_1)
image_3_1.RotateX(10)
image_3_1.RotateY(5)

outline_filter_3_1 = vtkOutlineFilter()
outline_filter_3_1.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_1 = vtkDataSetMapper()
outline_mapper_3_1.SetInputConnection(outline_filter_3_1.GetOutputPort())

outline_actor_3_1 = vtkActor()
outline_actor_3_1.SetMapper(outline_mapper_3_1)
outline_actor_3_1.RotateX(10)
outline_actor_3_1.RotateY(5)

image_mapper_3_2 = vtkImageResliceMapper()
image_mapper_3_2.SetInputConnection(reader.GetOutputPort())
image_mapper_3_2.GetSlicePlane().SetNormal(0.0, 0.0, 1.0)
image_mapper_3_2.SliceAtFocalPointOn()
image_mapper_3_2.BorderOn()
image_mapper_3_2.SetResampleToScreenPixels(1)

image_3_2 = vtkImageSlice()
image_3_2.SetProperty(image_property_3)
image_3_2.SetMapper(image_mapper_3_2)
image_3_2.RotateX(10)
image_3_2.RotateY(5)

outline_filter_3_2 = vtkOutlineFilter()
outline_filter_3_2.SetInputConnection(reader.GetOutputPort())

outline_mapper_3_2 = vtkDataSetMapper()
outline_mapper_3_2.SetInputConnection(outline_filter_3_2.GetOutputPort())

outline_actor_3_2 = vtkActor()
outline_actor_3_2.SetMapper(outline_mapper_3_2)
outline_actor_3_2.RotateX(10)
outline_actor_3_2.RotateY(5)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_0.AddViewProp(image_0_0)
renderer_0.AddViewProp(outline_actor_0_0)
renderer_0.AddViewProp(image_0_1)
renderer_0.AddViewProp(outline_actor_0_1)
renderer_0.AddViewProp(image_0_2)
renderer_0.AddViewProp(outline_actor_0_2)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_1.AddViewProp(image_1_0)
renderer_1.AddViewProp(outline_actor_1_0)
renderer_1.AddViewProp(image_1_1)
renderer_1.AddViewProp(outline_actor_1_1)
renderer_1.AddViewProp(image_1_2)
renderer_1.AddViewProp(outline_actor_1_2)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.AddViewProp(image_2_0)
renderer_2.AddViewProp(outline_actor_2_0)
renderer_2.AddViewProp(image_2_1)
renderer_2.AddViewProp(outline_actor_2_1)
renderer_2.AddViewProp(image_2_2)
renderer_2.AddViewProp(outline_actor_2_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddViewProp(image_3_0)
renderer_3.AddViewProp(outline_actor_3_0)
renderer_3.AddViewProp(image_3_1)
renderer_3.AddViewProp(outline_actor_3_1)
renderer_3.AddViewProp(image_3_2)
renderer_3.AddViewProp(outline_actor_3_2)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("reslice mapper off axis")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.Azimuth(10)
camera_0.Elevation(-120)
renderer_0.ResetCamera()
camera_0.Dolly(1.2)
camera_0.SetParallelScale(125)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.Azimuth(10)
camera_1.Elevation(-120)
renderer_1.ResetCamera()
camera_1.Dolly(1.2)
camera_1.SetParallelScale(125)

camera_2 = renderer_2.GetActiveCamera()
camera_2.Azimuth(10)
camera_2.Elevation(-120)
renderer_2.ResetCamera()
camera_2.Dolly(1.2)
camera_2.SetParallelScale(125)

camera_3 = renderer_3.GetActiveCamera()
camera_3.Azimuth(10)
camera_3.Elevation(-120)
renderer_3.ResetCamera()
camera_3.Dolly(1.2)
camera_3.SetParallelScale(125)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
