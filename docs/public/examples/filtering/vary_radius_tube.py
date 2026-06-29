#!/usr/bin/env python

# Demonstrate vtkTubeFilter with varying radius modes (by scalar, by vector,
# by vector norm) on streamlines traced through a wavelet gradient field.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.SetCenter(0, 0, 0)

# Gradient of the wavelet
gradient = vtkImageGradient()
gradient.SetInputConnection(wavelet.GetOutputPort())
gradient.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData")
gradient.SetDimensionality(3)

# --- Vary radius by scalar ---
seeds_scalar = vtkPolyData()
seed_points_scalar = vtkPoints()
for x in range(9):
    seed_points_scalar.InsertNextPoint(float(x), 0, 0)
seeds_scalar.SetPoints(seed_points_scalar)

stream_scalar = vtkStreamTracer()
stream_scalar.SetInputConnection(gradient.GetOutputPort())
stream_scalar.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
stream_scalar.SetSourceData(seeds_scalar)
stream_scalar.SetIntegrationDirection(2)  # BOTH
stream_scalar.SetIntegratorType(2)        # Runge-Kutta 4-5

tube_scalar = vtkTubeFilter()
tube_scalar.SetInputConnection(stream_scalar.GetOutputPort())
tube_scalar.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData")
tube_scalar.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
tube_scalar.SetRadiusFactor(0.1)
tube_scalar.SetVaryRadiusToVaryRadiusByScalar()
tube_scalar.Update()

mapper_scalar = vtkPolyDataMapper()
mapper_scalar.SetInputData(tube_scalar.GetOutput())

actor_scalar = vtkActor()
actor_scalar.SetMapper(mapper_scalar)

# --- Vary radius by vector ---
seeds_vector = vtkPolyData()
seed_points_vector = vtkPoints()
for x in range(9):
    seed_points_vector.InsertNextPoint(float(x), -4.0, 0)
seeds_vector.SetPoints(seed_points_vector)

stream_vector = vtkStreamTracer()
stream_vector.SetInputConnection(gradient.GetOutputPort())
stream_vector.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
stream_vector.SetSourceData(seeds_vector)
stream_vector.SetIntegrationDirection(2)  # BOTH
stream_vector.SetIntegratorType(2)        # Runge-Kutta 4-5

tube_vector = vtkTubeFilter()
tube_vector.SetInputConnection(stream_vector.GetOutputPort())
tube_vector.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData")
tube_vector.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
tube_vector.SetRadiusFactor(0.1)
tube_vector.SetVaryRadiusToVaryRadiusByVector()
tube_vector.Update()

mapper_vector = vtkPolyDataMapper()
mapper_vector.SetInputData(tube_vector.GetOutput())

actor_vector = vtkActor()
actor_vector.SetMapper(mapper_vector)

# --- Vary radius by vector norm ---
seeds_vector_norm = vtkPolyData()
seed_points_vector_norm = vtkPoints()
for x in range(9):
    seed_points_vector_norm.InsertNextPoint(float(x), 4.0, 0)
seeds_vector_norm.SetPoints(seed_points_vector_norm)

stream_vector_norm = vtkStreamTracer()
stream_vector_norm.SetInputConnection(gradient.GetOutputPort())
stream_vector_norm.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
stream_vector_norm.SetSourceData(seeds_vector_norm)
stream_vector_norm.SetIntegrationDirection(2)  # BOTH
stream_vector_norm.SetIntegratorType(2)        # Runge-Kutta 4-5

tube_vector_norm = vtkTubeFilter()
tube_vector_norm.SetInputConnection(stream_vector_norm.GetOutputPort())
tube_vector_norm.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData")
tube_vector_norm.SetInputArrayToProcess(
    1, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTDataGradient")
tube_vector_norm.SetRadiusFactor(0.1)
tube_vector_norm.SetVaryRadiusToVaryRadiusByVectorNorm()
tube_vector_norm.Update()

mapper_vector_norm = vtkPolyDataMapper()
mapper_vector_norm.SetInputData(tube_vector_norm.GetOutput())

actor_vector_norm = vtkActor()
actor_vector_norm.SetMapper(mapper_vector_norm)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_scalar)
renderer.AddActor(actor_vector)
renderer.AddActor(actor_vector_norm)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("vary radius tube")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
