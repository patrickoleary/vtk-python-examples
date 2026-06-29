#!/usr/bin/env python

# Test vtkLassoStencilSource with spline and polygon shapes on 3D volume slices.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkLassoStencilSource,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Concave closed contour
lasso_points = [
    (30, 50), (50, 90), (150, 50), (180, 100),
    (100, 170), (60, 170), (30, 50),
]

extent = [0, 63, 0, 63, 1, 93]
origin = [0.0, 0.0, 0.0]
spacing = [3.2, 3.2, 1.5]
center = [0.5 * 3.2 * 63, 0.5 * 3.2 * 63, 0.5 * 1.5 * 94]

# Read volume
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(extent)
reader.SetDataOrigin(origin)
reader.SetDataSpacing(spacing)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# Dimmed version
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(reader.GetOutputPort())
shift_scale.SetScale(0.5)

# --- Pipeline 0: orientation=2, spline, 7 points ---
points_0 = vtkPoints()
points_0.SetNumberOfPoints(7)
for i in range(7):
    point = [0.0, 0.0, 0.0]
    point[0] = lasso_points[i][0]
    point[1] = lasso_points[i][1]
    points_0.SetPoint(i, point)

stencil_source_0 = vtkLassoStencilSource()
stencil_source_0.SetOutputOrigin(origin)
stencil_source_0.SetOutputSpacing(spacing)
stencil_source_0.SetOutputWholeExtent(extent)
stencil_source_0.SetPoints(points_0)
stencil_source_0.SetShapeToSpline()
stencil_source_0.SetSliceOrientation(2)

stencil_0 = vtkImageStencil()
stencil_0.SetInputConnection(0, shift_scale.GetOutputPort())
stencil_0.SetInputConnection(1, reader.GetOutputPort())
stencil_0.SetStencilConnection(stencil_source_0.GetOutputPort())
stencil_0.Update()

mapper_0 = vtkImageSliceMapper()
mapper_0.BorderOn()
mapper_0.SetInputConnection(stencil_0.GetOutputPort())
mapper_0.SliceAtFocalPointOn()
mapper_0.SetOrientation(2)

actor_0 = vtkImageSlice()
actor_0.GetProperty().SetColorWindow(2000.0)
actor_0.GetProperty().SetColorLevel(1000.0)
actor_0.SetMapper(mapper_0)

# --- Pipeline 1: orientation=1, spline, 7 points ---
points_1 = vtkPoints()
points_1.SetNumberOfPoints(7)
for i in range(7):
    point = [0.0, 0.0, 0.0]
    point[2] = lasso_points[i][0]
    point[0] = lasso_points[i][1]
    points_1.SetPoint(i, point)

stencil_source_1 = vtkLassoStencilSource()
stencil_source_1.SetOutputOrigin(origin)
stencil_source_1.SetOutputSpacing(spacing)
stencil_source_1.SetOutputWholeExtent(extent)
stencil_source_1.SetPoints(points_1)
stencil_source_1.SetShapeToSpline()
stencil_source_1.SetSliceOrientation(1)

stencil_1 = vtkImageStencil()
stencil_1.SetInputConnection(0, shift_scale.GetOutputPort())
stencil_1.SetInputConnection(1, reader.GetOutputPort())
stencil_1.SetStencilConnection(stencil_source_1.GetOutputPort())
stencil_1.Update()

mapper_1 = vtkImageSliceMapper()
mapper_1.BorderOn()
mapper_1.SetInputConnection(stencil_1.GetOutputPort())
mapper_1.SliceAtFocalPointOn()
mapper_1.SetOrientation(1)

actor_1 = vtkImageSlice()
actor_1.GetProperty().SetColorWindow(2000.0)
actor_1.GetProperty().SetColorLevel(1000.0)
actor_1.SetMapper(mapper_1)

# --- Pipeline 2: orientation=0, spline, 6 points ---
points_2 = vtkPoints()
points_2.SetNumberOfPoints(6)
for i in range(6):
    point = [0.0, 0.0, 0.0]
    point[1] = lasso_points[i][0]
    point[2] = lasso_points[i][1]
    points_2.SetPoint(i, point)

stencil_source_2 = vtkLassoStencilSource()
stencil_source_2.SetOutputOrigin(origin)
stencil_source_2.SetOutputSpacing(spacing)
stencil_source_2.SetOutputWholeExtent(extent)
stencil_source_2.SetPoints(points_2)
stencil_source_2.SetShapeToSpline()
stencil_source_2.SetSliceOrientation(0)

stencil_2 = vtkImageStencil()
stencil_2.SetInputConnection(0, shift_scale.GetOutputPort())
stencil_2.SetInputConnection(1, reader.GetOutputPort())
stencil_2.SetStencilConnection(stencil_source_2.GetOutputPort())
stencil_2.Update()

mapper_2 = vtkImageSliceMapper()
mapper_2.BorderOn()
mapper_2.SetInputConnection(stencil_2.GetOutputPort())
mapper_2.SliceAtFocalPointOn()
mapper_2.SetOrientation(0)

actor_2 = vtkImageSlice()
actor_2.GetProperty().SetColorWindow(2000.0)
actor_2.GetProperty().SetColorLevel(1000.0)
actor_2.SetMapper(mapper_2)

# --- Pipeline 3: orientation=1, polygon, 6 points ---
points_3 = vtkPoints()
points_3.SetNumberOfPoints(6)
for i in range(6):
    point = [0.0, 0.0, 0.0]
    point[2] = lasso_points[i][0]
    point[0] = lasso_points[i][1]
    points_3.SetPoint(i, point)

stencil_source_3 = vtkLassoStencilSource()
stencil_source_3.SetOutputOrigin(origin)
stencil_source_3.SetOutputSpacing(spacing)
stencil_source_3.SetOutputWholeExtent(extent)
stencil_source_3.SetPoints(points_3)
stencil_source_3.SetShapeToSpline()
stencil_source_3.SetSliceOrientation(1)
stencil_source_3.SetShapeToPolygon()

stencil_3 = vtkImageStencil()
stencil_3.SetInputConnection(0, shift_scale.GetOutputPort())
stencil_3.SetInputConnection(1, reader.GetOutputPort())
stencil_3.SetStencilConnection(stencil_source_3.GetOutputPort())
stencil_3.Update()

mapper_3 = vtkImageSliceMapper()
mapper_3.BorderOn()
mapper_3.SetInputConnection(stencil_3.GetOutputPort())
mapper_3.SliceAtFocalPointOn()
mapper_3.SetOrientation(1)

actor_3 = vtkImageSlice()
actor_3.GetProperty().SetColorWindow(2000.0)
actor_3.GetProperty().SetColorLevel(1000.0)
actor_3.SetMapper(mapper_3)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_0.AddViewProp(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_1.AddViewProp(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_2.AddViewProp(actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_3.AddViewProp(actor_3)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(256, 256)
render_window.SetWindowName("stencil with lasso")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(0.25 * 100.8 * spacing[1])
camera_0.SetFocalPoint(center[0], center[1], center[2])
camera_0.SetPosition(center[0], center[1], center[2] + 10.0)
camera_0.SetViewUp(0.0, 1.0, 0.0)
camera_0.SetClippingRange(5.0, 15.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.25 * 100.8 * spacing[1])
camera_1.SetFocalPoint(center[0], center[1], center[2])
camera_1.SetPosition(center[0], center[1] + 10.0, center[2])
camera_1.SetViewUp(0.0, 0.0, -1.0)
camera_1.SetClippingRange(5.0, 15.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(0.25 * 100.8 * spacing[1])
camera_2.SetFocalPoint(center[0], center[1], center[2])
camera_2.SetPosition(center[0] + 10.0, center[1], center[2])
camera_2.SetViewUp(0.0, 0.0, -1.0)
camera_2.SetClippingRange(5.0, 15.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(0.25 * 100.8 * spacing[1])
camera_3.SetFocalPoint(center[0], center[1], center[2])
camera_3.SetPosition(center[0], center[1] + 10.0, center[2])
camera_3.SetViewUp(0.0, 0.0, -1.0)
camera_3.SetClippingRange(5.0, 15.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

interactor.Initialize()
interactor.Start()
