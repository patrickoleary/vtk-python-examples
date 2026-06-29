#!/usr/bin/env python
# Demonstrate a 2D chart overlaid on a 3D scene with a cube.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectf, vtkTable
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)
arr_t = vtkFloatArray()
arr_t.SetName("Tan")
table.AddColumn(arr_t)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.tan(i * inc) + 0.5)

# Cube source.
cube = vtkCubeSource()

cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
cube_actor.GetProperty().SetRepresentationToSurface()

# Chart overlaid on 3D scene.
chart = vtkChartXY()
chart.SetAutoSize(False)
chart.SetSize(vtkRectf(0.0, 0.0, 300, 200))

# Add scatter plots.
points = chart.AddPlot(vtkChartXY.POINTS)
points.SetInputData(table, 0, 1)
points.SetColor(0, 0, 0, 255)
points.SetWidth(1.0)
vtkPlotPoints.SafeDownCast(points).SetMarkerStyle(vtkPlotPoints.CROSS)

points = chart.AddPlot(vtkChartXY.POINTS)
points.SetInputData(table, 0, 2)
points.SetColor(0, 0, 0, 255)
points.SetWidth(1.0)
vtkPlotPoints.SafeDownCast(points).SetMarkerStyle(vtkPlotPoints.PLUS)

points = chart.AddPlot(vtkChartXY.POINTS)
points.SetInputData(table, 0, 3)
points.SetColor(0, 0, 255, 255)
points.SetWidth(4.0)

# Context scene wiring.
chart_scene = vtkContextScene()
chart_scene.AddItem(chart)
chart_actor = vtkContextActor()
chart_actor.SetScene(chart_scene)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)
renderer.AddActor(cube_actor)
chart_scene.SetRenderer(renderer)
renderer.AddActor(chart_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("charts on3d")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().SetPosition(1.0, 1.0, -4.0)
renderer.GetActiveCamera().Azimuth(40)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
