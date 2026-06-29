#!/usr/bin/env python

# Render five rows of PBR spheres with different materials and increasing
# roughness.  Row 0: white metallic, row 1: brass metallic, row 2: black
# dielectric, row 3: cyan dielectric, row 4: red dielectric.  An HDR
# equirectangular environment map provides image-based lighting and a skybox.

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
black = (0.0, 0.0, 0.0)
cyan = (0.0, 1.0, 1.0)
red = (1.0, 0.0, 0.0)

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
sphere.SetThetaResolution(100)
sphere.SetPhiResolution(100)

# Mapper: shared mapper for all spheres
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Row 0: white metallic, roughness 0.0 to 1.0
actor_r0_0 = vtkActor()
actor_r0_0.SetPosition(0, 0.0, 0.0)
actor_r0_0.SetMapper(mapper)
actor_r0_0.GetProperty().SetInterpolationToPBR()
actor_r0_0.GetProperty().SetColor(white)
actor_r0_0.GetProperty().SetMetallic(1.0)
actor_r0_0.GetProperty().SetRoughness(0.0)

actor_r0_1 = vtkActor()
actor_r0_1.SetPosition(1, 0.0, 0.0)
actor_r0_1.SetMapper(mapper)
actor_r0_1.GetProperty().SetInterpolationToPBR()
actor_r0_1.GetProperty().SetColor(white)
actor_r0_1.GetProperty().SetMetallic(1.0)
actor_r0_1.GetProperty().SetRoughness(0.2)

actor_r0_2 = vtkActor()
actor_r0_2.SetPosition(2, 0.0, 0.0)
actor_r0_2.SetMapper(mapper)
actor_r0_2.GetProperty().SetInterpolationToPBR()
actor_r0_2.GetProperty().SetColor(white)
actor_r0_2.GetProperty().SetMetallic(1.0)
actor_r0_2.GetProperty().SetRoughness(0.4)

actor_r0_3 = vtkActor()
actor_r0_3.SetPosition(3, 0.0, 0.0)
actor_r0_3.SetMapper(mapper)
actor_r0_3.GetProperty().SetInterpolationToPBR()
actor_r0_3.GetProperty().SetColor(white)
actor_r0_3.GetProperty().SetMetallic(1.0)
actor_r0_3.GetProperty().SetRoughness(0.6)

actor_r0_4 = vtkActor()
actor_r0_4.SetPosition(4, 0.0, 0.0)
actor_r0_4.SetMapper(mapper)
actor_r0_4.GetProperty().SetInterpolationToPBR()
actor_r0_4.GetProperty().SetColor(white)
actor_r0_4.GetProperty().SetMetallic(1.0)
actor_r0_4.GetProperty().SetRoughness(0.8)

actor_r0_5 = vtkActor()
actor_r0_5.SetPosition(5, 0.0, 0.0)
actor_r0_5.SetMapper(mapper)
actor_r0_5.GetProperty().SetInterpolationToPBR()
actor_r0_5.GetProperty().SetColor(white)
actor_r0_5.GetProperty().SetMetallic(1.0)
actor_r0_5.GetProperty().SetRoughness(1.0)

# Row 1: brass metallic, roughness 0.0 to 1.0
actor_r1_0 = vtkActor()
actor_r1_0.SetPosition(0, 1.0, 0.0)
actor_r1_0.SetMapper(mapper)
actor_r1_0.GetProperty().SetInterpolationToPBR()
actor_r1_0.GetProperty().SetColor(brass)
actor_r1_0.GetProperty().SetMetallic(1.0)
actor_r1_0.GetProperty().SetRoughness(0.0)

actor_r1_1 = vtkActor()
actor_r1_1.SetPosition(1, 1.0, 0.0)
actor_r1_1.SetMapper(mapper)
actor_r1_1.GetProperty().SetInterpolationToPBR()
actor_r1_1.GetProperty().SetColor(brass)
actor_r1_1.GetProperty().SetMetallic(1.0)
actor_r1_1.GetProperty().SetRoughness(0.2)

actor_r1_2 = vtkActor()
actor_r1_2.SetPosition(2, 1.0, 0.0)
actor_r1_2.SetMapper(mapper)
actor_r1_2.GetProperty().SetInterpolationToPBR()
actor_r1_2.GetProperty().SetColor(brass)
actor_r1_2.GetProperty().SetMetallic(1.0)
actor_r1_2.GetProperty().SetRoughness(0.4)

actor_r1_3 = vtkActor()
actor_r1_3.SetPosition(3, 1.0, 0.0)
actor_r1_3.SetMapper(mapper)
actor_r1_3.GetProperty().SetInterpolationToPBR()
actor_r1_3.GetProperty().SetColor(brass)
actor_r1_3.GetProperty().SetMetallic(1.0)
actor_r1_3.GetProperty().SetRoughness(0.6)

actor_r1_4 = vtkActor()
actor_r1_4.SetPosition(4, 1.0, 0.0)
actor_r1_4.SetMapper(mapper)
actor_r1_4.GetProperty().SetInterpolationToPBR()
actor_r1_4.GetProperty().SetColor(brass)
actor_r1_4.GetProperty().SetMetallic(1.0)
actor_r1_4.GetProperty().SetRoughness(0.8)

actor_r1_5 = vtkActor()
actor_r1_5.SetPosition(5, 1.0, 0.0)
actor_r1_5.SetMapper(mapper)
actor_r1_5.GetProperty().SetInterpolationToPBR()
actor_r1_5.GetProperty().SetColor(brass)
actor_r1_5.GetProperty().SetMetallic(1.0)
actor_r1_5.GetProperty().SetRoughness(1.0)

# Row 2: black dielectric, roughness 0.0 to 1.0
actor_r2_0 = vtkActor()
actor_r2_0.SetPosition(0, 2.0, 0.0)
actor_r2_0.SetMapper(mapper)
actor_r2_0.GetProperty().SetInterpolationToPBR()
actor_r2_0.GetProperty().SetColor(black)
actor_r2_0.GetProperty().SetMetallic(0.0)
actor_r2_0.GetProperty().SetRoughness(0.0)

actor_r2_1 = vtkActor()
actor_r2_1.SetPosition(1, 2.0, 0.0)
actor_r2_1.SetMapper(mapper)
actor_r2_1.GetProperty().SetInterpolationToPBR()
actor_r2_1.GetProperty().SetColor(black)
actor_r2_1.GetProperty().SetMetallic(0.0)
actor_r2_1.GetProperty().SetRoughness(0.2)

actor_r2_2 = vtkActor()
actor_r2_2.SetPosition(2, 2.0, 0.0)
actor_r2_2.SetMapper(mapper)
actor_r2_2.GetProperty().SetInterpolationToPBR()
actor_r2_2.GetProperty().SetColor(black)
actor_r2_2.GetProperty().SetMetallic(0.0)
actor_r2_2.GetProperty().SetRoughness(0.4)

actor_r2_3 = vtkActor()
actor_r2_3.SetPosition(3, 2.0, 0.0)
actor_r2_3.SetMapper(mapper)
actor_r2_3.GetProperty().SetInterpolationToPBR()
actor_r2_3.GetProperty().SetColor(black)
actor_r2_3.GetProperty().SetMetallic(0.0)
actor_r2_3.GetProperty().SetRoughness(0.6)

actor_r2_4 = vtkActor()
actor_r2_4.SetPosition(4, 2.0, 0.0)
actor_r2_4.SetMapper(mapper)
actor_r2_4.GetProperty().SetInterpolationToPBR()
actor_r2_4.GetProperty().SetColor(black)
actor_r2_4.GetProperty().SetMetallic(0.0)
actor_r2_4.GetProperty().SetRoughness(0.8)

actor_r2_5 = vtkActor()
actor_r2_5.SetPosition(5, 2.0, 0.0)
actor_r2_5.SetMapper(mapper)
actor_r2_5.GetProperty().SetInterpolationToPBR()
actor_r2_5.GetProperty().SetColor(black)
actor_r2_5.GetProperty().SetMetallic(0.0)
actor_r2_5.GetProperty().SetRoughness(1.0)

# Row 3: cyan dielectric, roughness 0.0 to 1.0
actor_r3_0 = vtkActor()
actor_r3_0.SetPosition(0, 3.0, 0.0)
actor_r3_0.SetMapper(mapper)
actor_r3_0.GetProperty().SetInterpolationToPBR()
actor_r3_0.GetProperty().SetColor(cyan)
actor_r3_0.GetProperty().SetMetallic(0.0)
actor_r3_0.GetProperty().SetRoughness(0.0)

actor_r3_1 = vtkActor()
actor_r3_1.SetPosition(1, 3.0, 0.0)
actor_r3_1.SetMapper(mapper)
actor_r3_1.GetProperty().SetInterpolationToPBR()
actor_r3_1.GetProperty().SetColor(cyan)
actor_r3_1.GetProperty().SetMetallic(0.0)
actor_r3_1.GetProperty().SetRoughness(0.2)

actor_r3_2 = vtkActor()
actor_r3_2.SetPosition(2, 3.0, 0.0)
actor_r3_2.SetMapper(mapper)
actor_r3_2.GetProperty().SetInterpolationToPBR()
actor_r3_2.GetProperty().SetColor(cyan)
actor_r3_2.GetProperty().SetMetallic(0.0)
actor_r3_2.GetProperty().SetRoughness(0.4)

actor_r3_3 = vtkActor()
actor_r3_3.SetPosition(3, 3.0, 0.0)
actor_r3_3.SetMapper(mapper)
actor_r3_3.GetProperty().SetInterpolationToPBR()
actor_r3_3.GetProperty().SetColor(cyan)
actor_r3_3.GetProperty().SetMetallic(0.0)
actor_r3_3.GetProperty().SetRoughness(0.6)

actor_r3_4 = vtkActor()
actor_r3_4.SetPosition(4, 3.0, 0.0)
actor_r3_4.SetMapper(mapper)
actor_r3_4.GetProperty().SetInterpolationToPBR()
actor_r3_4.GetProperty().SetColor(cyan)
actor_r3_4.GetProperty().SetMetallic(0.0)
actor_r3_4.GetProperty().SetRoughness(0.8)

actor_r3_5 = vtkActor()
actor_r3_5.SetPosition(5, 3.0, 0.0)
actor_r3_5.SetMapper(mapper)
actor_r3_5.GetProperty().SetInterpolationToPBR()
actor_r3_5.GetProperty().SetColor(cyan)
actor_r3_5.GetProperty().SetMetallic(0.0)
actor_r3_5.GetProperty().SetRoughness(1.0)

# Row 4: red dielectric, roughness 0.0 to 1.0
actor_r4_0 = vtkActor()
actor_r4_0.SetPosition(0, 4.0, 0.0)
actor_r4_0.SetMapper(mapper)
actor_r4_0.GetProperty().SetInterpolationToPBR()
actor_r4_0.GetProperty().SetColor(red)
actor_r4_0.GetProperty().SetMetallic(0.0)
actor_r4_0.GetProperty().SetRoughness(0.0)

actor_r4_1 = vtkActor()
actor_r4_1.SetPosition(1, 4.0, 0.0)
actor_r4_1.SetMapper(mapper)
actor_r4_1.GetProperty().SetInterpolationToPBR()
actor_r4_1.GetProperty().SetColor(red)
actor_r4_1.GetProperty().SetMetallic(0.0)
actor_r4_1.GetProperty().SetRoughness(0.2)

actor_r4_2 = vtkActor()
actor_r4_2.SetPosition(2, 4.0, 0.0)
actor_r4_2.SetMapper(mapper)
actor_r4_2.GetProperty().SetInterpolationToPBR()
actor_r4_2.GetProperty().SetColor(red)
actor_r4_2.GetProperty().SetMetallic(0.0)
actor_r4_2.GetProperty().SetRoughness(0.4)

actor_r4_3 = vtkActor()
actor_r4_3.SetPosition(3, 4.0, 0.0)
actor_r4_3.SetMapper(mapper)
actor_r4_3.GetProperty().SetInterpolationToPBR()
actor_r4_3.GetProperty().SetColor(red)
actor_r4_3.GetProperty().SetMetallic(0.0)
actor_r4_3.GetProperty().SetRoughness(0.6)

actor_r4_4 = vtkActor()
actor_r4_4.SetPosition(4, 4.0, 0.0)
actor_r4_4.SetMapper(mapper)
actor_r4_4.GetProperty().SetInterpolationToPBR()
actor_r4_4.GetProperty().SetColor(red)
actor_r4_4.GetProperty().SetMetallic(0.0)
actor_r4_4.GetProperty().SetRoughness(0.8)

actor_r4_5 = vtkActor()
actor_r4_5.SetPosition(5, 4.0, 0.0)
actor_r4_5.SetMapper(mapper)
actor_r4_5.GetProperty().SetInterpolationToPBR()
actor_r4_5.GetProperty().SetColor(red)
actor_r4_5.GetProperty().SetMetallic(0.0)
actor_r4_5.GetProperty().SetRoughness(1.0)

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
renderer.AddActor(actor_r3_0)
renderer.AddActor(actor_r3_1)
renderer.AddActor(actor_r3_2)
renderer.AddActor(actor_r3_3)
renderer.AddActor(actor_r3_4)
renderer.AddActor(actor_r3_5)
renderer.AddActor(actor_r4_0)
renderer.AddActor(actor_r4_1)
renderer.AddActor(actor_r4_2)
renderer.AddActor(actor_r4_3)
renderer.AddActor(actor_r4_4)
renderer.AddActor(actor_r4_5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr materials")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
