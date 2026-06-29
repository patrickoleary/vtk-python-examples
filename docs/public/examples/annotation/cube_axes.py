#!/usr/bin/env python

# Demonstrate vtkCubeAxesActor2D with a teapot in two viewports.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
teapot_reader = vtkBYUReader()
teapot_reader.SetGeometryFileName(os.path.join(data_dir, "teapot.g"))

# Filter
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(teapot_reader.GetOutputPort())

teapot_mapper = vtkPolyDataMapper()
teapot_mapper.SetInputConnection(normals_filter.GetOutputPort())

teapot_actor = vtkLODActor()
teapot_actor.SetMapper(teapot_mapper)

# Outline
outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(normals_filter.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)

# Renderer 0 — outer edges fly mode
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.AddViewProp(teapot_actor)
renderer_0.AddViewProp(outline_actor)
renderer_0.SetBackground(0.1, 0.2, 0.4)

# Renderer 1 — closest triad fly mode
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.AddViewProp(teapot_actor)
renderer_1.AddViewProp(outline_actor)
renderer_1.SetBackground(0.1, 0.2, 0.4)

# Text property
text_property = vtkTextProperty()
text_property.SetColor(1, 1, 1)
text_property.ShadowOn()

# Axes 1 — outer edges
axes = vtkCubeAxesActor2D()
axes.SetInputConnection(normals_filter.GetOutputPort())
axes.SetLabelFormat("{:6.1f}")
axes.SetFlyModeToOuterEdges()
axes.SetFontFactor(0.8)
axes.SetAxisTitleTextProperty(text_property)
axes.SetAxisLabelTextProperty(text_property)
renderer_0.AddViewProp(axes)

# Axes 2 — closest triad
axes_2 = vtkCubeAxesActor2D()
axes_2.SetViewProp(teapot_actor)
axes_2.SetLabelFormat(axes.GetLabelFormat())
axes_2.SetFlyModeToClosestTriad()
axes_2.SetFontFactor(axes.GetFontFactor())
axes_2.ScalingOff()
axes_2.SetAxisTitleTextProperty(text_property)
axes_2.SetAxisLabelTextProperty(text_property)
renderer_1.AddViewProp(axes_2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("cube axes")
render_window.SetMultiSamples(0)
render_window.SetSize(790, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0)
light.SetPosition(8.3761, 4.94858, 4.12505)
renderer_0.AddLight(light)
renderer_1.AddLight(light)

renderer_0.GetActiveCamera().SetClippingRange(1.60187, 20.0842)
renderer_0.GetActiveCamera().SetFocalPoint(0.21406, 1.5, 0)
renderer_0.GetActiveCamera().SetPosition(11.63, 6.32, 5.77)
renderer_0.GetActiveCamera().SetViewUp(0.180325, 0.549245, -0.815974)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

axes.SetCamera(renderer_0.GetActiveCamera())
axes_2.SetCamera(renderer_1.GetActiveCamera())

interactor.Initialize()
interactor.Start()
