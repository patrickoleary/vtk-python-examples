#!/usr/bin/env python

# Demonstrate sRGB color space comparison with two viewports and positional lights.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkJPEGReader
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

# Shared image reader and plane source
img_reader = vtkJPEGReader()
img_reader.SetFileName(os.path.join(data_dir, "skybox", "posz.jpg"))

plane = vtkPlaneSource()

# Viewport 0: sRGB on (left)
light_0_r = vtkLight()
light_0_r.SetLightTypeToSceneLight()
light_0_r.SetPosition(-1.73, -1.0, 2.0)
light_0_r.PositionalOn()
light_0_r.SetConeAngle(90)
light_0_r.SetAttenuationValues(0, 1.0, 0)
light_0_r.SetColor(4, 0, 0)
light_0_r.SetExponent(0)

light_0_g = vtkLight()
light_0_g.SetLightTypeToSceneLight()
light_0_g.SetPosition(1.73, -1.0, 2.0)
light_0_g.PositionalOn()
light_0_g.SetConeAngle(90)
light_0_g.SetAttenuationValues(0, 0, 1.0)
light_0_g.SetColor(0, 6, 0)
light_0_g.SetExponent(0)

light_0_b = vtkLight()
light_0_b.SetLightTypeToSceneLight()
light_0_b.SetPosition(0.0, 2.0, 2.0)
light_0_b.PositionalOn()
light_0_b.SetConeAngle(50)
light_0_b.SetColor(0, 0, 4)
light_0_b.SetAttenuationValues(1.0, 0.0, 0.0)
light_0_b.SetExponent(0)

texture_0 = vtkTexture()
texture_0.InterpolateOn()
texture_0.RepeatOff()
texture_0.EdgeClampOn()
texture_0.SetUseSRGBColorSpace(True)
texture_0.SetInputConnection(img_reader.GetOutputPort())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(plane.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetScale(6.0, 6.0, 6.0)
actor_0.GetProperty().SetSpecular(0.2)
actor_0.GetProperty().SetSpecularPower(20)
actor_0.GetProperty().SetDiffuse(0.9)
actor_0.GetProperty().SetAmbient(0.2)
actor_0.SetTexture(texture_0)
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.SetBackground(0.3, 0.3, 0.3)
renderer_0.AddActor(actor_0)

# Viewport 1: sRGB off (right)
light_1_r = vtkLight()
light_1_r.SetLightTypeToSceneLight()
light_1_r.SetPosition(-1.73, -1.0, 2.0)
light_1_r.PositionalOn()
light_1_r.SetConeAngle(90)
light_1_r.SetAttenuationValues(0, 1.0, 0)
light_1_r.SetColor(4, 0, 0)
light_1_r.SetExponent(0)

light_1_g = vtkLight()
light_1_g.SetLightTypeToSceneLight()
light_1_g.SetPosition(1.73, -1.0, 2.0)
light_1_g.PositionalOn()
light_1_g.SetConeAngle(90)
light_1_g.SetAttenuationValues(0, 0, 1.0)
light_1_g.SetColor(0, 6, 0)
light_1_g.SetExponent(0)

light_1_b = vtkLight()
light_1_b.SetLightTypeToSceneLight()
light_1_b.SetPosition(0.0, 2.0, 2.0)
light_1_b.PositionalOn()
light_1_b.SetConeAngle(50)
light_1_b.SetColor(0, 0, 4)
light_1_b.SetAttenuationValues(1.0, 0.0, 0.0)
light_1_b.SetExponent(0)

texture_1 = vtkTexture()
texture_1.InterpolateOn()
texture_1.RepeatOff()
texture_1.EdgeClampOn()
texture_1.SetUseSRGBColorSpace(False)
texture_1.SetInputConnection(img_reader.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(plane.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetScale(6.0, 6.0, 6.0)
actor_1.GetProperty().SetSpecular(0.2)
actor_1.GetProperty().SetSpecularPower(20)
actor_1.GetProperty().SetDiffuse(0.9)
actor_1.GetProperty().SetAmbient(0.2)
actor_1.SetTexture(texture_1)
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.SetBackground(0.3, 0.3, 0.3)
renderer_1.AddActor(actor_1)

render_window = vtkRenderWindow()
render_window.SetSize(800, 400)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("srgb")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.AddLight(light_0_r)
renderer_0.AddLight(light_0_g)
renderer_0.AddLight(light_0_b)
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Zoom(1.3)
renderer_0.ResetCameraClippingRange()

renderer_1.AddLight(light_1_r)
renderer_1.AddLight(light_1_g)
renderer_1.AddLight(light_1_b)
renderer_1.ResetCamera()
renderer_1.GetActiveCamera().Zoom(1.3)
renderer_1.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
