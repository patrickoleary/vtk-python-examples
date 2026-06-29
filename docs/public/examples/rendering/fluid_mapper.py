#!/usr/bin/env python

# Demonstrate vtkOpenGLFluidMapper with a grid of particles, dragon model, and skybox IBL.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkImagingCore import vtkImageFlip
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
    vtkVolume,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkOpenGLFluidMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.0)
renderer.GetEnvMapIrradiance().SetIrradianceStep(0.3)

# Dragon model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "dragon.ply"))
reader.Update()

dragon_mapper = vtkPolyDataMapper()
dragon_mapper.SetInputConnection(reader.GetOutputPort())

dragon = vtkActor()
dragon.SetMapper(dragon_mapper)
dragon.SetScale(20, 20, 20)
dragon.SetPosition(2, -0.5, 3)
dragon.GetProperty().SetDiffuseColor(0.780392, 0.568627, 0.113725)
dragon.GetProperty().SetSpecular(1.0)
dragon.GetProperty().SetSpecularPower(80.0)
dragon.GetProperty().SetDiffuse(0.7)
renderer.AddActor(dragon)

# Cubemap environment
cubemap = vtkTexture()
cubemap.CubeMapOn()
cubemap.UseSRGBColorSpaceOn()

# Face 0: +X
jpg_px = vtkJPEGReader()
jpg_px.SetFileName(os.path.join(data_dir, "skybox", "posx.jpg"))
flip_px = vtkImageFlip()
flip_px.SetInputConnection(jpg_px.GetOutputPort())
flip_px.SetFilteredAxis(1)
cubemap.SetInputConnection(0, flip_px.GetOutputPort())

# Face 1: -X
jpg_nx = vtkJPEGReader()
jpg_nx.SetFileName(os.path.join(data_dir, "skybox", "negx.jpg"))
flip_nx = vtkImageFlip()
flip_nx.SetInputConnection(jpg_nx.GetOutputPort())
flip_nx.SetFilteredAxis(1)
cubemap.SetInputConnection(1, flip_nx.GetOutputPort())

# Face 2: +Y
jpg_py = vtkJPEGReader()
jpg_py.SetFileName(os.path.join(data_dir, "skybox", "posy.jpg"))
flip_py = vtkImageFlip()
flip_py.SetInputConnection(jpg_py.GetOutputPort())
flip_py.SetFilteredAxis(1)
cubemap.SetInputConnection(2, flip_py.GetOutputPort())

# Face 3: -Y
jpg_ny = vtkJPEGReader()
jpg_ny.SetFileName(os.path.join(data_dir, "skybox", "negy.jpg"))
flip_ny = vtkImageFlip()
flip_ny.SetInputConnection(jpg_ny.GetOutputPort())
flip_ny.SetFilteredAxis(1)
cubemap.SetInputConnection(3, flip_ny.GetOutputPort())

# Face 4: +Z
jpg_pz = vtkJPEGReader()
jpg_pz.SetFileName(os.path.join(data_dir, "skybox", "posz.jpg"))
flip_pz = vtkImageFlip()
flip_pz.SetInputConnection(jpg_pz.GetOutputPort())
flip_pz.SetFilteredAxis(1)
cubemap.SetInputConnection(4, flip_pz.GetOutputPort())

# Face 5: -Z
jpg_nz = vtkJPEGReader()
jpg_nz.SetFileName(os.path.join(data_dir, "skybox", "negz.jpg"))
flip_nz = vtkImageFlip()
flip_nz.SetInputConnection(jpg_nz.GetOutputPort())
flip_nz.SetFilteredAxis(1)
cubemap.SetInputConnection(5, flip_nz.GetOutputPort())

renderer.SetEnvironmentTexture(cubemap)
renderer.UseImageBasedLightingOn()

skybox = vtkSkybox()
skybox.SetTexture(cubemap)
renderer.AddActor(skybox)

# Grid-textured ground plane
grid = vtkImageGridSource()
grid.SetGridSpacing(32, 32, 0)
grid.SetLineValue(0.2)
grid.SetFillValue(1.0)

lut = vtkLookupTable()
lut.SetSaturationRange(0.0, 0.0)
lut.SetValueRange(0.0, 1.0)
lut.SetTableRange(0.0, 1.0)
lut.Build()

grid_texture = vtkTexture()
grid_texture.SetColorModeToMapScalars()
grid_texture.SetLookupTable(lut)
grid_texture.InterpolateOn()
grid_texture.RepeatOn()
grid_texture.MipmapOn()
grid_texture.SetInputConnection(grid.GetOutputPort(0))
grid_texture.UseSRGBColorSpaceOn()

plane = vtkPlaneSource()
plane.SetNormal(0.0, -1.0, 0.0)
plane.SetOrigin(-15.0, 0.0, -15.0)
plane.SetPoint1(15, 0, -15)
plane.SetPoint2(-15, 0, 15)
plane.Update()

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

textured_plane = vtkActor()
textured_plane.SetMapper(plane_mapper)
textured_plane.GetProperty().SetBaseColorTexture(grid_texture)
textured_plane.GetProperty().SetInterpolationToPBR()
textured_plane.GetProperty().SetMetallic(0.2)
textured_plane.GetProperty().SetRoughness(0.1)
renderer.AddActor(textured_plane)

# Particle data for fluid
points = vtkPoints()
spacing = 0.1
for z in range(50):
    for y in range(15):
        for x in range(50):
            points.InsertNextPoint(x * spacing, y * spacing, z * spacing)

point_data = vtkPolyData()
point_data.SetPoints(points)

# Fluid mapper
fluid_mapper = vtkOpenGLFluidMapper()
fluid_mapper.SetInputData(point_data)
fluid_mapper.SetParticleRadius(0.03 * 3.0)
fluid_mapper.SetSurfaceFilterIterations(3)
fluid_mapper.SetSurfaceFilterRadius(5)
fluid_mapper.SetSurfaceFilterMethod(vtkOpenGLFluidMapper.NarrowRange)
fluid_mapper.SetDisplayMode(vtkOpenGLFluidMapper.TransparentFluidVolume)
fluid_mapper.SetAttenuationColor(0.8, 0.2, 0.15)
fluid_mapper.SetAttenuationScale(1.0)
fluid_mapper.SetOpaqueColor(0.0, 0.0, 0.9)
fluid_mapper.SetParticleColorPower(0.1)
fluid_mapper.SetParticleColorScale(0.57)
fluid_mapper.SetAdditionalReflection(0.0)
fluid_mapper.SetRefractiveIndex(1.33)
fluid_mapper.SetRefractionScale(0.07)

vol = vtkVolume()
vol.SetMapper(fluid_mapper)
renderer.AddVolume(vol)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.UseSRGBColorSpaceOn()
render_window.AddRenderer(renderer)
render_window.SetWindowName("fluid mapper")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetPosition(10, 2, 20)
renderer.GetActiveCamera().SetFocalPoint(1, 1, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().SetViewAngle(40.0)
renderer.GetActiveCamera().Dolly(1.7)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
