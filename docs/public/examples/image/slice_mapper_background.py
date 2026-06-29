#!/usr/bin/env python

# Test the Background variable on vtkImageSliceMapper with beach.tif.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read beach image
reader = vtkTIFFReader()
reader.SetFileName(os.path.join(data_dir, "beach.tif"))

# Viewport 0: no border, no background
image_mapper_0 = vtkImageSliceMapper()
image_mapper_0.SetInputConnection(reader.GetOutputPort())
image_mapper_0.CroppingOn()
image_mapper_0.SetCroppingRegion(100, 107, 100, 107, 0, 0)

clipping_plane_0 = vtkPlane()
clipping_plane_0.SetNormal(-0.5, 0.5, 0)
clipping_plane_0.SetOrigin(105, 105, 0)
image_mapper_0.AddClippingPlane(clipping_plane_0)

image_0 = vtkImageSlice()
image_0.SetMapper(image_mapper_0)
image_0.GetProperty().SetColorWindow(255.0)
image_0.GetProperty().SetColorLevel(127.5)

# Viewport 1: border on, no background
image_mapper_1 = vtkImageSliceMapper()
image_mapper_1.SetInputConnection(reader.GetOutputPort())
image_mapper_1.CroppingOn()
image_mapper_1.SetCroppingRegion(100, 107, 100, 107, 0, 0)
image_mapper_1.BorderOn()

clipping_plane_1 = vtkPlane()
clipping_plane_1.SetNormal(-0.5, 0.5, 0)
clipping_plane_1.SetOrigin(105, 105, 0)
image_mapper_1.AddClippingPlane(clipping_plane_1)

image_1 = vtkImageSlice()
image_1.SetMapper(image_mapper_1)
image_1.GetProperty().SetColorWindow(255.0)
image_1.GetProperty().SetColorLevel(127.5)

# Viewport 2: no border, background on
image_mapper_2 = vtkImageSliceMapper()
image_mapper_2.SetInputConnection(reader.GetOutputPort())
image_mapper_2.CroppingOn()
image_mapper_2.SetCroppingRegion(100, 107, 100, 107, 0, 0)
image_mapper_2.BackgroundOn()

clipping_plane_2 = vtkPlane()
clipping_plane_2.SetNormal(-0.5, 0.5, 0)
clipping_plane_2.SetOrigin(105, 105, 0)
image_mapper_2.AddClippingPlane(clipping_plane_2)

image_2 = vtkImageSlice()
image_2.SetMapper(image_mapper_2)
image_2.GetProperty().SetColorWindow(255.0)
image_2.GetProperty().SetColorLevel(127.5)

# Viewport 3: border on, background on
image_mapper_3 = vtkImageSliceMapper()
image_mapper_3.SetInputConnection(reader.GetOutputPort())
image_mapper_3.CroppingOn()
image_mapper_3.SetCroppingRegion(100, 107, 100, 107, 0, 0)
image_mapper_3.BorderOn()
image_mapper_3.BackgroundOn()

clipping_plane_3 = vtkPlane()
clipping_plane_3.SetNormal(-0.5, 0.5, 0)
clipping_plane_3.SetOrigin(105, 105, 0)
image_mapper_3.AddClippingPlane(clipping_plane_3)

image_3 = vtkImageSlice()
image_3.SetMapper(image_mapper_3)
image_3.GetProperty().SetColorWindow(255.0)
image_3.GetProperty().SetColorLevel(127.5)

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
render_window.SetWindowName("slice mapper background")

# Scene
bounds_0 = image_mapper_0.GetBounds()
point_0 = [0.5 * (bounds_0[0] + bounds_0[1]), 0.5 * (bounds_0[2] + bounds_0[3]), 0.5 * (bounds_0[4] + bounds_0[5])]
camera_0 = renderer_0.GetActiveCamera()
camera_0.SetFocalPoint(point_0)
point_0[image_mapper_0.GetOrientation()] += 500.0
camera_0.SetPosition(point_0)
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(5.0)

bounds_1 = image_mapper_1.GetBounds()
point_1 = [0.5 * (bounds_1[0] + bounds_1[1]), 0.5 * (bounds_1[2] + bounds_1[3]), 0.5 * (bounds_1[4] + bounds_1[5])]
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(point_1)
point_1[image_mapper_1.GetOrientation()] += 500.0
camera_1.SetPosition(point_1)
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(5.0)

bounds_2 = image_mapper_2.GetBounds()
point_2 = [0.5 * (bounds_2[0] + bounds_2[1]), 0.5 * (bounds_2[2] + bounds_2[3]), 0.5 * (bounds_2[4] + bounds_2[5])]
camera_2 = renderer_2.GetActiveCamera()
camera_2.SetFocalPoint(point_2)
point_2[image_mapper_2.GetOrientation()] += 500.0
camera_2.SetPosition(point_2)
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(5.0)

bounds_3 = image_mapper_3.GetBounds()
point_3 = [0.5 * (bounds_3[0] + bounds_3[1]), 0.5 * (bounds_3[2] + bounds_3[3]), 0.5 * (bounds_3[4] + bounds_3[5])]
camera_3 = renderer_3.GetActiveCamera()
camera_3.SetFocalPoint(point_3)
point_3[image_mapper_3.GetOrientation()] += 500.0
camera_3.SetPosition(point_3)
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(5.0)

# Interactor
style = vtkInteractorStyleImage()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
