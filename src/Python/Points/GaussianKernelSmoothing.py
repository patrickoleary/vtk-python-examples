#!/usr/bin/env python

# Interpolate scalar data from a sparse point cloud onto a dense
# target cloud using vtkPointInterpolator with a vtkGaussianKernel.
# The left viewport shows the sparse source points and the right
# shows the dense cloud with interpolated scalars.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersPoints import (
    vtkGaussianKernel,
    vtkPointInterpolator,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a sparse point cloud with an elevation scalar
sparse_pts = vtkPoints()
sparse_verts = vtkCellArray()
sparse_scalars = vtkFloatArray()
sparse_scalars.SetName("Elevation")
for i in range(100):
    phi = math.acos(1.0 - 2.0 * (i / 100.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = sparse_pts.InsertNextPoint(x, y, z)
    sparse_verts.InsertNextCell(1, [pid])
    sparse_scalars.InsertNextValue(z)

sparse_cloud = vtkPolyData()
sparse_cloud.SetPoints(sparse_pts)
sparse_cloud.SetVerts(sparse_verts)
sparse_cloud.GetPointData().SetScalars(sparse_scalars)

# Target: create a dense point cloud without scalars
dense_pts = vtkPoints()
dense_verts = vtkCellArray()
for i in range(2000):
    phi = math.acos(1.0 - 2.0 * (i / 2000.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    x = math.sin(phi) * math.cos(theta)
    y = math.sin(phi) * math.sin(theta)
    z = math.cos(phi)
    pid = dense_pts.InsertNextPoint(x, y, z)
    dense_verts.InsertNextCell(1, [pid])

dense_cloud = vtkPolyData()
dense_cloud.SetPoints(dense_pts)
dense_cloud.SetVerts(dense_verts)

# ---- Left viewport: sparse source cloud ----
sparse_mapper = vtkPolyDataMapper()
sparse_mapper.SetInputData(sparse_cloud)
sparse_mapper.SetScalarRange(-1.0, 1.0)

sparse_actor = vtkActor()
sparse_actor.SetMapper(sparse_mapper)
sparse_actor.GetProperty().SetPointSize(8)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(sparse_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: dense cloud with interpolated scalars ----
kernel = vtkGaussianKernel()
kernel.SetSharpness(2.0)
kernel.SetRadius(0.5)

interpolator = vtkPointInterpolator()
interpolator.SetInputData(dense_cloud)
interpolator.SetSourceData(sparse_cloud)
interpolator.SetKernel(kernel)

interp_mapper = vtkPolyDataMapper()
interp_mapper.SetInputConnection(interpolator.GetOutputPort())
interp_mapper.SetScalarRange(-1.0, 1.0)

interp_actor = vtkActor()
interp_actor.SetMapper(interp_mapper)
interp_actor.GetProperty().SetPointSize(4)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(interp_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("GaussianKernelSmoothing")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
