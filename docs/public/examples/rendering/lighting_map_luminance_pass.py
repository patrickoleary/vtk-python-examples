#!/usr/bin/env python

# Demonstrate lighting map luminance render pass on a dragon mesh.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

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
    vtkLightingMapPass,
    vtkRenderPassCollection,
    vtkSequencePass,
)

# Read dragon mesh
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
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

# Positional light
light = vtkLight()
light.SetLightTypeToSceneLight()
light.SetPosition(0.0, 0.0, 1.0)
light.SetPositional(True)
light.SetFocalPoint(0.0, 0.0, 0.0)
light.SetIntensity(1.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Lighting map luminance pass pipeline
lighting_pass = vtkLightingMapPass()
lighting_pass.SetRenderType(vtkLightingMapPass.LUMINANCE)

passes = vtkRenderPassCollection()
passes.AddItem(lighting_pass)

sequence = vtkSequencePass()
sequence.SetPasses(passes)

camera_pass = vtkCameraPass()
camera_pass.SetDelegatePass(sequence)
renderer.SetPass(camera_pass)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("lighting map luminance pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)

interactor.Initialize()
interactor.Start()
