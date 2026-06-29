#!/usr/bin/env python

# Test vtkGridAxesActor3D with a teapot model and axis labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor
from vtkmodules.vtkRenderingGridAxes import vtkGridAxesActor3D

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Read teapot geometry
reader = vtkBYUReader()
reader.SetGeometryFileName(os.path.join(data_dir, "teapot.g"))

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(reader.GetOutputPort())

# Mapper and actor for teapot
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())

actor = vtkLODActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(0.7, 0.3, 0.0)

# Camera
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
camera.SetFocalPoint(0.9, 1.0, 0.0)
camera.SetPosition(11.63, 6.0, 10.77)

# Light
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(8.3761, 4.94858, 4.12505)

# Grid axes
normals.Update()
axes = vtkGridAxesActor3D()
axes.SetGridBounds(normals.GetOutput().GetBounds())
axes.GetProperty().SetFrontfaceCulling(True)

# X axis: red
axes.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes.GetLabelTextProperty(0).SetColor(0.8, 0.0, 0.0)
axes.SetTitle(0, "X-Axis")
axes.SetTitle(1, "Y-Axis")
axes.SetTitle(2, "Z-Axis")
axes.SetLabelUniqueEdgesOnly(True)

# Y axis: green
axes.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes.GetLabelTextProperty(1).SetColor(0.0, 0.8, 0.0)


# Renderer
renderer = vtkRenderer()
renderer.SetActiveCamera(camera)
renderer.AddLight(light)
renderer.AddViewProp(actor)
renderer.AddViewProp(axes)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("grid axes actor3d")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
