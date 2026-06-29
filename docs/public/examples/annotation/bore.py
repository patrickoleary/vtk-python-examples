#!/usr/bin/env python

# Create arc plots along bore hole tracks using vtkArcPlotter.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkTubeFilter
from vtkmodules.vtkIOLegacy import vtkPolyDataReader
from vtkmodules.vtkRenderingAnnotation import vtkArcPlotter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data path
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Camera
camera = vtkCamera()

# Read bore
bore_reader = vtkPolyDataReader()
bore_reader.SetFileName(os.path.join(data_dir, "bore.vtk"))

tuber = vtkTubeFilter()
tuber.SetInputConnection(bore_reader.GetOutputPort())
tuber.SetNumberOfSides(6)
tuber.SetRadius(15)

bore_mapper = vtkPolyDataMapper()
bore_mapper.SetInputConnection(tuber.GetOutputPort())
bore_mapper.ScalarVisibilityOff()

bore_actor = vtkActor()
bore_actor.SetMapper(bore_mapper)
bore_actor.GetProperty().SetColor(0, 0, 0)

# Track 1 arc plot
track_1 = vtkPolyDataReader()
track_1.SetFileName(os.path.join(data_dir, "track1.binary.vtk"))

arc_plotter = vtkArcPlotter()
arc_plotter.SetInputConnection(track_1.GetOutputPort())
arc_plotter.SetCamera(camera)
arc_plotter.SetRadius(250.0)
arc_plotter.SetHeight(200.0)
arc_plotter.UseDefaultNormalOn()
arc_plotter.SetDefaultNormal(1, 1, 0)

arc_mapper = vtkPolyDataMapper()
arc_mapper.SetInputConnection(arc_plotter.GetOutputPort())

arc_actor = vtkActor()
arc_actor.SetMapper(arc_mapper)
arc_actor.GetProperty().SetColor(0, 1, 0)

# Track 2 arc plot
track_2 = vtkPolyDataReader()
track_2.SetFileName(os.path.join(data_dir, "track2.binary.vtk"))

arc_plotter_2 = vtkArcPlotter()
arc_plotter_2.SetInputConnection(track_2.GetOutputPort())
arc_plotter_2.SetCamera(camera)
arc_plotter_2.SetRadius(450.0)
arc_plotter_2.SetHeight(200.0)
arc_plotter_2.UseDefaultNormalOn()
arc_plotter_2.SetDefaultNormal(1, 1, 0)

arc_mapper_2 = vtkPolyDataMapper()
arc_mapper_2.SetInputConnection(arc_plotter_2.GetOutputPort())

arc_actor_2 = vtkActor()
arc_actor_2.SetMapper(arc_mapper_2)
arc_actor_2.GetProperty().SetColor(0, 0, 1)

# Track 3 arc plot
track_3 = vtkPolyDataReader()
track_3.SetFileName(os.path.join(data_dir, "track3.binary.vtk"))

arc_plotter_3 = vtkArcPlotter()
arc_plotter_3.SetInputConnection(track_3.GetOutputPort())
arc_plotter_3.SetCamera(camera)
arc_plotter_3.SetRadius(250.0)
arc_plotter_3.SetHeight(50.0)
arc_plotter_3.SetDefaultNormal(1, 1, 0)

arc_mapper_3 = vtkPolyDataMapper()
arc_mapper_3.SetInputConnection(arc_plotter_3.GetOutputPort())

arc_actor_3 = vtkActor()
arc_actor_3.SetMapper(arc_mapper_3)
arc_actor_3.GetProperty().SetColor(1, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.SetActiveCamera(camera)
renderer.AddActor(bore_actor)
renderer.AddActor(arc_actor)
renderer.AddActor(arc_actor_2)
renderer.AddActor(arc_actor_3)
renderer.SetBackground(1, 1, 1)

# Camera settings
camera.SetClippingRange(14144, 32817)
camera.SetFocalPoint(-1023, 680, 5812)
camera.SetPosition(15551, -2426, 19820)
camera.SetViewUp(-0.651889, -0.07576, 0.754521)
camera.SetViewAngle(20)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetMultiSamples(0)
render_window.SetSize(230, 500)
render_window.SetWindowName("bore")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
interactor.Start()
