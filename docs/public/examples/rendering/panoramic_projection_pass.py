#!/usr/bin/env python

# Demonstrate panoramic (azimuthal) projection render pass with colored spheres.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkLightsPass,
    vtkOpaquePass,
    vtkPanoramicProjectionPass,
    vtkRenderPassCollection,
    vtkSequencePass,
)

# Sphere source
sphere = vtkSphereSource()
sphere.SetRadius(1.0)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Scene light
light = vtkLight()
light.SetPosition(0.0, 10.0, 0.0)
light.SetFocalPoint(0.0, 0.0, 0.0)
light.SetLightTypeToSceneLight()

# Renderer with no automatic lights or cullers
renderer = vtkRenderer()
renderer.GetCullers().RemoveAllItems()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AutomaticLightCreationOff()

# Render pass pipeline: lights + opaque -> camera -> panoramic projection
camera_pass = vtkCameraPass()
seq = vtkSequencePass()
opaque = vtkOpaquePass()
lights = vtkLightsPass()

passes = vtkRenderPassCollection()
passes.AddItem(lights)
passes.AddItem(opaque)
seq.SetPasses(passes)
camera_pass.SetDelegatePass(seq)

projection_pass = vtkPanoramicProjectionPass()
projection_pass.SetProjectionTypeToAzimuthal()
projection_pass.SetAngle(360.0)
projection_pass.SetDelegatePass(camera_pass)
renderer.SetPass(projection_pass)

# i=0: f=2.0, x=0.0, pos=(0.0, 0.0, 2.0), color=(1.0, 0.0, 0.0)
actor_0 = vtkActor()
actor_0.SetMapper(mapper)
actor_0.SetPosition(0.0, 0.0, 2.0)
actor_0.GetProperty().SetColor(1.0, 0.0, 0.0)
renderer.AddActor(actor_0)

# i=1: f=-2.0, x=0.0, pos=(0.0, 0.0, -2.0), color=(0.0, 1.0, 0.0)
actor_1 = vtkActor()
actor_1.SetMapper(mapper)
actor_1.SetPosition(0.0, 0.0, -2.0)
actor_1.GetProperty().SetColor(0.0, 1.0, 0.0)
renderer.AddActor(actor_1)

# i=2: f=2.0, x=1.0, pos=(2.0, 0.0, 0.0), color=(1.0, 1.0, 0.0)
actor_2 = vtkActor()
actor_2.SetMapper(mapper)
actor_2.SetPosition(2.0, 0.0, 0.0)
actor_2.GetProperty().SetColor(1.0, 1.0, 0.0)
renderer.AddActor(actor_2)

# i=3: f=-2.0, x=1.0, pos=(-2.0, 0.0, 0.0), color=(0.0, 0.0, 1.0)
actor_3 = vtkActor()
actor_3.SetMapper(mapper)
actor_3.SetPosition(-2.0, 0.0, 0.0)
actor_3.GetProperty().SetColor(0.0, 0.0, 1.0)
renderer.AddActor(actor_3)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("panoramic projection pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)

camera = vtkCamera()
camera.SetPosition(0.0, 0.0, 0.0)
camera.SetFocalPoint(0.0, 0.0, 1.0)
camera.SetViewUp(0.0, 1.0, 0.0)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
