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

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(skybox)

# Actors: five rows of six spheres, each row a different material
row_params = [
    (0.0, white, 1.0),   # row 0: white metallic
    (1.0, brass, 1.0),   # row 1: brass metallic
    (2.0, black, 0.0),   # row 2: black dielectric
    (3.0, cyan, 0.0),    # row 3: cyan dielectric
    (4.0, red, 0.0),     # row 4: red dielectric
]

for y, color, metallic in row_params:
    for i in range(6):
        actor = vtkActor()
        actor.SetPosition(i, y, 0.0)
        actor.SetMapper(mapper)
        actor.GetProperty().SetInterpolationToPBR()
        actor.GetProperty().SetColor(color)
        actor.GetProperty().SetMetallic(metallic)
        actor.GetProperty().SetRoughness(i / 5.0)
        renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PBR_Materials")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
