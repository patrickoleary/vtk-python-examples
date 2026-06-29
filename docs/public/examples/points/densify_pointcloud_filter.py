#!/usr/bin/env python

# Demonstrate vtkDensifyPointCloudFilter by clipping a bounded point source
# to a hemisphere, computing point density before and after densification,
# and displaying the density slices side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkDensifyPointCloudFilter,
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

# Create bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.1, 0.2)
sphere.SetRadius(0.75)

# Extract points within sphere
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

# Density before densification
density_filter_0 = vtkPointDensityFilter()
density_filter_0.SetInputConnection(clipper.GetOutputPort())
density_filter_0.SetSampleDimensions(res, res, res)
density_filter_0.SetDensityEstimateToFixedRadius()
density_filter_0.SetRadius(0.05)
density_filter_0.SetDensityFormToVolumeNormalized()
density_filter_0.Update()
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

# Densify and recompute density
print("Number of input points: {0}".format(clipper.GetOutput().GetNumberOfPoints()))
densify_filter = vtkDensifyPointCloudFilter()
densify_filter.SetInputConnection(clipper.GetOutputPort())
densify_filter.SetTargetDistance(0.025)
densify_filter.SetMaximumNumberOfIterations(5)
densify_filter.Update()
print("Number of output points: {0}".format(densify_filter.GetOutput().GetNumberOfPoints()))

density_filter_1 = vtkPointDensityFilter()
density_filter_1.SetInputConnection(densify_filter.GetOutputPort())
density_filter_1.SetSampleDimensions(res, res, res)
density_filter_1.SetDensityEstimateToFixedRadius()
density_filter_1.SetRadius(0.05)
density_filter_1.SetDensityFormToVolumeNormalized()
density_filter_1.Update()
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

# Renderers side by side
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.AddActor(slice_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1.0)
renderer_1.AddActor(slice_1)
renderer_1.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("densify pointcloud filter")

# Scene
camera = renderer_0.GetActiveCamera()
camera.ParallelProjectionOn()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0, 0, 1)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
