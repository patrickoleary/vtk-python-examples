#!/usr/bin/env python

# Demonstrate vtkPCACurvatureEstimation by sampling points from a cylinder,
# plane, and sphere, estimating PCA curvature, and rendering three views
# for each curvature component.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkAssignAttribute,
)
from vtkmodules.vtkFiltersExtraction import vtkExtractVectorComponents
from vtkmodules.vtkFiltersModeling import vtkPolyDataPointSampler
from vtkmodules.vtkFiltersPoints import vtkPCACurvatureEstimation
from vtkmodules.vtkFiltersSources import (
    vtkCylinderSource,
    vtkPlaneSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a cylinder
cylinder = vtkCylinderSource()
cylinder.SetCenter(-2, 0, 0)
cylinder.SetRadius(0.02)
cylinder.SetHeight(1.8)
cylinder.SetResolution(24)

# Create a plane
plane = vtkPlaneSource()
plane.SetOrigin(-1, -0.5, 0)
plane.SetPoint1(0.5, -0.5, 0)
plane.SetPoint2(-1, 0.5, 0)

# Create a sphere
sphere = vtkSphereSource()
sphere.SetCenter(2, 0, 0)
sphere.SetRadius(0.8)
sphere.SetThetaResolution(96)
sphere.SetPhiResolution(48)

# Combine
append = vtkAppendPolyData()
append.AddInputConnection(cylinder.GetOutputPort())
append.AddInputConnection(plane.GetOutputPort())
append.AddInputConnection(sphere.GetOutputPort())

# Sample points along surfaces
sampler = vtkPolyDataPointSampler()
sampler.SetInputConnection(append.GetOutputPort())
sampler.SetDistance(0.01)
sampler.Update()

# Estimate PCA curvature
curvature_filter = vtkPCACurvatureEstimation()
curvature_filter.SetInputConnection(sampler.GetOutputPort())
curvature_filter.SetSampleSize(20)

timer = vtkTimerLog()
timer.StartTimer()
curvature_filter.Update()
timer.StopTimer()
print("Points processed: {0}".format(sampler.GetOutput().GetNumberOfPoints()))
print("   Time to generate curvature: {0}".format(timer.GetElapsedTime()))

# Break curvature into three separate scalar arrays
assign = vtkAssignAttribute()
assign.SetInputConnection(curvature_filter.GetOutputPort())
assign.Assign("PCACurvature", "VECTORS", "POINT_DATA")

extract = vtkExtractVectorComponents()
extract.SetInputConnection(assign.GetOutputPort())
extract.Update()

# Three curvature component views
curvature_mapper_0 = vtkPointGaussianMapper()
curvature_mapper_0.SetInputConnection(extract.GetOutputPort(0))
curvature_mapper_0.EmissiveOff()
curvature_mapper_0.SetScaleFactor(0.0)

curvature_actor_0 = vtkActor()
curvature_actor_0.SetMapper(curvature_mapper_0)
curvature_actor_0.AddPosition(0, 2.25, 0)

curvature_mapper_1 = vtkPointGaussianMapper()
curvature_mapper_1.SetInputConnection(extract.GetOutputPort(1))
curvature_mapper_1.EmissiveOff()
curvature_mapper_1.SetScaleFactor(0.0)

curvature_actor_1 = vtkActor()
curvature_actor_1.SetMapper(curvature_mapper_1)

curvature_mapper_2 = vtkPointGaussianMapper()
curvature_mapper_2.SetInputConnection(extract.GetOutputPort(2))
curvature_mapper_2.EmissiveOff()
curvature_mapper_2.SetScaleFactor(0.0)

curvature_actor_2 = vtkActor()
curvature_actor_2.SetMapper(curvature_mapper_2)
curvature_actor_2.AddPosition(0, -2.25, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(curvature_actor_0)
renderer.AddActor(curvature_actor_1)
renderer.AddActor(curvature_actor_2)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("pca curvature estimation")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(0, 0, -1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
