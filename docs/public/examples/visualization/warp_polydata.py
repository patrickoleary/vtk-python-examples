#!/usr/bin/env python

# Demonstrate warping PolyData using thin plate splines and grid transforms
# with different interpolation modes (cubic, linear, nearest) in an
# 8-viewport layout showing forward and inverse transforms.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonTransforms import (
    vtkGeneralTransform,
    vtkThinPlateSplineTransform,
)
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersHybrid import (
    vtkGridTransform,
    vtkTransformToGrid,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source with normals
sphere = vtkSphereSource()
sphere.SetThetaResolution(20)
sphere.SetPhiResolution(20)

ap = vtkPolyDataNormals()
ap.SetInputConnection(sphere.GetOutputPort())

# -- Thin plate spline transform --
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

thin = vtkThinPlateSplineTransform()
thin.SetSourceLandmarks(spoints)
thin.SetTargetLandmarks(tpoints)
thin.SetBasisToR2LogR()

t1 = vtkGeneralTransform()
t1.SetInput(thin)

# -- Row 0, Col 0: thin plate spline forward --
f11 = vtkTransformPolyDataFilter()
f11.SetInputConnection(ap.GetOutputPort())
f11.SetTransform(t1)

m11 = vtkDataSetMapper()
m11.SetInputConnection(f11.GetOutputPort())

a11 = vtkActor()
a11.SetMapper(m11)
a11.RotateY(90)
a11.GetProperty().SetColor(1, 0, 0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.25, 1.0)
renderer_0.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_0.AddActor(a11)

# -- Row 1, Col 0: thin plate spline inverse --
f12 = vtkTransformPolyDataFilter()
f12.SetInputConnection(ap.GetOutputPort())
f12.SetTransform(t1.GetInverse())

m12 = vtkDataSetMapper()
m12.SetInputConnection(f12.GetOutputPort())

a12 = vtkActor()
a12.SetMapper(m12)
a12.RotateY(90)
a12.GetProperty().SetColor(0.9, 0.9, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.0, 0.0, 0.25, 0.5)
renderer_1.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_1.AddActor(a12)

# -- Grid transform from thin plate spline --
grid_trans = vtkTransformToGrid()
grid_trans.SetInput(t1)
grid_trans.SetGridOrigin(-1.5, -1.5, -1.5)
grid_trans.SetGridExtent(0, 60, 0, 60, 0, 60)
grid_trans.SetGridSpacing(0.05, 0.05, 0.05)

# -- Row 0, Col 1: grid transform cubic forward --
t2 = vtkGridTransform()
t2.SetDisplacementGridConnection(grid_trans.GetOutputPort())
t2.SetInterpolationModeToCubic()

f21 = vtkTransformPolyDataFilter()
f21.SetInputConnection(ap.GetOutputPort())
f21.SetTransform(t2)

m21 = vtkDataSetMapper()
m21.SetInputConnection(f21.GetOutputPort())

a21 = vtkActor()
a21.SetMapper(m21)
a21.RotateY(90)
a21.GetProperty().SetColor(1, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.25, 0.5, 0.50, 1.0)
renderer_2.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_2.AddActor(a21)

# -- Row 1, Col 1: grid transform cubic inverse --
f22 = vtkTransformPolyDataFilter()
f22.SetInputConnection(ap.GetOutputPort())
f22.SetTransform(t2.GetInverse())

m22 = vtkDataSetMapper()
m22.SetInputConnection(f22.GetOutputPort())

a22 = vtkActor()
a22.SetMapper(m22)
a22.RotateY(90)
a22.GetProperty().SetColor(0.9, 0.9, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.25, 0.0, 0.50, 0.5)
renderer_3.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_3.AddActor(a22)

# -- Row 0, Col 2: grid transform linear forward --
t3 = vtkGridTransform()
t3.SetDisplacementGridConnection(grid_trans.GetOutputPort())
t3.SetInterpolationModeToLinear()

f31 = vtkTransformPolyDataFilter()
f31.SetInputConnection(ap.GetOutputPort())
f31.SetTransform(t3)

m31 = vtkDataSetMapper()
m31.SetInputConnection(f31.GetOutputPort())

a31 = vtkActor()
a31.SetMapper(m31)
a31.RotateY(90)
a31.GetProperty().SetColor(1, 0, 0)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.50, 0.5, 0.75, 1.0)
renderer_4.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_4.AddActor(a31)

# -- Row 1, Col 2: grid transform linear inverse --
f32 = vtkTransformPolyDataFilter()
f32.SetInputConnection(ap.GetOutputPort())
f32.SetTransform(t3.GetInverse())

m32 = vtkDataSetMapper()
m32.SetInputConnection(f32.GetOutputPort())

a32 = vtkActor()
a32.SetMapper(m32)
a32.RotateY(90)
a32.GetProperty().SetColor(0.9, 0.9, 0)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.5, 0.0, 0.75, 0.5)
renderer_5.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_5.AddActor(a32)

# -- Row 0, Col 3: grid transform nearest forward --
t4 = vtkGridTransform()
t4.SetDisplacementGridConnection(grid_trans.GetOutputPort())
t4.SetInterpolationModeToNearestNeighbor()
t4.SetInverseTolerance(0.05)

f41 = vtkTransformPolyDataFilter()
f41.SetInputConnection(ap.GetOutputPort())
f41.SetTransform(t4)

m41 = vtkDataSetMapper()
m41.SetInputConnection(f41.GetOutputPort())

a41 = vtkActor()
a41.SetMapper(m41)
a41.RotateY(90)
a41.GetProperty().SetColor(1, 0, 0)

renderer_6 = vtkRenderer()
renderer_6.SetViewport(0.75, 0.5, 1.0, 1.0)
renderer_6.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_6.AddActor(a41)

# -- Row 1, Col 3: grid transform nearest inverse --
f42 = vtkTransformPolyDataFilter()
f42.SetInputConnection(ap.GetOutputPort())
f42.SetTransform(t4.GetInverse())

m42 = vtkDataSetMapper()
m42.SetInputConnection(f42.GetOutputPort())

a42 = vtkActor()
a42.SetMapper(m42)
a42.RotateY(90)
a42.GetProperty().SetColor(0.9, 0.9, 0)

renderer_7 = vtkRenderer()
renderer_7.SetViewport(0.75, 0.0, 1.0, 0.5)
renderer_7.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_7.AddActor(a42)

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
render_window.SetWindowName("warp polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Apply rotation to the general transform (matches original test)
t1.RotateX(-100)
t1.PostMultiply()
t1.RotateX(+100)

interactor.Initialize()
interactor.Start()
