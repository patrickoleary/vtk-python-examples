#!/usr/bin/env python

# Test vtkGridAxesActor2D with a teapot model, outline, and axis labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor
from vtkmodules.vtkRenderingGridAxes import vtkGridAxesActor2D, vtkGridAxesHelper

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

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(normals.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)

# Camera
camera = vtkCamera()
camera.SetClippingRange(1.0, 100.0)
camera.SetFocalPoint(0.9, 1.0, 0.0)
camera.SetPosition(11.63, 6.0, 10.77)

# Light
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(8.3761, 4.94858, 4.12505)

# Grid axes (default face)
normals.Update()
bounds = normals.GetOutput().GetBounds()

axes = vtkGridAxesActor2D()
axes.SetGridBounds(bounds)
axes.GetProperty().SetFrontfaceCulling(True)

# X axis: red
axes.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes.GetLabelTextProperty(0).SetColor(0.8, 0.0, 0.0)
axes.SetTitle(0, "X-Axis")
axes.SetTitle(1, "Y-Axis")
axes.SetTitle(2, "Z-Axis")

# Y axis: green
axes.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes.GetLabelTextProperty(1).SetColor(0.0, 0.8, 0.0)


# Grid axes (MAX_ZX face)
axes_1 = vtkGridAxesActor2D()
axes_1.SetGridBounds(bounds)
axes_1.SetFace(vtkGridAxesHelper.MAX_ZX)
axes_1.GetProperty().SetFrontfaceCulling(False)

# X axis: red
axes_1.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes_1.GetLabelTextProperty(0).SetColor(0.8, 0.0, 0.0)
axes_1.SetTitle(0, "X-Axis")
axes_1.SetTitle(1, "Y-Axis")
axes_1.SetTitle(2, "Z-Axis")

# Y axis: green
axes_1.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes_1.GetLabelTextProperty(1).SetColor(0.0, 0.8, 0.0)


# Renderer
renderer = vtkRenderer()
renderer.SetActiveCamera(camera)
renderer.AddLight(light)
renderer.AddViewProp(actor)
renderer.AddViewProp(outline_actor)
renderer.AddViewProp(axes)
renderer.AddViewProp(axes_1)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("grid axes actor2d")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
