#!/usr/bin/env python

# Test vtkCubeAxesActor with sticky axes (not centered) on a teapot model.

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

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
teapot_reader = vtkBYUReader()
teapot_reader.SetGeometryFileName(os.path.join(data_dir, "teapot.g"))

# Filter
normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(teapot_reader.GetOutputPort())

# Teapot actor
teapot_mapper = vtkPolyDataMapper()
teapot_mapper.SetInputConnection(normals_filter.GetOutputPort())

teapot_actor = vtkActor()
teapot_actor.SetMapper(teapot_mapper)
teapot_actor.GetProperty().SetDiffuseColor(0.7, 0.3, 0.0)

# Outline
outline_filter = vtkOutlineFilter()
outline_filter.SetInputConnection(normals_filter.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0.0, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddViewProp(teapot_actor)
renderer.AddViewProp(outline_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

normals_filter.Update()

# Cube axes actor with sticky axes
axes = vtkCubeAxesActor()
axes.SetBounds(normals_filter.GetOutput().GetBounds())
axes.SetXAxisRange(20, 300)
axes.SetYAxisRange(-0.01, 0.01)
axes.SetXLabelFormat("{:6.1f}")
axes.SetYLabelFormat("{:6.1f}")
axes.SetZLabelFormat("{:6.1f}")
axes.SetScreenSize(15.0)
axes.SetFlyModeToClosestTriad()
axes.SetCornerOffset(0.0)
axes.SetStickyAxes(True)
axes.SetCenterStickyAxes(False)

# Red for X axis
axes.GetXAxesLinesProperty().SetColor(1.0, 0.0, 0.0)
axes.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes.GetLabelTextProperty(0).SetColor(0.8, 0.0, 0.0)

# Green for Y axis
axes.GetYAxesLinesProperty().SetColor(0.0, 1.0, 0.0)
axes.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes.GetLabelTextProperty(1).SetColor(0.0, 0.8, 0.0)

renderer.AddViewProp(axes)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cube axes sticky")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(8.3761, 4.94858, 4.12505)
renderer.AddLight(light)

renderer.GetActiveCamera().SetClippingRange(1.0, 100.0)
renderer.GetActiveCamera().SetFocalPoint(-4.1, 0.0, 1.0)
renderer.GetActiveCamera().SetPosition(3.63, 5.0, 4.77)
axes.SetCamera(renderer.GetActiveCamera())

interactor.Initialize()
interactor.Start()
