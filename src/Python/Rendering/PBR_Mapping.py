#!/usr/bin/env python

# Render a PBR cube with albedo, ORM (occlusion/roughness/metallic), normal,
# and anisotropy texture maps.  A single directional light and HDR
# equirectangular environment map provide image-based lighting with a skybox.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkPolyDataTangents,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkIOImage import (
    vtkHDRReader,
    vtkPNGReader,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
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
tex_dir = data_dir / "Textures" / "Isotropic"
aniso_dir = data_dir / "Textures" / "Anisotropic"

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

# Source: triangulated cube with tangent vectors for normal/anisotropy mapping
cube = vtkCubeSource()

triangulation = vtkTriangleFilter()
triangulation.SetInputConnection(cube.GetOutputPort())

tangents = vtkPolyDataTangents()
tangents.SetInputConnection(triangulation.GetOutputPort())

# Mapper: map the tangent-enriched cube geometry
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tangents.GetOutputPort())

# Texture: albedo (base color)
albedo_reader = vtkPNGReader()
albedo_reader.SetFileName(str(tex_dir / "vtk_Base_Color.png"))
albedo = vtkTexture()
albedo.UseSRGBColorSpaceOn()
albedo.InterpolateOn()
albedo.SetInputConnection(albedo_reader.GetOutputPort())

# Texture: ORM (occlusion, roughness, metallic)
material_reader = vtkPNGReader()
material_reader.SetFileName(str(tex_dir / "vtk_Material.png"))
material = vtkTexture()
material.InterpolateOn()
material.SetInputConnection(material_reader.GetOutputPort())

# Texture: normal map
normal_reader = vtkPNGReader()
normal_reader.SetFileName(str(tex_dir / "vtk_Normal.png"))
normal = vtkTexture()
normal.InterpolateOn()
normal.SetInputConnection(normal_reader.GetOutputPort())

# Texture: anisotropy direction
aniso_reader = vtkPNGReader()
aniso_reader.SetFileName(str(aniso_dir / "vtk_Anisotropy.png"))
anisotropy = vtkTexture()
anisotropy.InterpolateOn()
anisotropy.SetInputConnection(aniso_reader.GetOutputPort())

# Actor: PBR cube with all texture maps applied
actor = vtkActor()
actor.SetOrientation(0.0, 25.0, 0.0)
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

# Renderer: OpenGL renderer with explicit light and image-based lighting
renderer = vtkOpenGLRenderer()
renderer.SetBackground(black)
renderer.AutomaticLightCreationOff()
renderer.UseImageBasedLightingOn()
renderer.UseSphericalHarmonicsOn()
renderer.SetEnvironmentTexture(env_texture, False)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)

light = vtkLight()
light.SetPosition(2.0, 0.0, 2.0)
light.SetFocalPoint(0.0, 0.0, 0.0)
renderer.AddLight(light)

renderer.AddActor(actor)
renderer.AddActor(skybox)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("PBR_Mapping")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
renderer.GetActiveCamera().Zoom(1.5)
interactor.Start()
