#!/usr/bin/env python

# Demonstrate normal mapping on a plane with a normal map texture.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataTangents, vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkPNGReader
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
light.SetPosition(0.5, 0.5, 1.0)
light.SetFocalPoint(0.0, 0.0, 0.0)

# Plane with tangents for normal mapping
plane = vtkPlaneSource()
triangulation = vtkTriangleFilter()
triangulation.SetInputConnection(plane.GetOutputPort())
tangents = vtkPolyDataTangents()
tangents.SetInputConnection(triangulation.GetOutputPort())

# Normal map texture
png = vtkPNGReader()
png.SetFileName(os.path.join(data_dir, "normalMapping.png"))
texture = vtkTexture()
texture.SetInputConnection(png.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tangents.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetNormalTexture(texture)

renderer = vtkRenderer()
renderer.AutomaticLightCreationOff()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("normal mapping")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.AddLight(light)

interactor.Initialize()
interactor.Start()
