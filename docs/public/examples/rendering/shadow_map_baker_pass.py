#!/usr/bin/env python

# Demonstrate shadow rendering with the modern renderer.UseShadowsOn() API.
# Modern replacement for the removed vtkShadowMapBakerPass.
# Shadow map generation is now handled internally by the renderer.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.2, 0.2, 1.0)
actor.GetProperty().SetDiffuseColor(1.0, 0.65, 0.7)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.5)
actor.GetProperty().SetSpecularPower(20.0)
actor.GetProperty().SetOpacity(1.0)

# Ground plane to receive shadows
plane = vtkPlaneSource()
plane.SetOrigin(-0.15, -0.05, -0.15)
plane.SetPoint1(0.15, -0.05, -0.15)
plane.SetPoint2(-0.15, -0.05, 0.15)
plane.SetResolution(10, 10)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(0.9, 0.9, 0.9)

# Positional light for shadow casting
light = vtkLight()
light.SetPositional(True)
light.SetPosition(0.0, 0.3, 0.1)
light.SetFocalPoint(0.0, 0.0, 0.0)
light.SetConeAngle(45)
light.SetIntensity(1.0)

# Renderer with shadows enabled
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.4, 0.6)
renderer.AddActor(actor)
renderer.AddActor(plane_actor)
renderer.UseShadowsOn()

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("shadow map baker pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.0)

interactor.Initialize()
interactor.Start()
