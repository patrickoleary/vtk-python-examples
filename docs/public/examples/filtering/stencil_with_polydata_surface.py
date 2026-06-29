#!/usr/bin/env python

# Test vtkPolyDataToImageStencil with nested 3D surfaces and slice visualization.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkCommonCore import (
    VTK_UNSIGNED_CHAR,
    vtkBoxMuellerRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkImageData,
    vtkPlane,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkCutter,
    vtkStripper,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkPolyDataToImageStencil,
)
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

spacing = [0.9765625, 0.9765625, 3.0]
origin = [-124.51171875, -124.51171875, -105.0]
extent = [0, 255, 0, 255, 0, 70]

# Create white 3D image
image = vtkImageData()
image.SetSpacing(spacing)
image.SetOrigin(origin)
image.SetExtent(extent)
image.AllocateScalars(VTK_UNSIGNED_CHAR, 1)
image.GetPointData().GetScalars().Fill(255)

# Sphere source
sphere_source = vtkSphereSource()
sphere_source.SetRadius(100)
sphere_source.SetPhiResolution(21)
sphere_source.SetThetaResolution(41)
sphere_source.Update()

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(sphere_source.GetOutputPort())
triangle_filter.Update()

# Add noise to sphere points
random_sequence = vtkBoxMuellerRandomSequence()
poly_data = vtkPolyData()
poly_data.DeepCopy(triangle_filter.GetOutput())
sphere_points = poly_data.GetPoints()
new_points = vtkPoints()
new_points.SetNumberOfPoints(sphere_points.GetNumberOfPoints())
for i in range(sphere_points.GetNumberOfPoints()):
    pt = list(sphere_points.GetPoint(i))
    r = math.exp(random_sequence.GetScaledValue(0.0, 0.1))
    random_sequence.Next()
    pt[0] *= r
    pt[1] *= r
    pt[2] *= r
    new_points.SetPoint(i, pt)
poly_data.SetPoints(new_points)

# Create triangle strips for second surface
stripper = vtkStripper()
stripper.SetInputConnection(triangle_filter.GetOutputPort())

transform = vtkTransform()
transform.Scale(0.49, 0.5, 0.6)
transform.Translate(9.111, -7.56, 1.0)
transform.RotateWXYZ(30, 1.0, 0.5, 0.0)

transform_filter = vtkTransformPolyDataFilter()
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(stripper.GetOutputPort())

# Append nested surfaces
append = vtkAppendPolyData()
append.SetInputData(poly_data)
append.AddInputConnection(transform_filter.GetOutputPort())

# Stencil from 3D surface
stencil_source = vtkPolyDataToImageStencil()
stencil_source.SetOutputOrigin(origin)
stencil_source.SetOutputSpacing(spacing)
stencil_source.SetOutputWholeExtent(extent)
stencil_source.SetInputConnection(append.GetOutputPort())

stencil = vtkImageStencil()
stencil.SetInputData(image)
stencil.SetStencilConnection(stencil_source.GetOutputPort())
stencil.Update()

# --- Pipeline 0: z_idx=3 ---
z_0 = 3 * spacing[2] + origin[2]

plane_0 = vtkPlane()
plane_0.SetNormal(0.0, 0.0, 1.0)
plane_0.SetOrigin(0.0, 0.0, z_0)

cutter_0 = vtkCutter()
cutter_0.SetInputConnection(append.GetOutputPort())
cutter_0.SetCutFunction(plane_0)
cutter_0.GenerateCutScalarsOff()

poly_mapper_0 = vtkPolyDataMapper()
poly_mapper_0.SetInputConnection(cutter_0.GetOutputPort())
poly_mapper_0.ScalarVisibilityOff()

poly_actor_0 = vtkActor()
poly_actor_0.SetMapper(poly_mapper_0)
poly_actor_0.GetProperty().SetDiffuse(0.0)
poly_actor_0.GetProperty().SetAmbient(1.0)
poly_actor_0.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_0.SetPosition(0.0, 0.0, 1.0)

slice_mapper_0 = vtkImageSliceMapper()
slice_mapper_0.SetOrientation(2)
slice_mapper_0.SetSliceNumber(3)
slice_mapper_0.SetInputConnection(stencil.GetOutputPort())

slice_actor_0 = vtkImageSlice()
slice_actor_0.GetProperty().SetColorWindow(255.0)
slice_actor_0.GetProperty().SetColorLevel(127.5)
slice_actor_0.GetProperty().SetInterpolationTypeToLinear()
slice_actor_0.SetMapper(slice_mapper_0)

# --- Pipeline 1: z_idx=14 ---
z_1 = 14 * spacing[2] + origin[2]

plane_1 = vtkPlane()
plane_1.SetNormal(0.0, 0.0, 1.0)
plane_1.SetOrigin(0.0, 0.0, z_1)

cutter_1 = vtkCutter()
cutter_1.SetInputConnection(append.GetOutputPort())
cutter_1.SetCutFunction(plane_1)
cutter_1.GenerateCutScalarsOff()

poly_mapper_1 = vtkPolyDataMapper()
poly_mapper_1.SetInputConnection(cutter_1.GetOutputPort())
poly_mapper_1.ScalarVisibilityOff()

poly_actor_1 = vtkActor()
poly_actor_1.SetMapper(poly_mapper_1)
poly_actor_1.GetProperty().SetDiffuse(0.0)
poly_actor_1.GetProperty().SetAmbient(1.0)
poly_actor_1.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_1.SetPosition(0.0, 0.0, 1.0)

slice_mapper_1 = vtkImageSliceMapper()
slice_mapper_1.SetOrientation(2)
slice_mapper_1.SetSliceNumber(14)
slice_mapper_1.SetInputConnection(stencil.GetOutputPort())

slice_actor_1 = vtkImageSlice()
slice_actor_1.GetProperty().SetColorWindow(255.0)
slice_actor_1.GetProperty().SetColorLevel(127.5)
slice_actor_1.GetProperty().SetInterpolationTypeToLinear()
slice_actor_1.SetMapper(slice_mapper_1)

# --- Pipeline 2: z_idx=25 ---
z_2 = 25 * spacing[2] + origin[2]

plane_2 = vtkPlane()
plane_2.SetNormal(0.0, 0.0, 1.0)
plane_2.SetOrigin(0.0, 0.0, z_2)

cutter_2 = vtkCutter()
cutter_2.SetInputConnection(append.GetOutputPort())
cutter_2.SetCutFunction(plane_2)
cutter_2.GenerateCutScalarsOff()

poly_mapper_2 = vtkPolyDataMapper()
poly_mapper_2.SetInputConnection(cutter_2.GetOutputPort())
poly_mapper_2.ScalarVisibilityOff()

poly_actor_2 = vtkActor()
poly_actor_2.SetMapper(poly_mapper_2)
poly_actor_2.GetProperty().SetDiffuse(0.0)
poly_actor_2.GetProperty().SetAmbient(1.0)
poly_actor_2.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_2.SetPosition(0.0, 0.0, 1.0)

slice_mapper_2 = vtkImageSliceMapper()
slice_mapper_2.SetOrientation(2)
slice_mapper_2.SetSliceNumber(25)
slice_mapper_2.SetInputConnection(stencil.GetOutputPort())

slice_actor_2 = vtkImageSlice()
slice_actor_2.GetProperty().SetColorWindow(255.0)
slice_actor_2.GetProperty().SetColorLevel(127.5)
slice_actor_2.GetProperty().SetInterpolationTypeToLinear()
slice_actor_2.SetMapper(slice_mapper_2)

# --- Pipeline 3: z_idx=36 ---
z_3 = 36 * spacing[2] + origin[2]

plane_3 = vtkPlane()
plane_3.SetNormal(0.0, 0.0, 1.0)
plane_3.SetOrigin(0.0, 0.0, z_3)

cutter_3 = vtkCutter()
cutter_3.SetInputConnection(append.GetOutputPort())
cutter_3.SetCutFunction(plane_3)
cutter_3.GenerateCutScalarsOff()

poly_mapper_3 = vtkPolyDataMapper()
poly_mapper_3.SetInputConnection(cutter_3.GetOutputPort())
poly_mapper_3.ScalarVisibilityOff()

poly_actor_3 = vtkActor()
poly_actor_3.SetMapper(poly_mapper_3)
poly_actor_3.GetProperty().SetDiffuse(0.0)
poly_actor_3.GetProperty().SetAmbient(1.0)
poly_actor_3.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_3.SetPosition(0.0, 0.0, 1.0)

slice_mapper_3 = vtkImageSliceMapper()
slice_mapper_3.SetOrientation(2)
slice_mapper_3.SetSliceNumber(36)
slice_mapper_3.SetInputConnection(stencil.GetOutputPort())

slice_actor_3 = vtkImageSlice()
slice_actor_3.GetProperty().SetColorWindow(255.0)
slice_actor_3.GetProperty().SetColorLevel(127.5)
slice_actor_3.GetProperty().SetInterpolationTypeToLinear()
slice_actor_3.SetMapper(slice_mapper_3)

# --- Pipeline 4: z_idx=47 ---
z_4 = 47 * spacing[2] + origin[2]

plane_4 = vtkPlane()
plane_4.SetNormal(0.0, 0.0, 1.0)
plane_4.SetOrigin(0.0, 0.0, z_4)

cutter_4 = vtkCutter()
cutter_4.SetInputConnection(append.GetOutputPort())
cutter_4.SetCutFunction(plane_4)
cutter_4.GenerateCutScalarsOff()

poly_mapper_4 = vtkPolyDataMapper()
poly_mapper_4.SetInputConnection(cutter_4.GetOutputPort())
poly_mapper_4.ScalarVisibilityOff()

poly_actor_4 = vtkActor()
poly_actor_4.SetMapper(poly_mapper_4)
poly_actor_4.GetProperty().SetDiffuse(0.0)
poly_actor_4.GetProperty().SetAmbient(1.0)
poly_actor_4.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_4.SetPosition(0.0, 0.0, 1.0)

slice_mapper_4 = vtkImageSliceMapper()
slice_mapper_4.SetOrientation(2)
slice_mapper_4.SetSliceNumber(47)
slice_mapper_4.SetInputConnection(stencil.GetOutputPort())

slice_actor_4 = vtkImageSlice()
slice_actor_4.GetProperty().SetColorWindow(255.0)
slice_actor_4.GetProperty().SetColorLevel(127.5)
slice_actor_4.GetProperty().SetInterpolationTypeToLinear()
slice_actor_4.SetMapper(slice_mapper_4)

# --- Pipeline 5: z_idx=58 ---
z_5 = 58 * spacing[2] + origin[2]

plane_5 = vtkPlane()
plane_5.SetNormal(0.0, 0.0, 1.0)
plane_5.SetOrigin(0.0, 0.0, z_5)

cutter_5 = vtkCutter()
cutter_5.SetInputConnection(append.GetOutputPort())
cutter_5.SetCutFunction(plane_5)
cutter_5.GenerateCutScalarsOff()

poly_mapper_5 = vtkPolyDataMapper()
poly_mapper_5.SetInputConnection(cutter_5.GetOutputPort())
poly_mapper_5.ScalarVisibilityOff()

poly_actor_5 = vtkActor()
poly_actor_5.SetMapper(poly_mapper_5)
poly_actor_5.GetProperty().SetDiffuse(0.0)
poly_actor_5.GetProperty().SetAmbient(1.0)
poly_actor_5.GetProperty().SetColor(0.1, 0.6, 0.1)
poly_actor_5.SetPosition(0.0, 0.0, 1.0)

slice_mapper_5 = vtkImageSliceMapper()
slice_mapper_5.SetOrientation(2)
slice_mapper_5.SetSliceNumber(58)
slice_mapper_5.SetInputConnection(stencil.GetOutputPort())

slice_actor_5 = vtkImageSlice()
slice_actor_5.GetProperty().SetColorWindow(255.0)
slice_actor_5.GetProperty().SetColorLevel(127.5)
slice_actor_5.GetProperty().SetInterpolationTypeToLinear()
slice_actor_5.SetMapper(slice_mapper_5)

# Renderers (3x2 grid)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 1.0 / 3.0, 1.0)
renderer_0.AddViewProp(slice_actor_0)
renderer_0.AddViewProp(poly_actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(1.0 / 3.0, 0.5, 2.0 / 3.0, 1.0)
renderer_1.AddViewProp(slice_actor_1)
renderer_1.AddViewProp(poly_actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(2.0 / 3.0, 0.5, 1.0, 1.0)
renderer_2.AddViewProp(slice_actor_2)
renderer_2.AddViewProp(poly_actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.0, 0.0, 1.0 / 3.0, 0.5)
renderer_3.AddViewProp(slice_actor_3)
renderer_3.AddViewProp(poly_actor_3)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)
renderer_4.AddViewProp(slice_actor_4)
renderer_4.AddViewProp(poly_actor_4)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(2.0 / 3.0, 0.0, 1.0, 0.5)
renderer_5.AddViewProp(slice_actor_5)
renderer_5.AddViewProp(poly_actor_5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(256 * 3, 256 * 2)
render_window.SetWindowName("stencil with polydata surface")

# Scene
camera_0 = renderer_0.GetActiveCamera()
camera_0.ParallelProjectionOn()
camera_0.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_0.SetFocalPoint(0.0, 0.0, z_0)
camera_0.SetPosition(0.0, 0.0, z_0 + 10.0)
camera_0.SetViewUp(0.0, 1.0, 0.0)
camera_0.SetClippingRange(5.0, 15.0)

camera_1 = renderer_1.GetActiveCamera()
camera_1.ParallelProjectionOn()
camera_1.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_1.SetFocalPoint(0.0, 0.0, z_1)
camera_1.SetPosition(0.0, 0.0, z_1 + 10.0)
camera_1.SetViewUp(0.0, 1.0, 0.0)
camera_1.SetClippingRange(5.0, 15.0)

camera_2 = renderer_2.GetActiveCamera()
camera_2.ParallelProjectionOn()
camera_2.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_2.SetFocalPoint(0.0, 0.0, z_2)
camera_2.SetPosition(0.0, 0.0, z_2 + 10.0)
camera_2.SetViewUp(0.0, 1.0, 0.0)
camera_2.SetClippingRange(5.0, 15.0)

camera_3 = renderer_3.GetActiveCamera()
camera_3.ParallelProjectionOn()
camera_3.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_3.SetFocalPoint(0.0, 0.0, z_3)
camera_3.SetPosition(0.0, 0.0, z_3 + 10.0)
camera_3.SetViewUp(0.0, 1.0, 0.0)
camera_3.SetClippingRange(5.0, 15.0)

camera_4 = renderer_4.GetActiveCamera()
camera_4.ParallelProjectionOn()
camera_4.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_4.SetFocalPoint(0.0, 0.0, z_4)
camera_4.SetPosition(0.0, 0.0, z_4 + 10.0)
camera_4.SetViewUp(0.0, 1.0, 0.0)
camera_4.SetClippingRange(5.0, 15.0)

camera_5 = renderer_5.GetActiveCamera()
camera_5.ParallelProjectionOn()
camera_5.SetParallelScale(0.5 * spacing[1] * (extent[3] - extent[2]))
camera_5.SetFocalPoint(0.0, 0.0, z_5)
camera_5.SetPosition(0.0, 0.0, z_5 + 10.0)
camera_5.SetViewUp(0.0, 1.0, 0.0)
camera_5.SetClippingRange(5.0, 15.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

interactor.Initialize()
interactor.Start()
