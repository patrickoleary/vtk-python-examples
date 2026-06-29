#!/usr/bin/env python

# Smooth a plane mesh using vtkConstrainedSmoothingFilter with
# user-defined smoothing stencils, comparing constraint distance
# and constraint array strategies in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkCellArray
from vtkmodules.vtkFiltersCore import vtkConstrainedSmoothingFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 4

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

# Manually create smoothing stencils for the 5x5 grid (25 points)
stencils = vtkCellArray()

stencil_data = [
    [1, 5],                # point 0
    [0, 2, 6],             # point 1
    [1, 3, 7],             # point 2
    [2, 4, 8],             # point 3
    [3, 9],                # point 4
    [0, 6, 10],            # point 5
    [1, 7, 11, 5],         # point 6
    [2, 8, 12, 6],         # point 7
    [3, 9, 13, 7],         # point 8
    [4, 8, 14],            # point 9
    [5, 11, 15],           # point 10
    [6, 12, 16, 10],       # point 11
    [7, 13, 17, 11],       # point 12
    [8, 14, 18, 12],       # point 13
    [9, 13, 19],           # point 14
    [10, 16, 20],          # point 15
    [11, 17, 21, 15],      # point 16
    [12, 18, 22, 16],      # point 17
    [13, 19, 23, 17],      # point 18
    [14, 18, 24],          # point 19
    [15, 21],              # point 20
    [20, 16, 22],          # point 21
    [21, 17, 23],          # point 22
    [22, 18, 24],          # point 23
    [19, 23],              # point 24
]

for pts in stencil_data:
    stencils.InsertNextCell(len(pts), pts)

# Filter: smooth with constraint distance and user stencils
smooth_distance = vtkConstrainedSmoothingFilter()
smooth_distance.SetInputConnection(plane.GetOutputPort())
smooth_distance.SetSmoothingStencils(stencils)
smooth_distance.SetConstraintStrategyToConstraintDistance()
smooth_distance.SetConstraintDistance(0.1)
smooth_distance.SetNumberOfIterations(100)
smooth_distance.SetRelaxationFactor(0.2)
smooth_distance.GenerateErrorScalarsOn()
smooth_distance.GenerateErrorVectorsOff()
smooth_distance.Update()

smooth_distance_mapper = vtkPolyDataMapper()
smooth_distance_mapper.SetInputConnection(smooth_distance.GetOutputPort())
smooth_distance_mapper.ScalarVisibilityOn()

smooth_distance_actor = vtkActor()
smooth_distance_actor.SetMapper(smooth_distance_mapper)
smooth_distance_actor.GetProperty().SetInterpolationToFlat()

# Filter: smooth with constraint array and user stencils
smooth_array = vtkConstrainedSmoothingFilter()
smooth_array.SetInputConnection(plane.GetOutputPort())
smooth_array.SetSmoothingStencils(stencils)
smooth_array.SetConstraintStrategyToConstraintArray()
smooth_array.SetNumberOfIterations(100)
smooth_array.SetRelaxationFactor(0.2)
smooth_array.GenerateErrorScalarsOn()
smooth_array.GenerateErrorVectorsOn()
smooth_array.Update()

smooth_array_mapper = vtkPolyDataMapper()
smooth_array_mapper.SetInputConnection(smooth_array.GetOutputPort())
smooth_array_mapper.ScalarVisibilityOff()
smooth_array_mapper.SetScalarModeToUsePointFieldData()
smooth_array_mapper.SelectColorArray("SmoothingErrorScalars")
smooth_array_mapper.SetScalarRange(
    smooth_array.GetOutput().GetPointData().GetArray("SmoothingErrorScalars").GetRange()
)

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
render_window.SetWindowName("constrained smoothing stencils")

# Scene
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
