#!/usr/bin/env python

# Demonstrate vtkFitImplicitFunction by extracting points near a sphere
# surface from a bounded random point source, rendering the extracted
# points with a Gaussian mapper and an outline.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkFitImplicitFunction,
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

# Create bounded random point source
points = vtkBoundedPointSource()
points.SetNumberOfPoints(n_pts)
points.ProduceRandomScalarsOn()
points.ProduceCellOutputOff()
points.Update()

# Sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0.9, 0.1, 0.1)
sphere.SetRadius(0.33)

# Extract points near sphere surface
extract = vtkFitImplicitFunction()
extract.SetInputConnection(points.GetOutputPort())
extract.SetImplicitFunction(sphere)
extract.SetThreshold(0.005)

timer = vtkTimerLog()
timer.StartTimer()
extract.Update()
timer.StopTimer()
print("Time to extract points: {0}".format(timer.GetElapsedTime()))
print("   Number removed: {0}".format(extract.GetNumberOfPointsRemoved()))
print("   Original number of points: {0}".format(n_pts))

extract_mapper = vtkPointGaussianMapper()
extract_mapper.SetInputConnection(extract.GetOutputPort())
extract_mapper.EmissiveOff()
extract_mapper.SetScaleFactor(0.0)

extract_actor = vtkActor()
extract_actor.SetMapper(extract_mapper)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(extract_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("fit implicit function")

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
