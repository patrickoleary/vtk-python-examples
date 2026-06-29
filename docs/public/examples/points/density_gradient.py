#!/usr/bin/env python

# Demonstrate vtkPointDensityFilter with gradient computation, showing
# gradient magnitude as an image slice, classification labels, and
# gradient vectors via hedgehog in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import (
    vtkAssignAttribute,
    vtkClipPolyData,
    vtkFlyingEdgesPlaneCutter,
    vtkHedgeHog,
)
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkFitImplicitFunction,
    vtkPointDensityFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkPolyDataMapper,
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
clip_plane = vtkPlane()
clip_plane.SetOrigin(sphere.GetCenter())
clip_plane.SetNormal(1, 1, 1)

clipper = vtkClipPolyData()
clipper.SetInputConnection(extract.GetOutputPort())
clipper.SetClipFunction(clip_plane)

# Density with gradient
density_filter = vtkPointDensityFilter()
density_filter.SetInputConnection(clipper.GetOutputPort())
density_filter.SetSampleDimensions(res, res, res)
density_filter.SetDensityEstimateToFixedRadius()
density_filter.SetRadius(0.05)
density_filter.SetRelativeRadius(2.5)
density_filter.SetDensityFormToNumberOfPoints()
density_filter.ComputeGradientOn()
density_filter.Update()
scalar_range = density_filter.GetOutput().GetPointData().GetArray("Gradient Magnitude").GetRange()

# Gradient magnitude slice
assign_0 = vtkAssignAttribute()
assign_0.SetInputConnection(density_filter.GetOutputPort())
assign_0.Assign("Gradient Magnitude", "SCALARS", "POINT_DATA")

slice_mapper_0 = vtkImageSliceMapper()
slice_mapper_0.BorderOn()
slice_mapper_0.SliceAtFocalPointOn()
slice_mapper_0.SliceFacesCameraOn()
slice_mapper_0.SetInputConnection(assign_0.GetOutputPort())

slice_0 = vtkImageSlice()
slice_0.SetMapper(slice_mapper_0)
slice_0.GetProperty().SetColorWindow(scalar_range[1] - scalar_range[0])
slice_0.GetProperty().SetColorLevel(0.5 * (scalar_range[0] + scalar_range[1]))

# Classification labels slice
assign_1 = vtkAssignAttribute()
assign_1.SetInputConnection(density_filter.GetOutputPort())
assign_1.Assign("Classification", "SCALARS", "POINT_DATA")

slice_mapper_1 = vtkImageSliceMapper()
slice_mapper_1.BorderOn()
slice_mapper_1.SliceAtFocalPointOn()
slice_mapper_1.SliceFacesCameraOn()
slice_mapper_1.SetInputConnection(assign_1.GetOutputPort())
slice_mapper_1.Update()

slice_1 = vtkImageSlice()
slice_1.SetMapper(slice_mapper_1)
slice_1.GetProperty().SetColorWindow(1)
slice_1.GetProperty().SetColorLevel(0.5)

# Gradient vectors via hedgehog on a plane cut
assign_2 = vtkAssignAttribute()
assign_2.SetInputConnection(density_filter.GetOutputPort())
assign_2.Assign("Gradient", "VECTORS", "POINT_DATA")

cut_plane = vtkPlane()
cut_plane.SetNormal(0, 0, 1)
cut_plane.SetOrigin(0.0701652, 0.172689, 0.27271)

cut = vtkFlyingEdgesPlaneCutter()
cut.SetInputConnection(assign_2.GetOutputPort())
cut.SetPlane(cut_plane)
cut.InterpolateAttributesOn()

hedgehog = vtkHedgeHog()
hedgehog.SetInputConnection(cut.GetOutputPort())
hedgehog.SetScaleFactor(0.0001)

hedgehog_mapper = vtkPolyDataMapper()
hedgehog_mapper.SetInputConnection(hedgehog.GetOutputPort())
hedgehog_mapper.SetScalarRange(scalar_range)

hedgehog_actor = vtkActor()
hedgehog_actor.SetMapper(hedgehog_mapper)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 1)
renderer_0.AddActor(slice_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.667, 1)
renderer_1.AddActor(slice_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.667, 0, 1, 1)
renderer_2.AddActor(hedgehog_actor)
renderer_2.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(450, 150)
render_window.SetWindowName("density gradient")

# Scene
camera = renderer_0.GetActiveCamera()
camera.ParallelProjectionOn()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0, 0, 1)
renderer_0.ResetCamera()

renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
