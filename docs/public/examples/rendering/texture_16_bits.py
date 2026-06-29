#!/usr/bin/env python

# Demonstrate 16-bit unsigned short texture rendering on a plane.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkUnsignedShortArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTexture,
)

# Procedural 16-bit texture
image = vtkImageData()
image.SetExtent(0, 256, 0, 256, 0, 0)

pixels = vtkUnsignedShortArray()
pixels.SetNumberOfComponents(3)
pixels.SetNumberOfTuples(65536)

for i in range(65536):
    v = i & 0xFFFF
    pixels.SetTuple3(i, v, 65535 - v, (32768 + v) & 0xFFFF)

image.GetPointData().SetScalars(pixels)

texture = vtkTexture()
texture.SetColorModeToDirectScalars()
texture.SetInputData(image)

# Plane with texture
plane = vtkPlaneSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(plane.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetTexture(texture)

renderer = vtkRenderer()
renderer.SetBackground(0.5, 0.5, 0.5)
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("texture 16 bits")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.3)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
