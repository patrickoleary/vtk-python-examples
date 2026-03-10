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

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(skybox)

# Row 0: full anisotropy, increasing roughness
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 0.0, 0.0)
    actor.RotateX(20)
    actor.RotateY(20)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(white)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetAnisotropy(1.0)
    actor.GetProperty().SetRoughness(i / 5.0)
    renderer.AddActor(actor)

# Row 1: low roughness, increasing anisotropy
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 1.0, 0.0)
    actor.RotateX(20)
    actor.RotateY(20)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(white)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetRoughness(0.1)
    actor.GetProperty().SetAnisotropy(i / 5.0)
    renderer.AddActor(actor)

# Row 2: full anisotropy, low roughness, increasing anisotropy rotation
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 2.0, 0.0)
    actor.RotateX(20)
    actor.RotateY(20)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(white)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetRoughness(0.1)
    actor.GetProperty().SetAnisotropy(1.0)
    actor.GetProperty().SetAnisotropyRotation(i / 5.0)
    renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PBR_Anisotropy")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
