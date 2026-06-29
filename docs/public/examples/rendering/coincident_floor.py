#!/usr/bin/env python

# Demonstrate skybox floor projection with coincident polygonal geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkJPEGReader
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkSkybox,
    vtkTexture,
)

# Data paths
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Lights
light = vtkLight()
light.SetLightTypeToSceneLight()
light.SetPosition(1.0, 7.0, 1.0)

head_light = vtkLight()
head_light.SetLightTypeToHeadlight()
head_light.SetColor(1.0, 0.8, 1.0)
head_light.SetIntensity(0.5)

# Floor texture
jpg_reader = vtkJPEGReader()
jpg_reader.SetFileName(os.path.join(data_dir, "beach.jpg"))

texture = vtkTexture()
texture.InterpolateOn()
texture.RepeatOn()
texture.MipmapOn()
texture.SetInputConnection(jpg_reader.GetOutputPort())

# Bunny mesh
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "bunny.ply"))

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(reader.GetOutputPort())

actor = vtkActor()
actor.SetPosition(0, -0.2, 0)
actor.SetScale(6.0, 6.0, 6.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetSpecularPower(20)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.4)
actor.GetProperty().SetAmbientColor(0.4, 0.0, 1.0)
actor.SetMapper(mapper)

# Ground plane
plane = vtkPlaneSource()
plane.SetOrigin(-0.5, 0.0, -0.5)
plane.SetPoint1(0.5, 0.0, -0.5)
plane.SetPoint2(-0.5, 0.0, 0.5)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)
plane_actor.GetProperty().SetColor(0.5, 0.23, 0.45)

# Skybox floor
floor = vtkSkybox()
floor.SetFloorPlane(0, 1, 0, 0.0)
floor.SetFloorRight(0, 0, 1)
floor.SetFloorTexCoordScale(1.2, 0.9)
floor.SetProjectionToFloor()
floor.SetTexture(texture)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(plane_actor)
renderer.AddActor(floor)
renderer.SetBackground(0.6, 0.7, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("coincident floor")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)
renderer.AddLight(head_light)
renderer.GetActiveCamera().SetPosition(0.0, 0.55, 3.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.55, 0.0)

interactor.Initialize()
interactor.Start()
