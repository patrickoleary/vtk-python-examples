#!/usr/bin/env python

# Demonstrate vtkVoxelGrid by subsampling a random point cloud using
# manual division configuration, rendering original and subsampled
# points in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkCommonSystem import vtkTimerLog
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersPoints import (
    vtkBoundedPointSource,
    vtkVoxelGrid,
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

# Subsample with voxel grid
subsample = vtkVoxelGrid()
subsample.SetInputConnection(points.GetOutputPort())
subsample.SetConfigurationStyleToManual()
subsample.SetDivisions(47, 47, 47)

timer = vtkTimerLog()
timer.StartTimer()
subsample.Update()
timer.StopTimer()
print("Time to subsample: {0}".format(timer.GetElapsedTime()))
print("   Number of divisions: {}".format(subsample.GetDivisions()))
print("   Original number of points: {0}".format(n_pts))
print("   Final number of points: {0}".format(subsample.GetOutput().GetNumberOfPoints()))

# Original points
original_mapper = vtkPointGaussianMapper()
original_mapper.SetInputConnection(points.GetOutputPort())
original_mapper.EmissiveOff()
original_mapper.SetScaleFactor(0.0)

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)

outline = vtkOutlineFilter()
outline.SetInputConnection(points.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Subsampled points
subsample_mapper = vtkPointGaussianMapper()
subsample_mapper.SetInputConnection(subsample.GetOutputPort())
subsample_mapper.EmissiveOff()
subsample_mapper.SetScaleFactor(0.0)

subsample_actor = vtkActor()
subsample_actor.SetMapper(subsample_mapper)

outline_1 = vtkOutlineFilter()
outline_1.SetInputConnection(points.GetOutputPort())

outline_mapper_1 = vtkPolyDataMapper()
outline_mapper_1.SetInputConnection(outline_1.GetOutputPort())

outline_actor_1 = vtkActor()
outline_actor_1.SetMapper(outline_mapper_1)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(original_actor)
renderer_0.AddActor(outline_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(subsample_actor)
renderer_1.AddActor(outline_actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("voxel grid filter")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 1, 1)
renderer_0.ResetCamera()

renderer_1.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
