#!/usr/bin/env python
# Compare thin-plate spline and B-spline transforms applied to a sphere in eight viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersHybrid import (
    vtkBSplineTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkImageBSplineCoefficients
from vtkmodules.vtkCommonTransforms import vtkThinPlateSplineTransform
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere with normals
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)
sphere.Update()

# Sphere without normals
sphere_data = vtkPolyData()
sphere_data.SetPoints(sphere.GetOutput().GetPoints())
sphere_data.SetPolys(sphere.GetOutput().GetPolys())

# Source and target landmarks for thin-plate spline
spoints = vtkPoints()
spoints.SetNumberOfPoints(10)
spoints.SetPoint(0, 0.000, 0.000, 0.500)
spoints.SetPoint(1, 0.000, 0.000, -0.500)
spoints.SetPoint(2, 0.433, 0.000, 0.250)
spoints.SetPoint(3, 0.433, 0.000, -0.250)
spoints.SetPoint(4, -0.000, 0.433, 0.250)
spoints.SetPoint(5, -0.000, 0.433, -0.250)
spoints.SetPoint(6, -0.433, -0.000, 0.250)
spoints.SetPoint(7, -0.433, -0.000, -0.250)
spoints.SetPoint(8, 0.000, -0.433, 0.250)
spoints.SetPoint(9, 0.000, -0.433, -0.250)

tpoints = vtkPoints()
tpoints.SetNumberOfPoints(10)
tpoints.SetPoint(0, 0.000, 0.000, 0.800)
tpoints.SetPoint(1, 0.000, 0.000, -0.200)
tpoints.SetPoint(2, 0.433, 0.000, 0.350)
tpoints.SetPoint(3, 0.433, 0.000, -0.150)
tpoints.SetPoint(4, -0.000, 0.233, 0.350)
tpoints.SetPoint(5, -0.000, 0.433, -0.150)
tpoints.SetPoint(6, -0.433, -0.000, 0.350)
tpoints.SetPoint(7, -0.433, -0.000, -0.150)
tpoints.SetPoint(8, 0.000, -0.233, 0.350)
tpoints.SetPoint(9, 0.000, -0.433, -0.150)

# Thin-plate spline transform
thin = vtkThinPlateSplineTransform()
thin.SetSourceLandmarks(spoints)
thin.SetTargetLandmarks(tpoints)
thin.SetBasisToR2LogR()

# B-spline approximation of the thin-plate spline
transform_to_grid = vtkTransformToGrid()
transform_to_grid.SetInput(thin)
transform_to_grid.SetGridOrigin(-1.5, -1.5, -1.5)
transform_to_grid.SetGridExtent(0, 60, 0, 60, 0, 60)
transform_to_grid.SetGridSpacing(0.05, 0.05, 0.05)

coeffs = vtkImageBSplineCoefficients()
coeffs.SetInputConnection(transform_to_grid.GetOutputPort())

bspline = vtkBSplineTransform()
bspline.SetCoefficientConnection(coeffs.GetOutputPort())

# -- Filters (eight panels) --
# Top row: forward transforms; Bottom row: inverse transforms
# Columns: thin-plate no normals, b-spline no normals, thin-plate normals, b-spline normals

# Panel 0: top-left, thin-plate forward, no normals
filter_0 = vtkTransformPolyDataFilter()
filter_0.SetInputData(sphere_data)
filter_0.SetTransform(thin)

# Panel 1: top, b-spline forward, no normals
filter_1 = vtkTransformPolyDataFilter()
filter_1.SetInputData(sphere_data)
filter_1.SetTransform(bspline)

# Panel 2: top, thin-plate forward, with normals
filter_2 = vtkTransformPolyDataFilter()
filter_2.SetInputConnection(sphere.GetOutputPort())
filter_2.SetTransform(thin)

# Panel 3: top-right, b-spline forward, with normals
filter_3 = vtkTransformPolyDataFilter()
filter_3.SetInputConnection(sphere.GetOutputPort())
filter_3.SetTransform(bspline)

# Panel 4: bottom-left, thin-plate inverse, no normals
filter_4 = vtkTransformPolyDataFilter()
filter_4.SetInputData(sphere_data)
filter_4.SetTransform(thin.GetInverse())

# Panel 5: bottom, b-spline inverse, no normals
filter_5 = vtkTransformPolyDataFilter()
filter_5.SetInputData(sphere_data)
filter_5.SetTransform(bspline.GetInverse())

# Panel 6: bottom, thin-plate inverse, with normals
filter_6 = vtkTransformPolyDataFilter()
filter_6.SetInputConnection(sphere.GetOutputPort())
filter_6.SetTransform(thin.GetInverse())

# Panel 7: bottom-right, b-spline inverse, with normals
filter_7 = vtkTransformPolyDataFilter()
filter_7.SetInputConnection(sphere.GetOutputPort())
filter_7.SetTransform(bspline.GetInverse())

# -- Mappers --
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(filter_0.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(filter_1.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(filter_2.GetOutputPort())

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(filter_3.GetOutputPort())

mapper_4 = vtkPolyDataMapper()
mapper_4.SetInputConnection(filter_4.GetOutputPort())

mapper_5 = vtkPolyDataMapper()
mapper_5.SetInputConnection(filter_5.GetOutputPort())

mapper_6 = vtkPolyDataMapper()
mapper_6.SetInputConnection(filter_6.GetOutputPort())

mapper_7 = vtkPolyDataMapper()
mapper_7.SetInputConnection(filter_7.GetOutputPort())

# -- Actors --
actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.RotateY(90)
actor_0.GetProperty().SetColor(1, 0, 0)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.RotateY(90)
actor_1.GetProperty().SetColor(1, 0, 0)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.RotateY(90)
actor_2.GetProperty().SetColor(1, 0, 0)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.RotateY(90)
actor_3.GetProperty().SetColor(1, 0, 0)

actor_4 = vtkActor()
actor_4.SetMapper(mapper_4)
actor_4.RotateY(90)
actor_4.GetProperty().SetColor(0.9, 0.9, 0)

actor_5 = vtkActor()
actor_5.SetMapper(mapper_5)
actor_5.RotateY(90)
actor_5.GetProperty().SetColor(0.9, 0.9, 0)

actor_6 = vtkActor()
actor_6.SetMapper(mapper_6)
actor_6.RotateY(90)
actor_6.GetProperty().SetColor(0.9, 0.9, 0)

actor_7 = vtkActor()
actor_7.SetMapper(mapper_7)
actor_7.RotateY(90)
actor_7.GetProperty().SetColor(0.9, 0.9, 0)

# -- Renderers --
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.00, 0.5, 0.25, 1.0)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.25, 0.5, 0.50, 1.0)
renderer_1.AddActor(actor_1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.50, 0.5, 0.75, 1.0)
renderer_2.AddActor(actor_2)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.75, 0.5, 1.00, 1.0)
renderer_3.AddActor(actor_3)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.00, 0.0, 0.25, 0.5)
renderer_4.AddActor(actor_4)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.25, 0.0, 0.50, 0.5)
renderer_5.AddActor(actor_5)

renderer_6 = vtkRenderer()
renderer_6.SetViewport(0.50, 0.0, 0.75, 0.5)
renderer_6.AddActor(actor_6)

renderer_7 = vtkRenderer()
renderer_7.SetViewport(0.75, 0.0, 1.00, 0.5)
renderer_7.AddActor(actor_7)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetSize(600, 300)
render_window.SetWindowName("b spline transform")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_1.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_2.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_3.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_4.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_5.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_6.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_7.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

interactor.Initialize()
interactor.Start()
