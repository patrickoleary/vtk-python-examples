#!/usr/bin/env python

# Demonstrate shadow map render pass with a dragon model and ground plane.

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
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkRenderPassCollection,
    vtkSequencePass,
    vtkShadowMapBakerPass,
    vtkShadowMapPass,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Scene lights
light_1 = vtkLight()
light_1.SetFocalPoint(1, 0, 1)
light_1.SetPosition(0, 1, 0.2)
light_1.SetColor(0.95, 0.97, 1.0)
light_1.SetIntensity(0.8)

light_2 = vtkLight()
light_2.SetFocalPoint(0, 0, 1)
light_2.SetPosition(0.2, 0.5, 0.5)
light_2.SetColor(1.0, 0.8, 0.7)
light_2.SetIntensity(0.5)

light_3 = vtkLight()
light_3.SetFocalPoint(-0.1, -0.5, -0.5)
light_3.SetPosition(0.2, 0.5, 0.5)
light_3.SetColor(1.0, 0.8, 0.7)
light_3.SetPositional(True)
light_3.SetIntensity(0.3)

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbientColor(0.135, 0.2225, 0.3)
actor.GetProperty().SetDiffuseColor(0.54, 0.89, 0.63)
actor.GetProperty().SetSpecularColor(1.0, 1.0, 1.0)
actor.GetProperty().SetSpecular(0.51)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.7)
actor.GetProperty().SetSpecularPower(30.0)
actor.GetProperty().SetOpacity(1.0)

# Ground plane under the dragon
ply_bounds = mapper.GetBounds()
plane = vtkPlaneSource()
plane.SetOrigin(-0.2, ply_bounds[2], -0.2)
plane.SetPoint1(0.2, ply_bounds[2], -0.2)
plane.SetPoint2(-0.2, ply_bounds[2], 0.2)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.3, 0.4, 0.6)
renderer.AddActor(actor)
renderer.AddActor(plane_actor)

# Shadow map pass pipeline
shadows = vtkShadowMapPass()
seq = vtkSequencePass()
passes = vtkRenderPassCollection()
passes.AddItem(shadows.GetShadowMapBakerPass())
passes.AddItem(shadows)
seq.SetPasses(passes)

camera_pass = vtkCameraPass()
camera_pass.SetDelegatePass(seq)
renderer.SetPass(camera_pass)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("shadow map pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light_1)
renderer.AddLight(light_2)
renderer.AddLight(light_3)
renderer.GetActiveCamera().SetPosition(-0.2, 0.2, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().OrthogonalizeViewUp()
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(2.5)

interactor.Initialize()
interactor.Start()
