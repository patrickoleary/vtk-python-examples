#!/usr/bin/env python

# Demonstrate sphere rendering with vertex visibility, edge tubes, and point spheres.

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

# Actor with edge tubes and vertex spheres
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(0.4, 1.0, 1.0)

back_prop = vtkProperty()
back_prop.SetDiffuseColor(0.4, 0.65, 0.8)
actor.SetBackfaceProperty(back_prop)

actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(1.0, 1.0, 1.0)
actor.GetProperty().SetLineWidth(7.0)
actor.GetProperty().RenderLinesAsTubesOn()

actor.GetProperty().VertexVisibilityOn()
actor.GetProperty().SetVertexColor(1.0, 0.5, 1.0)
actor.GetProperty().SetPointSize(14.0)
actor.GetProperty().RenderPointsAsSpheresOn()

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("sphere vertex")

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
