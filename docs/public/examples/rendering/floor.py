#!/usr/bin/env python

# Demonstrate skybox floor projection with a bunny model and grid texture.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkIOPLY import vtkPLYReader
from vtkmodules.vtkImagingSources import vtkImageGridSource
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

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Scene light
light = vtkLight()
light.SetLightTypeToSceneLight()
light.SetPosition(1.0, 7.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.6, 0.7, 1.0)

# Read bunny model
reader = vtkPLYReader()
reader.SetFileName(os.path.join(data_dir, "bunny.ply"))

norms = vtkPolyDataNormals()
norms.SetInputConnection(reader.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(norms.GetOutputPort())

actor = vtkActor()
actor.SetPosition(0, 0, 0)
actor.SetScale(6.0, 6.0, 6.0)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetSpecularPower(20)
actor.GetProperty().SetDiffuse(0.7)
actor.GetProperty().SetAmbient(0.4)
actor.GetProperty().SetAmbientColor(0.4, 0.0, 1.0)
actor.SetMapper(mapper)
renderer.AddActor(actor)

# Grid texture for floor
grid = vtkImageGridSource()
grid.SetGridSpacing(32, 32, 0)

lut = vtkLookupTable()
lut.SetSaturationRange(0.0, 0.0)
lut.SetValueRange(0.0, 1.0)
lut.SetTableRange(0.0, 1.0)
lut.Build()

texture = vtkTexture()
texture.SetColorModeToMapScalars()
texture.SetLookupTable(lut)
texture.InterpolateOn()
texture.RepeatOn()
texture.MipmapOn()
texture.SetInputConnection(grid.GetOutputPort(0))

# Skybox as floor
floor = vtkSkybox()
floor.SetProjectionToFloor()
floor.SetTexture(texture)
renderer.AddActor(floor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("floor")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)
renderer.GetActiveCamera().SetPosition(0.0, 0.55, 2.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.55, 0.0)
renderer.GetActiveCamera().SetViewAngle(60.0)
renderer.GetActiveCamera().Zoom(1.1)
renderer.GetActiveCamera().Azimuth(0)
renderer.GetActiveCamera().Elevation(5)
renderer.GetActiveCamera().Roll(-10)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
