#!/usr/bin/env python
# Demonstrate vtkSphericalTransform mapping a plane to a sphere with earth texture.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkSphericalTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

data_dir = os.path.join(os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__))), "data")

# Plane source in spherical coordinates.
plane = vtkPlaneSource()
plane.SetOrigin(1.0, 3.14159265359 - 0.0001, 0.0)
plane.SetPoint1(1.0, 3.14159265359 - 0.0001, 6.28318530719)
plane.SetPoint2(1.0, 0.0001, 0.0)
plane.SetXResolution(19)
plane.SetYResolution(9)

# Spherical transform: forward, inverse, forward.
transform = vtkSphericalTransform()

tpoly = vtkTransformPolyDataFilter()
tpoly.SetInputConnection(plane.GetOutputPort())
tpoly.SetTransform(transform)

tpoly_2 = vtkTransformPolyDataFilter()
tpoly_2.SetInputConnection(tpoly.GetOutputPort())
tpoly_2.SetTransform(transform.GetInverse())

tpoly_3 = vtkTransformPolyDataFilter()
tpoly_3.SetInputConnection(tpoly_2.GetOutputPort())
tpoly_3.SetTransform(transform)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(tpoly_3.GetOutputPort())

# Earth texture.
earth_reader = vtkPNMReader()
earth_reader.SetFileName(os.path.join(data_dir, "earth.ppm"))

texture = vtkTexture()
texture.SetInputConnection(earth_reader.GetOutputPort())
texture.InterpolateOn()

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("spherical")

renderer.GetActiveCamera().SetPosition(8, -10, 6)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewAngle(15)
renderer.GetActiveCamera().SetViewUp(0.0, 0.0, 1.0)
renderer.GetActiveCamera().Zoom(1.4)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
