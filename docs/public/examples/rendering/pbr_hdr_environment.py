#!/usr/bin/env python

# Render a row of metallic spheres with increasing roughness using
# physically based rendering and an HDR equirectangular environment
# map for image-based lighting with a skybox backdrop.

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

# Actor 0: roughness 0.0
actor_0 = vtkActor()
actor_0.SetPosition(0, 0.0, 0.0)
actor_0.SetMapper(mapper)
actor_0.GetProperty().SetInterpolationToPBR()
actor_0.GetProperty().SetColor(white)
actor_0.GetProperty().SetMetallic(1.0)
actor_0.GetProperty().SetRoughness(0.0)

# Actor 1: roughness 0.2
actor_1 = vtkActor()
actor_1.SetPosition(1, 0.0, 0.0)
actor_1.SetMapper(mapper)
actor_1.GetProperty().SetInterpolationToPBR()
actor_1.GetProperty().SetColor(white)
actor_1.GetProperty().SetMetallic(1.0)
actor_1.GetProperty().SetRoughness(0.2)

# Actor 2: roughness 0.4
actor_2 = vtkActor()
actor_2.SetPosition(2, 0.0, 0.0)
actor_2.SetMapper(mapper)
actor_2.GetProperty().SetInterpolationToPBR()
actor_2.GetProperty().SetColor(white)
actor_2.GetProperty().SetMetallic(1.0)
actor_2.GetProperty().SetRoughness(0.4)

# Actor 3: roughness 0.6
actor_3 = vtkActor()
actor_3.SetPosition(3, 0.0, 0.0)
actor_3.SetMapper(mapper)
actor_3.GetProperty().SetInterpolationToPBR()
actor_3.GetProperty().SetColor(white)
actor_3.GetProperty().SetMetallic(1.0)
actor_3.GetProperty().SetRoughness(0.6)

# Actor 4: roughness 0.8
actor_4 = vtkActor()
actor_4.SetPosition(4, 0.0, 0.0)
actor_4.SetMapper(mapper)
actor_4.GetProperty().SetInterpolationToPBR()
actor_4.GetProperty().SetColor(white)
actor_4.GetProperty().SetMetallic(1.0)
actor_4.GetProperty().SetRoughness(0.8)

# Actor 5: roughness 1.0
actor_5 = vtkActor()
actor_5.SetPosition(5, 0.0, 0.0)
actor_5.SetMapper(mapper)
actor_5.GetProperty().SetInterpolationToPBR()
actor_5.GetProperty().SetColor(white)
actor_5.GetProperty().SetMetallic(1.0)
actor_5.GetProperty().SetRoughness(1.0)

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(skybox)
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr hdr environment")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
