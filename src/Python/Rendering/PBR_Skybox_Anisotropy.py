#!/usr/bin/env python

# Demonstrate physically based rendering with anisotropic texturing on Boy's
# parametric surface.  Carbon-fiber albedo, normal, ORM, and anisotropy-angle
# textures are applied.  An HDR equirectangular environment map provides
# image-based lighting and a skybox backdrop.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricBoy
from vtkmodules.vtkFiltersCore import vtkPolyDataTangents
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkIOImage import (
    vtkHDRReader,
    vtkPNGReader,
)
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
bkg_color = (0.102, 0.200, 0.400)

# Data directory
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
tex_dir = data_dir / "Textures" / "Anisotropic"

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

# Source: Boy's parametric surface with texture coordinates and tangents
boy = vtkParametricBoy()

boy_source = vtkParametricFunctionSource()
boy_source.SetUResolution(51)
boy_source.SetVResolution(51)
boy_source.GenerateTextureCoordinatesOn()
boy_source.SetParametricFunction(boy)

tangents = vtkPolyDataTangents()
tangents.SetInputConnection(boy_source.GetOutputPort())

# Mapper: map the tangent-enriched parametric surface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tangents.GetOutputPort())

# Texture: albedo (base color) — carbon fiber
albedo_reader = vtkPNGReader()
albedo_reader.SetFileName(str(tex_dir / "CarbonFiberAniso_albedo.png"))
albedo = vtkTexture()
albedo.UseSRGBColorSpaceOn()
albedo.InterpolateOn()
albedo.SetInputConnection(albedo_reader.GetOutputPort())

# Texture: ORM (occlusion, roughness, metallic) — carbon fiber
material_reader = vtkPNGReader()
material_reader.SetFileName(str(tex_dir / "CarbonFiberAniso_orm.png"))
material = vtkTexture()
material.InterpolateOn()
material.SetInputConnection(material_reader.GetOutputPort())

# Texture: normal map — carbon fiber
normal_reader = vtkPNGReader()
normal_reader.SetFileName(str(tex_dir / "CarbonFiberAniso_normal.png"))
normal = vtkTexture()
normal.InterpolateOn()
normal.SetInputConnection(normal_reader.GetOutputPort())

# Texture: anisotropy angle — carbon fiber
aniso_reader = vtkPNGReader()
aniso_reader.SetFileName(str(tex_dir / "CarbonFiberAniso_anisotropyAngle.png"))
anisotropy = vtkTexture()
anisotropy.InterpolateOn()
anisotropy.SetInputConnection(aniso_reader.GetOutputPort())

# Actor: PBR Boy's surface with anisotropic carbon-fiber textures
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToPBR()
actor.GetProperty().SetColor(white)
actor.GetProperty().SetMetallic(1.0)
actor.GetProperty().SetRoughness(1.0)
actor.GetProperty().SetAnisotropy(1.0)
actor.GetProperty().SetAnisotropyRotation(1.0)
actor.GetProperty().SetBaseColorTexture(albedo)
actor.GetProperty().SetORMTexture(material)
actor.GetProperty().SetNormalTexture(normal)
actor.GetProperty().SetAnisotropyTexture(anisotropy)

# Renderer: OpenGL renderer with image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(bkg_color)
renderer.AutomaticLightCreationOff()
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.AddActor(actor)
renderer.AddActor(skybox)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PBR_Skybox_Anisotropy")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
