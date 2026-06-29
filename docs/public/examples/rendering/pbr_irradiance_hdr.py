#!/usr/bin/env python

# Demonstrate PBR rendering with HDR irradiance using spherical harmonics.

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

# PBR sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.GetProperty().SetInterpolationToPBR()
actor.GetProperty().SetRoughness(0.0)
actor.GetProperty().SetColor(0.7, 0.0, 0.2)
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.UseSphericalHarmonicsOn()
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pbr irradiance hdr")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
# Pipeline exception: render needed before camera zoom for PBR/IBL
render_window.Render()
renderer.GetActiveCamera().Zoom(1.6)

interactor.Initialize()
interactor.Start()
