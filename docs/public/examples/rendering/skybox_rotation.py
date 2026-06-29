#!/usr/bin/env python

# Demonstrate skybox rotation using an HDR environment with a rotation matrix.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonMath import vtkMatrix3x3
from vtkmodules.vtkCommonTransforms import vtkTransform
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

# Build rotation matrix from transform
transform = vtkTransform()
transform.Identity()
transform.RotateX(25)
transform.RotateY(10)
transform.RotateZ(-90)

mat4 = transform.GetMatrix()
rot_mat = vtkMatrix3x3()
for i in range(3):
    for j in range(3):
        rot_mat.SetElement(i, j, mat4.GetElement(i, j))

# Skybox
skybox = vtkSkybox()
skybox.SetFloorRight(0.0, 0.0, 1.0)
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

# Renderer with rotated IBL
renderer = vtkRenderer()
renderer.SetEnvironmentRotationMatrix(rot_mat)
renderer.UseImageBasedLightingOn()
renderer.SetEnvironmentTexture(texture)
renderer.AddActor(skybox)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("skybox rotation")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
