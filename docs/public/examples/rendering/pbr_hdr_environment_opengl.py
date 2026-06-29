#!/usr/bin/env python

# Demonstrate PBR rendering with HDR environment lighting and a skybox.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkHDRReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# HDR environment texture
reader = vtkHDRReader()
reader.SetFileName(os.path.join(data_dir, "spiaggia_di_mondello_1k.hdr"))
texture = vtkTexture()
texture.SetColorModeToDirectScalars()
texture.MipmapOn()
texture.InterpolateOn()
texture.SetInputConnection(reader.GetOutputPort())

# Skybox
skybox = vtkSkybox()
skybox.SetFloorRight(0.0, 0.0, 1.0)
skybox.SetProjectionToSphere()
skybox.SetTexture(texture)

# Sphere source
sphere = vtkSphereSource()
sphere.SetThetaResolution(75)
sphere.SetPhiResolution(75)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Six metallic spheres with varying roughness
actor_0 = vtkActor()
actor_0.SetPosition(0, 0.0, 0.0)
actor_0.SetMapper(mapper)
actor_0.GetProperty().SetInterpolationToPBR()
actor_0.GetProperty().SetMetallic(1.0)
actor_0.GetProperty().SetRoughness(0.0)

actor_1 = vtkActor()
actor_1.SetPosition(1, 0.0, 0.0)
actor_1.SetMapper(mapper)
actor_1.GetProperty().SetInterpolationToPBR()
actor_1.GetProperty().SetMetallic(1.0)
actor_1.GetProperty().SetRoughness(0.2)

actor_2 = vtkActor()
actor_2.SetPosition(2, 0.0, 0.0)
actor_2.SetMapper(mapper)
actor_2.GetProperty().SetInterpolationToPBR()
actor_2.GetProperty().SetMetallic(1.0)
actor_2.GetProperty().SetRoughness(0.4)

actor_3 = vtkActor()
actor_3.SetPosition(3, 0.0, 0.0)
actor_3.SetMapper(mapper)
actor_3.GetProperty().SetInterpolationToPBR()
actor_3.GetProperty().SetMetallic(1.0)
actor_3.GetProperty().SetRoughness(0.6)

actor_4 = vtkActor()
actor_4.SetPosition(4, 0.0, 0.0)
actor_4.SetMapper(mapper)
actor_4.GetProperty().SetInterpolationToPBR()
actor_4.GetProperty().SetMetallic(1.0)
actor_4.GetProperty().SetRoughness(0.8)

actor_5 = vtkActor()
actor_5.SetPosition(5, 0.0, 0.0)
actor_5.SetMapper(mapper)
actor_5.GetProperty().SetInterpolationToPBR()
actor_5.GetProperty().SetMetallic(1.0)
actor_5.GetProperty().SetRoughness(1.0)

# Renderer with IBL
renderer = vtkRenderer()
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.AddActor(skybox)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr hdr environment opengl")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
