#!/usr/bin/env python

# Render five rows of PBR spheres demonstrating coat material properties.
# Row 0: brass metallic, smooth, increasing coat roughness.
# Row 1: brass metallic, rough, increasing coat roughness.
# Row 2: white metallic, smooth, red coat, increasing coat strength.
# Row 3: white dielectric, smooth, red coat rough, increasing coat strength.
# Row 4: dark teal dielectric, increasing base IOR.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
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
brass = (0.722, 0.451, 0.200)
dark_teal = (0.0, 0.502, 0.302)
red = (1.0, 0.0, 0.0)
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

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(75)
sphere.SetPhiResolution(75)

# Mapper: shared mapper for all spheres
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(skybox)

# Row 0: brass metallic, smooth base, increasing coat roughness
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 0.0, 0.0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(brass)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetRoughness(0.1)
    actor.GetProperty().SetCoatStrength(1.0)
    actor.GetProperty().SetCoatRoughness(i / 5.0)
    renderer.AddActor(actor)

# Row 1: brass metallic, rough base, increasing coat roughness
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 1.0, 0.0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(brass)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetRoughness(1.0)
    actor.GetProperty().SetCoatStrength(1.0)
    actor.GetProperty().SetCoatRoughness(i / 5.0)
    renderer.AddActor(actor)

# Row 2: white metallic, smooth base, red coat smooth, increasing coat strength
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 2.0, 0.0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(white)
    actor.GetProperty().SetMetallic(1.0)
    actor.GetProperty().SetRoughness(0.1)
    actor.GetProperty().SetCoatColor(red)
    actor.GetProperty().SetCoatRoughness(0.1)
    actor.GetProperty().SetCoatStrength(i / 5.0)
    renderer.AddActor(actor)

# Row 3: white dielectric, smooth base, red coat rough, increasing coat strength
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 3.0, 0.0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(white)
    actor.GetProperty().SetRoughness(0.1)
    actor.GetProperty().SetCoatColor(red)
    actor.GetProperty().SetCoatRoughness(1.0)
    actor.GetProperty().SetCoatStrength(i / 5.0)
    renderer.AddActor(actor)

# Row 4: dark teal dielectric, increasing base IOR
for i in range(6):
    actor = vtkActor()
    actor.SetPosition(i, 4.0, 0.0)
    actor.SetMapper(mapper)
    actor.GetProperty().SetInterpolationToPBR()
    actor.GetProperty().SetColor(dark_teal)
    actor.GetProperty().SetBaseIOR(1.0 + i / 3.0)
    renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PBR_Materials_Coat")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
