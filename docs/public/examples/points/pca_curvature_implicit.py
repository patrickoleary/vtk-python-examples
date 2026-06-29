#!/usr/bin/env python

# Demonstrate vtkPCACurvatureEstimation on points extracted from implicit
# functions (cylinder, box, sphere union), estimating curvature and
# rendering three curvature component views.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import (
    vtkBox,
    vtkCylinder,
    vtkImplicitBoolean,
    vtkSphere,
)
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersCore import vtkAssignAttribute
from vtkmodules.vtkFiltersExtraction import vtkExtractVectorComponents
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkFitImplicitFunction,
    vtkPCACurvatureEstimation,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
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
points.SetBounds(-3, 3, -1, 1, -1, 1)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Implicit functions
cylinder = vtkCylinder()
cylinder.SetCenter(-2, 0, 0)
cylinder.SetRadius(0.02)

box = vtkBox()
box.SetBounds(-1, 0.5, -0.5, 0.5, -0.0005, 0.0005)

sphere = vtkSphere()
sphere.SetCenter(2, 0, 0)
sphere.SetRadius(0.8)

boolean_func = vtkImplicitBoolean()
boolean_func.SetOperationTypeToUnion()
boolean_func.AddFunction(cylinder)
boolean_func.AddFunction(box)
boolean_func.AddFunction(sphere)

# Extract points near surface
extract = vtkFitImplicitFunction()
extract.SetInputConnection(points.GetOutputPort())
extract.SetImplicitFunction(boolean_func)
extract.SetThreshold(0.0005)
extract.Update()

# Estimate PCA curvature
curvature_filter = vtkPCACurvatureEstimation()
curvature_filter.SetInputConnection(extract.GetOutputPort())
curvature_filter.SetSampleSize(6)

timer = vtkTimerLog()
timer.StartTimer()
curvature_filter.Update()
timer.StopTimer()
print("Points processed: {0}".format(n_pts))
print("   Time to generate curvature: {0}".format(timer.GetElapsedTime()))

# Break curvature into three separate scalar arrays
assign = vtkAssignAttribute()
assign.SetInputConnection(curvature_filter.GetOutputPort())
assign.Assign("PCACurvature", "VECTORS", "POINT_DATA")

vec_extract = vtkExtractVectorComponents()
vec_extract.SetInputConnection(assign.GetOutputPort())
vec_extract.Update()

# Three curvature component views
curvature_mapper_0 = vtkPointGaussianMapper()
curvature_mapper_0.SetInputConnection(vec_extract.GetOutputPort(0))
curvature_mapper_0.EmissiveOff()
curvature_mapper_0.SetScaleFactor(0.0)

curvature_actor_0 = vtkActor()
curvature_actor_0.SetMapper(curvature_mapper_0)
curvature_actor_0.AddPosition(0, 2.25, 0)

curvature_mapper_1 = vtkPointGaussianMapper()
curvature_mapper_1.SetInputConnection(vec_extract.GetOutputPort(1))
curvature_mapper_1.EmissiveOff()
curvature_mapper_1.SetScaleFactor(0.0)

curvature_actor_1 = vtkActor()
curvature_actor_1.SetMapper(curvature_mapper_1)

curvature_mapper_2 = vtkPointGaussianMapper()
curvature_mapper_2.SetInputConnection(vec_extract.GetOutputPort(2))
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
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("pca curvature implicit")

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
