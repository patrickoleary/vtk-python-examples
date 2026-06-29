#!/usr/bin/env python

# Test actor rotation methods with a cow model.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read cow
cow = vtkBYUReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

cow.SetGeometryFileName(os.path.join(data_dir, "cow.g"))

cow_mapper = vtkPolyDataMapper()
cow_mapper.SetInputConnection(cow.GetOutputPort())

cow_actor = vtkActor()
cow_actor.SetMapper(cow_mapper)
cow_actor.GetProperty().SetDiffuseColor(0.9608, 0.8706, 0.7020)

# Axes
cow_axes_source = vtkAxes()
cow_axes_source.SetScaleFactor(10)
cow_axes_source.SetOrigin(0, 0, 0)

cow_axes_mapper = vtkPolyDataMapper()
cow_axes_mapper.SetInputConnection(cow_axes_source.GetOutputPort())

cow_axes = vtkActor()
cow_axes.SetMapper(cow_axes_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cow_axes)
renderer.AddActor(cow_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("rotations basic")
render_window.SetMultiSamples(0)
render_window.SetSize(320, 240)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(0)
renderer.GetActiveCamera().Dolly(1.4)
renderer.ResetCameraClippingRange()

cow_axes.VisibilityOn()
render_window.Render()

# Perform rotations
# RotateX
cow_actor.SetOrientation(0, 0, 0)
renderer.ResetCameraClippingRange()
render_window.Render()
render_window.EraseOff()
for i in range(6):
    cow_actor.RotateX(60)
    render_window.Render()
render_window.EraseOn()

# RotateY
cow_actor.SetOrientation(0, 0, 0)
renderer.ResetCameraClippingRange()
render_window.Render()
render_window.EraseOff()
for i in range(6):
    cow_actor.RotateY(60)
    render_window.Render()
render_window.EraseOn()

# RotateZ
cow_actor.SetOrientation(0, 0, 0)
renderer.ResetCameraClippingRange()
render_window.Render()
render_window.EraseOff()
for i in range(6):
    cow_actor.RotateZ(60)
    render_window.Render()
render_window.EraseOn()

# RotateXY
cow_actor.SetOrientation(0, 0, 0)
cow_actor.RotateX(60)
renderer.ResetCameraClippingRange()
render_window.Render()
render_window.EraseOff()
for i in range(6):
    cow_actor.RotateY(60)
    render_window.Render()
render_window.EraseOn()

render_window.EraseOff()
render_window.Render()
interactor.Initialize()
interactor.Start()
