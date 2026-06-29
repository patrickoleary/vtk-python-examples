#!/usr/bin/env python

# Demonstrate PBR texture mapping with albedo, ORM, normal, and anisotropy textures on a cube.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataTangents, vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkIOImage import vtkJPEGReader, vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageFlip
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Scene light
light = vtkLight()
light.SetPosition(2.0, 0.0, 2.0)
light.SetFocalPoint(0.0, 0.0, 0.0)

# Cubemap environment texture
cubemap = vtkTexture()
cubemap.CubeMapOn()
cubemap.UseSRGBColorSpaceOn()
cubemap.MipmapOn()
cubemap.InterpolateOn()

jpg_px = vtkJPEGReader()
jpg_px.SetFileName(os.path.join(data_dir, "skybox", "posx.jpg"))
flip_px = vtkImageFlip()
flip_px.SetInputConnection(jpg_px.GetOutputPort())
flip_px.SetFilteredAxis(1)
cubemap.SetInputConnection(0, flip_px.GetOutputPort())

jpg_nx = vtkJPEGReader()
jpg_nx.SetFileName(os.path.join(data_dir, "skybox", "negx.jpg"))
flip_nx = vtkImageFlip()
flip_nx.SetInputConnection(jpg_nx.GetOutputPort())
flip_nx.SetFilteredAxis(1)
cubemap.SetInputConnection(1, flip_nx.GetOutputPort())

jpg_py = vtkJPEGReader()
jpg_py.SetFileName(os.path.join(data_dir, "skybox", "posy.jpg"))
flip_py = vtkImageFlip()
flip_py.SetInputConnection(jpg_py.GetOutputPort())
flip_py.SetFilteredAxis(1)
cubemap.SetInputConnection(2, flip_py.GetOutputPort())

jpg_ny = vtkJPEGReader()
jpg_ny.SetFileName(os.path.join(data_dir, "skybox", "negy.jpg"))
flip_ny = vtkImageFlip()
flip_ny.SetInputConnection(jpg_ny.GetOutputPort())
flip_ny.SetFilteredAxis(1)
cubemap.SetInputConnection(3, flip_ny.GetOutputPort())

jpg_pz = vtkJPEGReader()
jpg_pz.SetFileName(os.path.join(data_dir, "skybox", "posz.jpg"))
flip_pz = vtkImageFlip()
flip_pz.SetInputConnection(jpg_pz.GetOutputPort())
flip_pz.SetFilteredAxis(1)
cubemap.SetInputConnection(4, flip_pz.GetOutputPort())

jpg_nz = vtkJPEGReader()
jpg_nz.SetFileName(os.path.join(data_dir, "skybox", "negz.jpg"))
flip_nz = vtkImageFlip()
flip_nz.SetInputConnection(jpg_nz.GetOutputPort())
flip_nz.SetFilteredAxis(1)
cubemap.SetInputConnection(5, flip_nz.GetOutputPort())

# Cube with tangents
cube = vtkCubeSource()
triangulation = vtkTriangleFilter()
triangulation.SetInputConnection(cube.GetOutputPort())
tangents = vtkPolyDataTangents()
tangents.SetInputConnection(triangulation.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tangents.GetOutputPort())

# ORM texture
material_reader = vtkPNGReader()
material_reader.SetFileName(os.path.join(data_dir, "vtk_Material.png"))
material = vtkTexture()
material.InterpolateOn()
material.SetInputConnection(material_reader.GetOutputPort())

# Albedo texture
albedo_reader = vtkPNGReader()
albedo_reader.SetFileName(os.path.join(data_dir, "vtk_Base_Color.png"))
albedo = vtkTexture()
albedo.UseSRGBColorSpaceOn()
albedo.InterpolateOn()
albedo.SetInputConnection(albedo_reader.GetOutputPort())

# Normal texture
normal_reader = vtkPNGReader()
normal_reader.SetFileName(os.path.join(data_dir, "vtk_Normal.png"))
normal = vtkTexture()
normal.InterpolateOn()
normal.SetInputConnection(normal_reader.GetOutputPort())

# Anisotropy texture
anisotropy_reader = vtkPNGReader()
anisotropy_reader.SetFileName(os.path.join(data_dir, "vtk_Anisotropy.png"))
anisotropy = vtkTexture()
anisotropy.InterpolateOn()
anisotropy.SetInputConnection(anisotropy_reader.GetOutputPort())

# PBR actor with full texture mapping
actor = vtkActor()
actor.SetOrientation(0.0, 25.0, 0.0)
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToPBR()
actor.GetProperty().SetMetallic(1.0)
actor.GetProperty().SetRoughness(1.0)
actor.GetProperty().SetAnisotropy(1.0)
actor.GetProperty().SetAnisotropyRotation(1.0)
actor.GetProperty().SetBaseColorTexture(albedo)
actor.GetProperty().SetORMTexture(material)
actor.GetProperty().SetNormalTexture(normal)
actor.GetProperty().SetAnisotropyTexture(anisotropy)

# Renderer with manual light and IBL
renderer = vtkRenderer()
renderer.AutomaticLightCreationOff()
renderer.UseSphericalHarmonicsOff()
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)
renderer.SetEnvironmentTexture(cubemap)
renderer.UseImageBasedLightingOn()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr mapping opengl")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)

# Pipeline exception: render needed before camera zoom for PBR/IBL
render_window.Render()
renderer.GetActiveCamera().Zoom(1.5)

interactor.Initialize()
interactor.Start()
