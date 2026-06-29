#!/usr/bin/env python

# Demonstrate vtkRadiusOutlierRemoval by generating random points,
# removing isolated outliers based on neighbor count within a radius,
# and rendering non-outliers and outliers in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import vtkStaticPointLocator
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkRadiusOutlierRemoval,
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
n_pts = 10000
math = vtkMath()
math.RandomSeed(31415)

# Random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Reuse locator
locator = vtkStaticPointLocator()
locator.SetDataSet(points.GetOutput())
locator.BuildLocator()

# Remove isolated points
removal = vtkRadiusOutlierRemoval()
removal.SetInputConnection(points.GetOutputPort())
removal.SetLocator(locator)
removal.SetRadius(0.1)
removal.SetNumberOfNeighbors(2)
removal.GenerateOutliersOn()

timer = vtkTimerLog()
timer.StartTimer()
removal.Update()
timer.StopTimer()
print("Time to remove points: {0}".format(timer.GetElapsedTime()))
print("   Number removed: {0}".format(removal.GetNumberOfPointsRemoved()))
print("   Original number of points: {0}".format(n_pts))

# Non-outliers
removal_mapper = vtkPointGaussianMapper()
removal_mapper.SetInputConnection(removal.GetOutputPort())
removal_mapper.EmissiveOff()
removal_mapper.SetScaleFactor(0.0)

removal_actor = vtkActor()
removal_actor.SetMapper(removal_mapper)

outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Outliers
outlier_mapper = vtkPointGaussianMapper()
outlier_mapper.SetInputConnection(removal.GetOutputPort(1))
outlier_mapper.EmissiveOff()
outlier_mapper.SetScaleFactor(0.0)

outlier_actor = vtkActor()
outlier_actor.SetMapper(outlier_mapper)

outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(points.GetOutputPort())

outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())

outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(removal_actor)
renderer_0.AddActor(outline_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(outlier_actor)
renderer_1.AddActor(outline_actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("radius outlier removal cloud")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetFocalPoint(1, 1, 1)
camera.SetPosition(0, 0, 0)
renderer_0.ResetCamera()

renderer_1.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
