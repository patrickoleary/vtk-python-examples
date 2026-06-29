#!/usr/bin/env python

# Sample a cylinder implicit function over a random point cloud using
# vtkSampleImplicitFunctionFilter and display with a point Gaussian mapper.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkCylinder
from vtkmodules.vtkFiltersGeneral import vtkSampleImplicitFunctionFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

n_pts = 100000

# Create a random point cloud
points = vtkPointSource()
points.SetNumberOfPoints(n_pts)
points.SetRadius(5)

# Create a cylinder implicit function
cyl = vtkCylinder()
cyl.SetCenter(0, 0, 0)
cyl.SetRadius(0.1)

# Sample the implicit function at the point locations
sample = vtkSampleImplicitFunctionFilter()
sample.SetInputConnection(points.GetOutputPort())
sample.SetImplicitFunction(cyl)
sample.Update()

# Draw the points colored by implicit function value
sample_mapper = vtkPointGaussianMapper()
sample_mapper.SetInputConnection(sample.GetOutputPort())
sample_mapper.EmissiveOff()
sample_mapper.SetScaleFactor(0.0)
sample_mapper.SetScalarRange(0, 20)

sample_actor = vtkActor()
sample_actor.SetMapper(sample_mapper)

# Create an outline
outline = vtkOutlineFilter()
outline.SetInputConnection(sample.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sample_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("sample implicit function")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
cam = renderer.GetActiveCamera()
cam.SetFocalPoint(0, 0, 0)
cam.SetPosition(1, 1, 1)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
