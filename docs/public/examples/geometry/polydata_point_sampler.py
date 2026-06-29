#!/usr/bin/env python

# Demonstrate vtkPolyDataPointSampler by creating a sphere, sampling
# points on its surface and interior, then showing a second sampler
# on stripped input alongside the first.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkStripper
from vtkmodules.vtkFiltersModeling import vtkPolyDataPointSampler
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere
sphere = vtkSphereSource()
sphere.SetPhiResolution(25)
sphere.SetThetaResolution(38)
sphere.SetCenter(4.5, 5.5, 5.0)
sphere.SetRadius(2.5)

# Sample points on the sphere
sampler = vtkPolyDataPointSampler()
sampler.SetInputConnection(sphere.GetOutputPort())
sampler.SetDistance(0.05)
sampler.GenerateInteriorPointsOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sampler.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Strip the sphere first, then sample
stripper = vtkStripper()
stripper.SetInputConnection(sphere.GetOutputPort())

sampler_2 = vtkPolyDataPointSampler()
sampler_2.SetInputConnection(stripper.GetOutputPort())
sampler_2.SetDistance(0.05)
sampler_2.GenerateInteriorPointsOn()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(sampler_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.AddPosition(5.5, 0, 0)
actor_2.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(actor_2)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(500, 250)
render_window.SetWindowName("polydata point sampler")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
