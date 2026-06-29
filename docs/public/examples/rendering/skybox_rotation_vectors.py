#!/usr/bin/env python

# Demonstrate skybox rotation using environment up and right vectors with HDR IBL.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkHDRReader
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

# HDR environment texture
reader = vtkHDRReader()
reader.SetFileName(os.path.join(data_dir, "spiaggia_di_mondello_1k.hdr"))
texture = vtkTexture()
texture.SetColorModeToDirectScalars()
texture.MipmapOn()
texture.InterpolateOn()
texture.SetInputConnection(reader.GetOutputPort())

# Skybox
skybox = vtkSkybox()
skybox.SetProjectionToSphere()
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

# Renderer with IBL and custom environment vectors
renderer = vtkRenderer()
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.SetEnvironmentUp(0, 0, 1)
renderer.SetEnvironmentRight(1, 0, 0)
renderer.AddActor(skybox)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("skybox rotation vectors")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
