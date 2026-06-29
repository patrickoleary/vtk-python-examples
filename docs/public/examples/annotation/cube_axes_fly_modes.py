#!/usr/bin/env python

# Demonstrate vtkCubeAxesActor with five fly modes in five viewports.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOGeometry import vtkBYUReader
from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
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

# Five renderers with different fly modes
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 0.5)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.66, 0.5)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.66, 0, 1.0, 0.5)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0, 0.5, 0.5, 1.0)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.5, 0.5, 1.0, 1.0)

# Add actors to renderers
renderer_0.AddViewProp(teapot_actor)
renderer_0.AddViewProp(outline_actor)
renderer_1.AddViewProp(teapot_actor)
renderer_1.AddViewProp(outline_actor)
renderer_2.AddViewProp(teapot_actor)
renderer_2.AddViewProp(outline_actor)
renderer_3.AddViewProp(teapot_actor)
renderer_3.AddViewProp(outline_actor)
renderer_4.AddViewProp(teapot_actor)

renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_3.SetBackground(0.1, 0.2, 0.4)
renderer_4.SetBackground(0.1, 0.2, 0.4)

normals_filter.Update()
bounds = normals_filter.GetOutput().GetBounds()

# Axes 1 — outer edges
axes = vtkCubeAxesActor()
axes.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5])
axes.SetCamera(renderer_0.GetActiveCamera())
axes.SetXLabelFormat("{:6.1f}")
axes.SetYLabelFormat("{:6.1f}")
axes.SetZLabelFormat("{:6.1f}")
axes.SetFlyModeToOuterEdges()
renderer_0.AddViewProp(axes)

# Axes 2 — closest triad
axes_2 = vtkCubeAxesActor()
axes_2.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5])
axes_2.SetCamera(renderer_1.GetActiveCamera())
axes_2.SetXLabelFormat(axes.GetXLabelFormat())
axes_2.SetYLabelFormat(axes.GetYLabelFormat())
axes_2.SetZLabelFormat(axes.GetZLabelFormat())
axes_2.SetFlyModeToClosestTriad()
renderer_1.AddViewProp(axes_2)

# Axes 3 — furthest triad
axes_3 = vtkCubeAxesActor()
axes_3.SetBounds(bounds[0], bounds[1], bounds[2], bounds[3], bounds[4], bounds[5])
axes_3.SetCamera(renderer_1.GetActiveCamera())
axes_3.SetXLabelFormat(axes.GetXLabelFormat())
axes_3.SetYLabelFormat(axes.GetYLabelFormat())
axes_3.SetZLabelFormat(axes.GetZLabelFormat())
axes_3.SetFlyModeToFurthestTriad()
renderer_2.AddViewProp(axes_3)

bounds_2 = axes_3.GetBounds()

# Axes 4 — static triad
axes_4 = vtkCubeAxesActor()
axes_4.SetBounds(bounds_2[0], bounds_2[1], bounds_2[2], bounds_2[3], bounds_2[4], bounds_2[5])
axes_4.SetCamera(renderer_1.GetActiveCamera())
axes_4.SetXLabelFormat(axes.GetXLabelFormat())
axes_4.SetYLabelFormat(axes.GetYLabelFormat())
axes_4.SetZLabelFormat(axes.GetZLabelFormat())
axes_4.SetFlyModeToStaticTriad()
renderer_3.AddViewProp(axes_4)

# Axes 5 — static edges
axes_5 = vtkCubeAxesActor()
axes_5.SetBounds(bounds_2[0], bounds_2[1], bounds_2[2], bounds_2[3], bounds_2[4], bounds_2[5])
axes_5.SetCamera(renderer_1.GetActiveCamera())
axes_5.SetXLabelFormat(axes.GetXLabelFormat())
axes_5.SetYLabelFormat(axes.GetYLabelFormat())
axes_5.SetZLabelFormat(axes.GetZLabelFormat())
axes_5.SetFlyModeToStaticEdges()
renderer_4.AddViewProp(axes_5)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.SetWindowName("cube axes fly modes")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0)
light.SetPosition(8.3761, 4.94858, 4.12505)
renderer_0.AddLight(light)
renderer_1.AddLight(light)
renderer_2.AddLight(light)
renderer_3.AddLight(light)
renderer_4.AddLight(light)

renderer_0.GetActiveCamera().SetClippingRange(1.60187, 20.0842)
renderer_0.GetActiveCamera().SetFocalPoint(0.21406, 1.5, 0)
renderer_0.GetActiveCamera().SetPosition(11.63, 6.32, 5.77)
renderer_0.GetActiveCamera().SetViewUp(0.180325, 0.549245, -0.815974)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_2.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_3.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_4.SetActiveCamera(renderer_0.GetActiveCamera())

interactor.Initialize()
interactor.Start()
