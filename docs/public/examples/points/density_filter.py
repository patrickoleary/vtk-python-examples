#!/usr/bin/env python

# Demonstrate vtkPointDensityFilter with four density estimation modes:
# fixed radius volume-normalized, relative radius number-of-points,
# weighted fixed radius, and weighted relative radius, displayed as
# image slices in a 2x2 grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersGeneral import vtkRandomAttributeGenerator
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkFitImplicitFunction,
    vtkPointDensityFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
res = 100
n_pts = 1000000
math = vtkMath()
math.RandomSeed(31415)

# Bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.1, 0.2)
sphere.SetRadius(0.75)

# Extract points near sphere surface
extract = vtkFitImplicitFunction()
extract.SetInputConnection(points.GetOutputPort())
extract.SetImplicitFunction(sphere)
extract.SetThreshold(0.005)
extract.GenerateVerticesOn()

# Clip with a plane
plane = vtkPlane()
plane.SetOrigin(sphere.GetCenter())
plane.SetNormal(1, 1, 1)

clipper = vtkClipPolyData()
clipper.SetInputConnection(extract.GetOutputPort())
clipper.SetClipFunction(plane)

# --- Fixed radius, volume normalized ---
timer = vtkTimerLog()

density_filter_0 = vtkPointDensityFilter()
density_filter_0.SetInputConnection(clipper.GetOutputPort())
density_filter_0.SetSampleDimensions(res, res, res)
density_filter_0.SetDensityEstimateToFixedRadius()
density_filter_0.SetRadius(0.05)
density_filter_0.SetRelativeRadius(2.5)
density_filter_0.SetDensityFormToVolumeNormalized()

timer.StartTimer()
density_filter_0.Update()
timer.StopTimer()
print("Time to compute density field: {0}".format(timer.GetElapsedTime()))
scalar_range = density_filter_0.GetOutput().GetScalarRange()

slice_mapper_0 = vtkImageSliceMapper()
slice_mapper_0.BorderOn()
slice_mapper_0.SliceAtFocalPointOn()
slice_mapper_0.SliceFacesCameraOn()
slice_mapper_0.SetInputConnection(density_filter_0.GetOutputPort())

slice_0 = vtkImageSlice()
slice_0.SetMapper(slice_mapper_0)
slice_0.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
slice_0.GetProperty().SetColorLevel(0.5 * (scalar_range[0] + scalar_range[1]))

# --- Relative radius, number of points ---
density_filter_1 = vtkPointDensityFilter()
density_filter_1.SetInputConnection(clipper.GetOutputPort())
density_filter_1.SetSampleDimensions(res, res, res)
density_filter_1.SetRadius(0.05)
density_filter_1.SetDensityEstimateToRelativeRadius()
density_filter_1.SetRelativeRadius(2.5)
density_filter_1.SetDensityFormToNumberOfPoints()

timer.StartTimer()
density_filter_1.Update()
timer.StopTimer()
print("Time to compute density field: {0}".format(timer.GetElapsedTime()))
scalar_range = density_filter_1.GetOutput().GetScalarRange()

slice_mapper_1 = vtkImageSliceMapper()
slice_mapper_1.BorderOn()
slice_mapper_1.SliceAtFocalPointOn()
slice_mapper_1.SliceFacesCameraOn()
slice_mapper_1.SetInputConnection(density_filter_1.GetOutputPort())

slice_1 = vtkImageSlice()
slice_1.SetMapper(slice_mapper_1)
slice_1.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
slice_1.GetProperty().SetColorLevel(0.5 * (scalar_range[0] + scalar_range[1]))

# --- Weighted fixed radius, volume normalized ---
weights = vtkRandomAttributeGenerator()
weights.SetInputConnection(clipper.GetOutputPort())
weights.SetMinimumComponentValue(0.25)
weights.SetMaximumComponentValue(1.75)
weights.GenerateAllDataOff()
weights.GeneratePointScalarsOn()

density_filter_2 = vtkPointDensityFilter()
density_filter_2.SetInputConnection(weights.GetOutputPort())
density_filter_2.SetSampleDimensions(res, res, res)
density_filter_2.SetDensityEstimateToFixedRadius()
density_filter_2.SetRadius(0.05)
density_filter_2.SetRelativeRadius(2.5)
density_filter_2.SetDensityFormToVolumeNormalized()
density_filter_2.ScalarWeightingOn()

timer.StartTimer()
density_filter_2.Update()
timer.StopTimer()
print("Time to compute density field: {0}".format(timer.GetElapsedTime()))
scalar_range = density_filter_2.GetOutput().GetScalarRange()

slice_mapper_2 = vtkImageSliceMapper()
slice_mapper_2.BorderOn()
slice_mapper_2.SliceAtFocalPointOn()
slice_mapper_2.SliceFacesCameraOn()
slice_mapper_2.SetInputConnection(density_filter_2.GetOutputPort())

slice_2 = vtkImageSlice()
slice_2.SetMapper(slice_mapper_2)
slice_2.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
slice_2.GetProperty().SetColorLevel(0.5 * (scalar_range[0] + scalar_range[1]))

# --- Weighted relative radius, number of points ---
density_filter_3 = vtkPointDensityFilter()
density_filter_3.SetInputConnection(weights.GetOutputPort())
density_filter_3.SetSampleDimensions(res, res, res)
density_filter_3.SetRadius(0.05)
density_filter_3.SetDensityEstimateToRelativeRadius()
density_filter_3.SetRelativeRadius(2.5)
density_filter_3.SetDensityFormToNumberOfPoints()
density_filter_3.ScalarWeightingOn()

timer.StartTimer()
density_filter_3.Update()
timer.StopTimer()
print("Time to compute density field: {0}".format(timer.GetElapsedTime()))
scalar_range = density_filter_3.GetOutput().GetScalarRange()

slice_mapper_3 = vtkImageSliceMapper()
slice_mapper_3.BorderOn()
slice_mapper_3.SliceAtFocalPointOn()
slice_mapper_3.SliceFacesCameraOn()
slice_mapper_3.SetInputConnection(density_filter_3.GetOutputPort())

slice_3 = vtkImageSlice()
slice_3.SetMapper(slice_mapper_3)
slice_3.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
slice_3.GetProperty().SetColorLevel(0.5 * (scalar_range[0] + scalar_range[1]))

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 0.5)
renderer_0.AddActor(slice_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 0.5)
renderer_1.AddActor(slice_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0, 0.5, 0.5, 1)
renderer_2.AddActor(slice_2)
renderer_2.SetBackground(0, 0, 0)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.5, 0.5, 1, 1)
renderer_3.AddActor(slice_3)
renderer_3.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(300, 300)
render_window.SetWindowName("density filter")

# Scene
camera = renderer_0.GetActiveCamera()
camera.ParallelProjectionOn()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0, 0, 1)
renderer_0.ResetCamera()

renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)
renderer_3.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
