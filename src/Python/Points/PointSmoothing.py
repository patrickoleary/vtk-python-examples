#!/usr/bin/env python

# Smooth a point cloud using vtkPointSmoothingFilter. The left viewport
# shows the original noisy point cloud and the right shows the smoothed
# result where points have been relaxed toward local centroids.

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
from vtkmodules.vtkFiltersPoints import vtkPointSmoothingFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a noisy spherical point cloud with elevation scalars
points = vtkPoints()
vertices = vtkCellArray()
scalars = vtkFloatArray()
scalars.SetName("Elevation")
for i in range(800):
    phi = math.acos(1.0 - 2.0 * (i / 800.0))
    theta = math.pi * (1.0 + 5.0**0.5) * i
    noise = 0.15 * math.sin(11.0 * phi) * math.cos(7.0 * theta)
    r = 1.0 + noise
    x = r * math.sin(phi) * math.cos(theta)
    y = r * math.sin(phi) * math.sin(theta)
    z = r * math.cos(phi)
    pid = points.InsertNextPoint(x, y, z)
    vertices.InsertNextCell(1, [pid])
    scalars.InsertNextValue(z)

cloud = vtkPolyData()
cloud.SetPoints(points)
cloud.SetVerts(vertices)
cloud.GetPointData().SetScalars(scalars)

# ---- Left viewport: noisy cloud ----
noisy_mapper = vtkPolyDataMapper()
noisy_mapper.SetInputData(cloud)
noisy_mapper.SetScalarRange(-1.0, 1.0)

noisy_actor = vtkActor()
noisy_actor.SetMapper(noisy_mapper)
noisy_actor.GetProperty().SetPointSize(5)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(noisy_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: smoothed cloud ----
smoother = vtkPointSmoothingFilter()
smoother.SetInputData(cloud)
smoother.SetNumberOfIterations(20)
smoother.SetSmoothingModeToDefault()
smoother.SetNeighborhoodSize(16)

smooth_mapper = vtkPolyDataMapper()
smooth_mapper.SetInputConnection(smoother.GetOutputPort())
smooth_mapper.SetScalarRange(-1.0, 1.0)

smooth_actor = vtkActor()
smooth_actor.SetMapper(smooth_mapper)
smooth_actor.GetProperty().SetPointSize(5)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(smooth_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("PointSmoothing")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
