#!/usr/bin/env python
# Demonstrate a 3D cube in one viewport and a 2D chart in another.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(800, 640)
render_window.SetWindowName("multiple renderers")

# 3D renderer with a cube.
renderer_3d = vtkRenderer()
renderer_3d.SetBackground(0.0, 0.0, 0.0)
renderer_3d.SetViewport(0, 0, 1, 0.5)
render_window.AddRenderer(renderer_3d)

cube = vtkCubeSource()
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)
cube_actor.GetProperty().SetColor(1.0, 0.0, 0.0)
cube_actor.GetProperty().SetRepresentationToSurface()
renderer_3d.AddActor(cube_actor)

# 2D renderer with a chart.
renderer_2d = vtkRenderer()
renderer_2d.SetBackground(1.0, 1.0, 1.0)
renderer_2d.SetViewport(0, 0.5, 1, 1)
render_window.AddRenderer(renderer_2d)

chart = vtkChartXY()
chart_scene = vtkContextScene()
chart_actor = vtkContextActor()

chart_scene.AddItem(chart)
chart_actor.SetScene(chart_scene)

renderer_2d.AddActor(chart_actor)
chart_scene.SetRenderer(renderer_2d)

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
arr_s2 = vtkFloatArray()
arr_s2.SetName("Sine2")
table.AddColumn(arr_s2)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.sin(i * inc) + 0.5)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)
line.SetWidth(1.0)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)
line.SetWidth(5.0)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 3)
line.SetColor(0, 0, 255, 255)
line.SetWidth(4.0)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
