#!/usr/bin/env python

# Demonstrate vtkPCANormalEstimation by extracting points near a sphere
# surface, estimating normals oriented toward a point, and rendering
# with hedgehog normals.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import (
    vtkHedgeHog,
    vtkMaskPoints,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkFitImplicitFunction,
    vtkPCANormalEstimation,
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

# Bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.75)

# Extract points near sphere surface
extract = vtkFitImplicitFunction()
extract.SetInputConnection(points.GetOutputPort())
extract.SetImplicitFunction(sphere)
extract.SetThreshold(0.005)
extract.Update()

# Estimate PCA normals oriented toward origin
normal_estimator = vtkPCANormalEstimation()
normal_estimator.SetInputConnection(extract.GetOutputPort())
normal_estimator.SetSampleSize(20)
normal_estimator.FlipNormalsOn()
normal_estimator.SetNormalOrientationToPoint()
normal_estimator.SetOrientationPoint(0, 0, 0)

timer = vtkTimerLog()
timer.StartTimer()
normal_estimator.Update()
timer.StopTimer()
print("Points processed: {0}".format(n_pts))
print("   Time to generate normals: {0}".format(timer.GetElapsedTime()))

normal_mapper = vtkPointGaussianMapper()
normal_mapper.SetInputConnection(normal_estimator.GetOutputPort())
normal_mapper.EmissiveOff()
normal_mapper.SetScaleFactor(0.0)

normal_actor = vtkActor()
normal_actor.SetMapper(normal_mapper)

# Draw normals as hedgehog
mask = vtkMaskPoints()
mask.SetInputConnection(normal_estimator.GetOutputPort())
mask.SetRandomModeType(1)
mask.SetMaximumNumberOfPoints(250)

hedgehog = vtkHedgeHog()
hedgehog.SetInputConnection(mask.GetOutputPort())
hedgehog.SetVectorModeToUseNormal()
hedgehog.SetScaleFactor(0.25)

hedgehog_mapper = vtkPolyDataMapper()
hedgehog_mapper.SetInputConnection(hedgehog.GetOutputPort())

hedgehog_actor = vtkActor()
hedgehog_actor.SetMapper(hedgehog_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(normal_actor)
renderer.AddActor(hedgehog_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("pca normal estimation cloud")

# Scene
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(1, 1, 1)
camera.SetPosition(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
