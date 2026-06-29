#!/usr/bin/env python

# Demonstrate vtkSignedDistance and vtkExtractSurface by generating a
# hemi-sphere point cloud from implicit functions, estimating normals,
# computing signed distance, and extracting a surface.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkImplicitBoolean,
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkExtractSurface,
    vtkFitImplicitFunction,
    vtkPCANormalEstimation,
    vtkSignedDistance,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Parameters
n_pts = 1000000
math = vtkMath()
math.RandomSeed(31415)

# Random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.75)

# Cut the sphere in half with a plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# Boolean intersection for hemi-sphere
boolean_func = vtkImplicitBoolean()
boolean_func.SetOperationTypeToIntersection()
boolean_func.AddFunction(sphere)
boolean_func.AddFunction(plane)

# Extract points along hemi-sphere surface
extract = vtkFitImplicitFunction()
extract.SetInputConnection(points.GetOutputPort())
extract.SetImplicitFunction(boolean_func)
extract.SetThreshold(0.005)
extract.Update()

# Estimate normals via graph traversal
normal_estimator = vtkPCANormalEstimation()
normal_estimator.SetInputConnection(extract.GetOutputPort())
normal_estimator.SetSampleSize(20)
normal_estimator.FlipNormalsOff()
normal_estimator.SetNormalOrientationToGraphTraversal()
normal_estimator.Update()

point_mapper = vtkPointGaussianMapper()
point_mapper.SetInputConnection(extract.GetOutputPort())
point_mapper.EmissiveOff()
point_mapper.SetScaleFactor(0.0)

point_actor = vtkActor()
point_actor.SetMapper(point_mapper)

# Compute signed distance field
signed_distance = vtkSignedDistance()
signed_distance.SetInputConnection(normal_estimator.GetOutputPort())
signed_distance.SetRadius(0.1)
signed_distance.SetBounds(-1, 1, -1, 1, -1, 1)
signed_distance.SetDimensions(50, 50, 50)

# Extract surface
extract_surface = vtkExtractSurface()
extract_surface.SetInputConnection(signed_distance.GetOutputPort())
extract_surface.SetRadius(0.1)

timer = vtkTimerLog()
timer.StartTimer()
extract_surface.Update()
timer.StopTimer()
print("Points processed: {0}".format(n_pts))
print("   Time to generate and extract distance function: {0}".format(timer.GetElapsedTime()))
print("   Resulting bounds: {}".format(extract_surface.GetOutput().GetBounds()))

surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(extract_surface.GetOutputPort())

surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(point_actor)
renderer.AddActor(surface_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("signed distance filter")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(1, -1, -1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
