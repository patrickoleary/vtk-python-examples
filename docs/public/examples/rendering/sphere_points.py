#!/usr/bin/env python

# Demonstrate sphere rendering with edge tubes and point spheres.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Partial sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(16)
sphere.SetPhiResolution(16)
sphere.SetEndTheta(270.0)

# Surface actor with edge tubes and backface property
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(sphere.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(0.4, 1.0, 1.0)
back_prop = vtkProperty()
back_prop.SetDiffuseColor(0.4, 0.65, 0.8)
actor_0.SetBackfaceProperty(back_prop)
actor_0.GetProperty().EdgeVisibilityOn()
actor_0.GetProperty().SetLineWidth(7.0)
actor_0.GetProperty().RenderLinesAsTubesOn()
actor_0.GetProperty().SetEdgeColor(1.0, 1.0, 1.0)

# Points actor with spherical points
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(sphere.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor_1.GetProperty().SetSpecular(0.5)
actor_1.GetProperty().SetDiffuse(0.7)
actor_1.GetProperty().SetSpecularPower(20.0)
actor_1.GetProperty().RenderPointsAsSpheresOn()
actor_1.GetProperty().SetPointSize(14.0)
actor_1.GetProperty().SetRepresentationToPoints()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("sphere points")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(-45)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.GetActiveCamera().Zoom(1.5)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
