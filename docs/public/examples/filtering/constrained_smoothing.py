#!/usr/bin/env python

# Smooth a plane mesh using vtkConstrainedSmoothingFilter with
# constraint distance and constraint array strategies in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkFiltersCore import vtkConstrainedSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 40

# Source: plane mesh
plane = vtkPlaneSource()
plane.SetResolution(resolution, resolution)
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(1, 0, 0)
plane.SetPoint2(0, 1, 0)
plane.Update()

# Create a constraint array pinning corner points
constraints = vtkDoubleArray()
constraints.SetName("SmoothingConstraints")
num_pts = plane.GetOutput().GetNumberOfPoints()
constraints.SetNumberOfTuples(num_pts)
for i in range(num_pts):
    constraints.SetTuple1(i, 1000)
constraints.SetTuple1(0, 0.0)
constraints.SetTuple1(resolution, 0.0)
constraints.SetTuple1(num_pts - resolution - 1, 0.0)
constraints.SetTuple1(num_pts - 1, 0.0)

plane.GetOutput().GetPointData().AddArray(constraints)

# Filter: smooth with constraint distance strategy
smooth_distance = vtkConstrainedSmoothingFilter()
smooth_distance.SetInputConnection(plane.GetOutputPort())
smooth_distance.SetConstraintStrategyToConstraintDistance()
smooth_distance.SetConstraintDistance(0.1)
smooth_distance.SetNumberOfIterations(100)
smooth_distance.SetRelaxationFactor(0.2)
smooth_distance.Update()

smooth_distance_mapper = vtkPolyDataMapper()
smooth_distance_mapper.SetInputConnection(smooth_distance.GetOutputPort())
smooth_distance_mapper.ScalarVisibilityOn()

smooth_distance_actor = vtkActor()
smooth_distance_actor.SetMapper(smooth_distance_mapper)
smooth_distance_actor.GetProperty().SetInterpolationToFlat()

# Filter: smooth with constraint array strategy
smooth_array = vtkConstrainedSmoothingFilter()
smooth_array.SetInputConnection(plane.GetOutputPort())
smooth_array.SetConstraintStrategyToConstraintArray()
smooth_array.SetNumberOfIterations(100)
smooth_array.SetRelaxationFactor(0.2)
smooth_array.Update()

smooth_array_mapper = vtkPolyDataMapper()
smooth_array_mapper.SetInputConnection(smooth_array.GetOutputPort())
smooth_array_mapper.ScalarVisibilityOn()

smooth_array_actor = vtkActor()
smooth_array_actor.SetMapper(smooth_array_mapper)
smooth_array_actor.GetProperty().SetInterpolationToFlat()

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(smooth_distance_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(smooth_array_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("constrained smoothing")

# Scene
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
