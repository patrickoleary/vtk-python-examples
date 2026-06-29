#!/usr/bin/env python

# Test vtkPolarAxesActor in default configuration with a teapot model.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingAnnotation import vtkPolarAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
teapot_reader = vtkBYUReader()
teapot_reader.SetGeometryFileName(os.path.join(data_dir, "teapot.g"))

# Filter
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(teapot_reader.GetOutputPort())

teapot_mapper = vtkPolyDataMapper()
teapot_mapper.SetInputConnection(normals_filter.GetOutputPort())

teapot_actor = vtkActor()
teapot_actor.SetMapper(teapot_mapper)
teapot_actor.GetProperty().SetDiffuseColor(0.5, 0.8, 0.3)

outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(normals_filter.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1.0, 1.0, 1.0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)

normals_filter.Update()

# Polar axes (default — just set pole position)
polar_axes = vtkPolarAxesActor()
polar_axes.SetPole(0.5, 1.0, 3.0)
polar_axes.SetBounds(normals_filter.GetOutput().GetBounds())

renderer.AddViewProp(teapot_actor)
renderer.AddViewProp(outline_actor)
renderer.AddViewProp(polar_axes)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polar axes default")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(7.0, 7.0, 4.0)
renderer.AddLight(light)

renderer.GetActiveCamera().SetClippingRange(1.0, 100.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.5, 0.0)
renderer.GetActiveCamera().SetPosition(5.0, 6.0, 14.0)
polar_axes.SetCamera(renderer.GetActiveCamera())

# First render then zoom
render_window.Render()
polar_axes.GetCamera().Zoom(3)

interactor.Initialize()
interactor.Start()
