#!/usr/bin/env python

# Test opacity with depth peeling using property, LUT, and texture opacity.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkTexturedSphereSource,
)
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Cone with property opacity
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetOpacity(0.5)

# Cone with LUT opacity
elevation = vtkElevationFilter()
elevation.SetInputConnection(cone.GetOutputPort())

cone_mapper_2 = vtkPolyDataMapper()
cone_mapper_2.SetInputConnection(elevation.GetOutputPort())

lut = vtkLookupTable()
lut.SetAlphaRange(0.9, 0.1)
lut.SetHueRange(0, 0)
lut.SetSaturationRange(1, 1)
lut.SetValueRange(1, 1)

cone_mapper_2.SetLookupTable(lut)
cone_mapper_2.SetScalarModeToUsePointData()
cone_mapper_2.SetScalarVisibility(1)
cone_mapper_2.InterpolateScalarsBeforeMappingOn()

cone_actor_lut = vtkActor()
cone_actor_lut.SetMapper(cone_mapper_2)
cone_actor_lut.SetPosition(0.1, 1.0, 0)
cone_actor_lut.GetProperty().SetOpacity(0.99)

# Sphere with texture opacity
png_reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

png_reader.SetFileName(os.path.join(data_dir, "alphachannel.png"))
png_reader.Update()

sphere = vtkTexturedSphereSource()

texture = vtkTexture()
texture.SetInputConnection(png_reader.GetOutputPort())

cone_mapper_3 = vtkPolyDataMapper()
cone_mapper_3.SetInputConnection(sphere.GetOutputPort())

cone_actor_texture = vtkActor()
cone_actor_texture.SetTexture(texture)
cone_actor_texture.SetMapper(cone_mapper_3)
cone_actor_texture.SetPosition(0, -1.0, 0)
cone_actor_texture.GetProperty().SetColor(0.5, 0.5, 1)
cone_actor_texture.GetProperty().SetOpacity(0.99)

# Renderer with depth peeling
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.AddActor(cone_actor_lut)
renderer.AddActor(cone_actor_texture)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.SetUseDepthPeeling(1)
renderer.SetMaximumNumberOfPeels(20)
renderer.SetOcclusionRatio(0.002)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("opacity depth peeling")
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
style = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(style)

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(9, -1, 3)
camera.SetViewAngle(30)
camera.SetViewUp(0.05, 0.96, 0.24)
camera.SetFocalPoint(0, 0.25, 0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
