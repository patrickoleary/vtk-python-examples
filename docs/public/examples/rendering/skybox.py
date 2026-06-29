#!/usr/bin/env python
# Demonstrate vtkSkybox with HDR environment texture and PBR spheres.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

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
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLSkybox

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Skybox with HDR texture.
skybox = vtkOpenGLSkybox()

hdr_reader = vtkHDRReader()
hdr_reader.SetFileName(os.path.join(data_dir, "spiaggia_di_mondello_1k.hdr"))

texture = vtkTexture()
texture.SetColorModeToDirectScalars()
texture.MipmapOn()
texture.InterpolateOn()
texture.SetInputConnection(hdr_reader.GetOutputPort())

skybox.SetFloorRight(0.0, 0.0, 1.0)
skybox.SetProjection(vtkSkybox.Sphere)
skybox.SetTexture(texture)

# PBR spheres with varying roughness.
sphere = vtkSphereSource()
sphere.SetThetaResolution(75)
sphere.SetPhiResolution(75)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor_0 = vtkActor()
sphere_actor_0.SetPosition(0, 0.0, 0.0)
sphere_actor_0.SetMapper(sphere_mapper)
sphere_actor_0.GetProperty().SetInterpolationToPBR()
sphere_actor_0.GetProperty().SetMetallic(1.0)
sphere_actor_0.GetProperty().SetRoughness(0.0)

sphere_actor_1 = vtkActor()
sphere_actor_1.SetPosition(1, 0.0, 0.0)
sphere_actor_1.SetMapper(sphere_mapper)
sphere_actor_1.GetProperty().SetInterpolationToPBR()
sphere_actor_1.GetProperty().SetMetallic(1.0)
sphere_actor_1.GetProperty().SetRoughness(0.2)

sphere_actor_2 = vtkActor()
sphere_actor_2.SetPosition(2, 0.0, 0.0)
sphere_actor_2.SetMapper(sphere_mapper)
sphere_actor_2.GetProperty().SetInterpolationToPBR()
sphere_actor_2.GetProperty().SetMetallic(1.0)
sphere_actor_2.GetProperty().SetRoughness(0.4)

sphere_actor_3 = vtkActor()
sphere_actor_3.SetPosition(3, 0.0, 0.0)
sphere_actor_3.SetMapper(sphere_mapper)
sphere_actor_3.GetProperty().SetInterpolationToPBR()
sphere_actor_3.GetProperty().SetMetallic(1.0)
sphere_actor_3.GetProperty().SetRoughness(0.6)

sphere_actor_4 = vtkActor()
sphere_actor_4.SetPosition(4, 0.0, 0.0)
sphere_actor_4.SetMapper(sphere_mapper)
sphere_actor_4.GetProperty().SetInterpolationToPBR()
sphere_actor_4.GetProperty().SetMetallic(1.0)
sphere_actor_4.GetProperty().SetRoughness(0.8)

sphere_actor_5 = vtkActor()
sphere_actor_5.SetPosition(5, 0.0, 0.0)
sphere_actor_5.SetMapper(sphere_mapper)
sphere_actor_5.GetProperty().SetInterpolationToPBR()
sphere_actor_5.GetProperty().SetMetallic(1.0)
sphere_actor_5.GetProperty().SetRoughness(1.0)

# Renderer
renderer = vtkRenderer()
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.AddActor(skybox)
renderer.AddActor(sphere_actor_0)
renderer.AddActor(sphere_actor_1)
renderer.AddActor(sphere_actor_2)
renderer.AddActor(sphere_actor_3)
renderer.AddActor(sphere_actor_4)
renderer.AddActor(sphere_actor_5)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("skybox")
render_window.SetMultiSamples(0)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
