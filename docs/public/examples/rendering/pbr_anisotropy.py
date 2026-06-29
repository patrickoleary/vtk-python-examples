#!/usr/bin/env python

# Render three rows of PBR spheres demonstrating anisotropic reflections.
# Row 0: full anisotropy with increasing roughness.
# Row 1: low roughness with increasing anisotropy.
# Row 2: full anisotropy, low roughness, increasing anisotropy rotation.
# Tangents are generated via spherical texture-coordinate mapping.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataTangents
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkFiltersTexture import vtkTextureMapToSphere
from vtkmodules.vtkIOImage import vtkHDRReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkSkybox,
    vtkTexture,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLRenderer

# Colors (normalized RGB)
white = (1.0, 1.0, 1.0)
black = (0.0, 0.0, 0.0)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Environment texture: load equirectangular HDR for image-based lighting
hdr_reader = vtkHDRReader()
hdr_reader.SetFileName(str(data_dir / "Skyboxes" / "spiaggia_di_mondello_4k.hdr"))

env_texture = vtkTexture()
env_texture.SetColorModeToDirectScalars()
env_texture.SetInputConnection(hdr_reader.GetOutputPort())
env_texture.MipmapOn()
env_texture.InterpolateOn()

# Skybox: spherical projection of the HDR environment
skybox = vtkSkybox()
skybox.SetFloorRight(0, 0, 1)
skybox.SetProjection(vtkSkybox.Sphere)
skybox.SetTexture(env_texture)
skybox.GammaCorrectOn()

# Source: high-resolution sphere with spherical texture coordinates and tangents
sphere = vtkSphereSource()
sphere.SetThetaResolution(75)
sphere.SetPhiResolution(75)

texture_map = vtkTextureMapToSphere()
texture_map.SetInputConnection(sphere.GetOutputPort())
texture_map.PreventSeamOff()

tangents = vtkPolyDataTangents()
tangents.SetInputConnection(texture_map.GetOutputPort())

# Mapper: shared mapper with tangent data for anisotropy direction
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tangents.GetOutputPort())

# Row 0: full anisotropy, increasing roughness
actor_r0_0 = vtkActor()
actor_r0_0.SetPosition(0, 0.0, 0.0)
actor_r0_0.RotateX(20)
actor_r0_0.RotateY(20)
actor_r0_0.SetMapper(mapper)
actor_r0_0.GetProperty().SetInterpolationToPBR()
actor_r0_0.GetProperty().SetColor(white)
actor_r0_0.GetProperty().SetMetallic(1.0)
actor_r0_0.GetProperty().SetAnisotropy(1.0)
actor_r0_0.GetProperty().SetRoughness(0.0)

actor_r0_1 = vtkActor()
actor_r0_1.SetPosition(1, 0.0, 0.0)
actor_r0_1.RotateX(20)
actor_r0_1.RotateY(20)
actor_r0_1.SetMapper(mapper)
actor_r0_1.GetProperty().SetInterpolationToPBR()
actor_r0_1.GetProperty().SetColor(white)
actor_r0_1.GetProperty().SetMetallic(1.0)
actor_r0_1.GetProperty().SetAnisotropy(1.0)
actor_r0_1.GetProperty().SetRoughness(0.2)

actor_r0_2 = vtkActor()
actor_r0_2.SetPosition(2, 0.0, 0.0)
actor_r0_2.RotateX(20)
actor_r0_2.RotateY(20)
actor_r0_2.SetMapper(mapper)
actor_r0_2.GetProperty().SetInterpolationToPBR()
actor_r0_2.GetProperty().SetColor(white)
actor_r0_2.GetProperty().SetMetallic(1.0)
actor_r0_2.GetProperty().SetAnisotropy(1.0)
actor_r0_2.GetProperty().SetRoughness(0.4)

actor_r0_3 = vtkActor()
actor_r0_3.SetPosition(3, 0.0, 0.0)
actor_r0_3.RotateX(20)
actor_r0_3.RotateY(20)
actor_r0_3.SetMapper(mapper)
actor_r0_3.GetProperty().SetInterpolationToPBR()
actor_r0_3.GetProperty().SetColor(white)
actor_r0_3.GetProperty().SetMetallic(1.0)
actor_r0_3.GetProperty().SetAnisotropy(1.0)
actor_r0_3.GetProperty().SetRoughness(0.6)

actor_r0_4 = vtkActor()
actor_r0_4.SetPosition(4, 0.0, 0.0)
actor_r0_4.RotateX(20)
actor_r0_4.RotateY(20)
actor_r0_4.SetMapper(mapper)
actor_r0_4.GetProperty().SetInterpolationToPBR()
actor_r0_4.GetProperty().SetColor(white)
actor_r0_4.GetProperty().SetMetallic(1.0)
actor_r0_4.GetProperty().SetAnisotropy(1.0)
actor_r0_4.GetProperty().SetRoughness(0.8)

actor_r0_5 = vtkActor()
actor_r0_5.SetPosition(5, 0.0, 0.0)
actor_r0_5.RotateX(20)
actor_r0_5.RotateY(20)
actor_r0_5.SetMapper(mapper)
actor_r0_5.GetProperty().SetInterpolationToPBR()
actor_r0_5.GetProperty().SetColor(white)
actor_r0_5.GetProperty().SetMetallic(1.0)
actor_r0_5.GetProperty().SetAnisotropy(1.0)
actor_r0_5.GetProperty().SetRoughness(1.0)

# Row 1: low roughness, increasing anisotropy
actor_r1_0 = vtkActor()
actor_r1_0.SetPosition(0, 1.0, 0.0)
actor_r1_0.RotateX(20)
actor_r1_0.RotateY(20)
actor_r1_0.SetMapper(mapper)
actor_r1_0.GetProperty().SetInterpolationToPBR()
actor_r1_0.GetProperty().SetColor(white)
actor_r1_0.GetProperty().SetMetallic(1.0)
actor_r1_0.GetProperty().SetRoughness(0.1)
actor_r1_0.GetProperty().SetAnisotropy(0.0)

actor_r1_1 = vtkActor()
actor_r1_1.SetPosition(1, 1.0, 0.0)
actor_r1_1.RotateX(20)
actor_r1_1.RotateY(20)
actor_r1_1.SetMapper(mapper)
actor_r1_1.GetProperty().SetInterpolationToPBR()
actor_r1_1.GetProperty().SetColor(white)
actor_r1_1.GetProperty().SetMetallic(1.0)
actor_r1_1.GetProperty().SetRoughness(0.1)
actor_r1_1.GetProperty().SetAnisotropy(0.2)

actor_r1_2 = vtkActor()
actor_r1_2.SetPosition(2, 1.0, 0.0)
actor_r1_2.RotateX(20)
actor_r1_2.RotateY(20)
actor_r1_2.SetMapper(mapper)
actor_r1_2.GetProperty().SetInterpolationToPBR()
actor_r1_2.GetProperty().SetColor(white)
actor_r1_2.GetProperty().SetMetallic(1.0)
actor_r1_2.GetProperty().SetRoughness(0.1)
actor_r1_2.GetProperty().SetAnisotropy(0.4)

actor_r1_3 = vtkActor()
actor_r1_3.SetPosition(3, 1.0, 0.0)
actor_r1_3.RotateX(20)
actor_r1_3.RotateY(20)
actor_r1_3.SetMapper(mapper)
actor_r1_3.GetProperty().SetInterpolationToPBR()
actor_r1_3.GetProperty().SetColor(white)
actor_r1_3.GetProperty().SetMetallic(1.0)
actor_r1_3.GetProperty().SetRoughness(0.1)
actor_r1_3.GetProperty().SetAnisotropy(0.6)

actor_r1_4 = vtkActor()
actor_r1_4.SetPosition(4, 1.0, 0.0)
actor_r1_4.RotateX(20)
actor_r1_4.RotateY(20)
actor_r1_4.SetMapper(mapper)
actor_r1_4.GetProperty().SetInterpolationToPBR()
actor_r1_4.GetProperty().SetColor(white)
actor_r1_4.GetProperty().SetMetallic(1.0)
actor_r1_4.GetProperty().SetRoughness(0.1)
actor_r1_4.GetProperty().SetAnisotropy(0.8)

actor_r1_5 = vtkActor()
actor_r1_5.SetPosition(5, 1.0, 0.0)
actor_r1_5.RotateX(20)
actor_r1_5.RotateY(20)
actor_r1_5.SetMapper(mapper)
actor_r1_5.GetProperty().SetInterpolationToPBR()
actor_r1_5.GetProperty().SetColor(white)
actor_r1_5.GetProperty().SetMetallic(1.0)
actor_r1_5.GetProperty().SetRoughness(0.1)
actor_r1_5.GetProperty().SetAnisotropy(1.0)

# Row 2: full anisotropy, low roughness, increasing anisotropy rotation
actor_r2_0 = vtkActor()
actor_r2_0.SetPosition(0, 2.0, 0.0)
actor_r2_0.RotateX(20)
actor_r2_0.RotateY(20)
actor_r2_0.SetMapper(mapper)
actor_r2_0.GetProperty().SetInterpolationToPBR()
actor_r2_0.GetProperty().SetColor(white)
actor_r2_0.GetProperty().SetMetallic(1.0)
actor_r2_0.GetProperty().SetRoughness(0.1)
actor_r2_0.GetProperty().SetAnisotropy(1.0)
actor_r2_0.GetProperty().SetAnisotropyRotation(0.0)

actor_r2_1 = vtkActor()
actor_r2_1.SetPosition(1, 2.0, 0.0)
actor_r2_1.RotateX(20)
actor_r2_1.RotateY(20)
actor_r2_1.SetMapper(mapper)
actor_r2_1.GetProperty().SetInterpolationToPBR()
actor_r2_1.GetProperty().SetColor(white)
actor_r2_1.GetProperty().SetMetallic(1.0)
actor_r2_1.GetProperty().SetRoughness(0.1)
actor_r2_1.GetProperty().SetAnisotropy(1.0)
actor_r2_1.GetProperty().SetAnisotropyRotation(0.2)

actor_r2_2 = vtkActor()
actor_r2_2.SetPosition(2, 2.0, 0.0)
actor_r2_2.RotateX(20)
actor_r2_2.RotateY(20)
actor_r2_2.SetMapper(mapper)
actor_r2_2.GetProperty().SetInterpolationToPBR()
actor_r2_2.GetProperty().SetColor(white)
actor_r2_2.GetProperty().SetMetallic(1.0)
actor_r2_2.GetProperty().SetRoughness(0.1)
actor_r2_2.GetProperty().SetAnisotropy(1.0)
actor_r2_2.GetProperty().SetAnisotropyRotation(0.4)

actor_r2_3 = vtkActor()
actor_r2_3.SetPosition(3, 2.0, 0.0)
actor_r2_3.RotateX(20)
actor_r2_3.RotateY(20)
actor_r2_3.SetMapper(mapper)
actor_r2_3.GetProperty().SetInterpolationToPBR()
actor_r2_3.GetProperty().SetColor(white)
actor_r2_3.GetProperty().SetMetallic(1.0)
actor_r2_3.GetProperty().SetRoughness(0.1)
actor_r2_3.GetProperty().SetAnisotropy(1.0)
actor_r2_3.GetProperty().SetAnisotropyRotation(0.6)

actor_r2_4 = vtkActor()
actor_r2_4.SetPosition(4, 2.0, 0.0)
actor_r2_4.RotateX(20)
actor_r2_4.RotateY(20)
actor_r2_4.SetMapper(mapper)
actor_r2_4.GetProperty().SetInterpolationToPBR()
actor_r2_4.GetProperty().SetColor(white)
actor_r2_4.GetProperty().SetMetallic(1.0)
actor_r2_4.GetProperty().SetRoughness(0.1)
actor_r2_4.GetProperty().SetAnisotropy(1.0)
actor_r2_4.GetProperty().SetAnisotropyRotation(0.8)

actor_r2_5 = vtkActor()
actor_r2_5.SetPosition(5, 2.0, 0.0)
actor_r2_5.RotateX(20)
actor_r2_5.RotateY(20)
actor_r2_5.SetMapper(mapper)
actor_r2_5.GetProperty().SetInterpolationToPBR()
actor_r2_5.GetProperty().SetColor(white)
actor_r2_5.GetProperty().SetMetallic(1.0)
actor_r2_5.GetProperty().SetRoughness(0.1)
actor_r2_5.GetProperty().SetAnisotropy(1.0)
actor_r2_5.GetProperty().SetAnisotropyRotation(1.0)

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(skybox)
renderer.AddActor(actor_r0_0)
renderer.AddActor(actor_r0_1)
renderer.AddActor(actor_r0_2)
renderer.AddActor(actor_r0_3)
renderer.AddActor(actor_r0_4)
renderer.AddActor(actor_r0_5)
renderer.AddActor(actor_r1_0)
renderer.AddActor(actor_r1_1)
renderer.AddActor(actor_r1_2)
renderer.AddActor(actor_r1_3)
renderer.AddActor(actor_r1_4)
renderer.AddActor(actor_r1_5)
renderer.AddActor(actor_r2_0)
renderer.AddActor(actor_r2_1)
renderer.AddActor(actor_r2_2)
renderer.AddActor(actor_r2_3)
renderer.AddActor(actor_r2_4)
renderer.AddActor(actor_r2_5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr anisotropy")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
