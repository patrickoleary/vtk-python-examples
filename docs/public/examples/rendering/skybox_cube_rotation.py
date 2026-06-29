#!/usr/bin/env python

# Demonstrate skybox cube map rotation with a PBR metallic sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkImagingCore import vtkImageFlip
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Cubemap texture from separate face images
texture = vtkTexture()
texture.CubeMapOn()

jpg_px = vtkJPEGReader()
jpg_px.SetFileName(os.path.join(data_dir, "skybox-px.jpg"))
flip_px = vtkImageFlip()
flip_px.SetInputConnection(jpg_px.GetOutputPort())
flip_px.SetFilteredAxis(1)
texture.SetInputConnection(0, flip_px.GetOutputPort())

jpg_nx = vtkJPEGReader()
jpg_nx.SetFileName(os.path.join(data_dir, "skybox-nx.jpg"))
flip_nx = vtkImageFlip()
flip_nx.SetInputConnection(jpg_nx.GetOutputPort())
flip_nx.SetFilteredAxis(1)
texture.SetInputConnection(1, flip_nx.GetOutputPort())

jpg_py = vtkJPEGReader()
jpg_py.SetFileName(os.path.join(data_dir, "skybox-py.jpg"))
flip_py = vtkImageFlip()
flip_py.SetInputConnection(jpg_py.GetOutputPort())
flip_py.SetFilteredAxis(1)
texture.SetInputConnection(2, flip_py.GetOutputPort())

jpg_ny = vtkJPEGReader()
jpg_ny.SetFileName(os.path.join(data_dir, "skybox-ny.jpg"))
flip_ny = vtkImageFlip()
flip_ny.SetInputConnection(jpg_ny.GetOutputPort())
flip_ny.SetFilteredAxis(1)
texture.SetInputConnection(3, flip_ny.GetOutputPort())

jpg_pz = vtkJPEGReader()
jpg_pz.SetFileName(os.path.join(data_dir, "skybox-pz.jpg"))
flip_pz = vtkImageFlip()
flip_pz.SetInputConnection(jpg_pz.GetOutputPort())
flip_pz.SetFilteredAxis(1)
texture.SetInputConnection(4, flip_pz.GetOutputPort())

jpg_nz = vtkJPEGReader()
jpg_nz.SetFileName(os.path.join(data_dir, "skybox-nz.jpg"))
flip_nz = vtkImageFlip()
flip_nz.SetInputConnection(jpg_nz.GetOutputPort())
flip_nz.SetFilteredAxis(1)
texture.SetInputConnection(5, flip_nz.GetOutputPort())

# Skybox
skybox = vtkSkybox()
skybox.SetTexture(texture)

# PBR metallic sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(75)
sphere.SetPhiResolution(75)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToPBR()
actor.GetProperty().SetMetallic(1.0)
actor.GetProperty().SetRoughness(0.3)

# Renderer with IBL
renderer = vtkRenderer()
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.AddActor(skybox)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("skybox cube rotation")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.SetEnvironmentRight(0, 0, 1)
renderer.SetEnvironmentUp(0, 1, 0)

interactor.Initialize()
interactor.Start()
