#!/usr/bin/env python
# Demonstrate four charts in separate renderers/viewports within one render window.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Chart data.
num_points = 69
inc = 7.5 / (num_points - 1)

# Table 0.
table_0 = vtkTable()
arr_x_0 = vtkFloatArray()
arr_x_0.SetName("X Axis")
table_0.AddColumn(arr_x_0)
arr_c_0 = vtkFloatArray()
arr_c_0.SetName("Cosine")
table_0.AddColumn(arr_c_0)
arr_s_0 = vtkFloatArray()
arr_s_0.SetName("Sine")
table_0.AddColumn(arr_s_0)
arr_s2_0 = vtkFloatArray()
arr_s2_0.SetName("Sine2")
table_0.AddColumn(arr_s2_0)
table_0.SetNumberOfRows(num_points)
for j in range(num_points):
    table_0.SetValue(j, 0, j * inc)
    table_0.SetValue(j, 1, math.cos(j * inc))
    table_0.SetValue(j, 2, math.sin(j * inc))
    table_0.SetValue(j, 3, math.sin(j * inc) + 0.5)

# Table 1.
table_1 = vtkTable()
arr_x_1 = vtkFloatArray()
arr_x_1.SetName("X Axis")
table_1.AddColumn(arr_x_1)
arr_c_1 = vtkFloatArray()
arr_c_1.SetName("Cosine")
table_1.AddColumn(arr_c_1)
arr_s_1 = vtkFloatArray()
arr_s_1.SetName("Sine")
table_1.AddColumn(arr_s_1)
arr_s2_1 = vtkFloatArray()
arr_s2_1.SetName("Sine2")
table_1.AddColumn(arr_s2_1)
table_1.SetNumberOfRows(num_points)
for j in range(num_points):
    table_1.SetValue(j, 0, j * inc)
    table_1.SetValue(j, 1, math.cos(j * inc))
    table_1.SetValue(j, 2, math.sin(j * inc))
    table_1.SetValue(j, 3, math.sin(j * inc) + 0.5)

# Table 2.
table_2 = vtkTable()
arr_x_2 = vtkFloatArray()
arr_x_2.SetName("X Axis")
table_2.AddColumn(arr_x_2)
arr_c_2 = vtkFloatArray()
arr_c_2.SetName("Cosine")
table_2.AddColumn(arr_c_2)
arr_s_2 = vtkFloatArray()
arr_s_2.SetName("Sine")
table_2.AddColumn(arr_s_2)
arr_s2_2 = vtkFloatArray()
arr_s2_2.SetName("Sine2")
table_2.AddColumn(arr_s2_2)
table_2.SetNumberOfRows(num_points)
for j in range(num_points):
    table_2.SetValue(j, 0, j * inc)
    table_2.SetValue(j, 1, math.cos(j * inc))
    table_2.SetValue(j, 2, math.sin(j * inc))
    table_2.SetValue(j, 3, math.sin(j * inc) + 0.5)

# Table 3.
table_3 = vtkTable()
arr_x_3 = vtkFloatArray()
arr_x_3.SetName("X Axis")
table_3.AddColumn(arr_x_3)
arr_c_3 = vtkFloatArray()
arr_c_3.SetName("Cosine")
table_3.AddColumn(arr_c_3)
arr_s_3 = vtkFloatArray()
arr_s_3.SetName("Sine")
table_3.AddColumn(arr_s_3)
arr_s2_3 = vtkFloatArray()
arr_s2_3.SetName("Sine2")
table_3.AddColumn(arr_s2_3)
table_3.SetNumberOfRows(num_points)
for j in range(num_points):
    table_3.SetValue(j, 0, j * inc)
    table_3.SetValue(j, 1, math.cos(j * inc))
    table_3.SetValue(j, 2, math.sin(j * inc))
    table_3.SetValue(j, 3, math.sin(j * inc) + 0.5)

# Chart 0.
chart_0 = vtkChartXY()
chart_scene_0 = vtkContextScene()
chart_scene_0.AddItem(chart_0)
chart_actor_0 = vtkContextActor()
chart_actor_0.SetScene(chart_scene_0)

line_0_0 = chart_0.AddPlot(vtkChartXY.LINE)
line_0_0.SetInputData(table_0, 0, 1)
line_0_0.SetColor(0, 255, 0, 255)
line_0_0.SetWidth(1.0)
line_0_1 = chart_0.AddPlot(vtkChartXY.LINE)
line_0_1.SetInputData(table_0, 0, 2)
line_0_1.SetColor(255, 0, 0, 255)
line_0_1.SetWidth(5.0)
line_0_2 = chart_0.AddPlot(vtkChartXY.LINE)
line_0_2.SetInputData(table_0, 0, 3)
line_0_2.SetColor(0, 0, 255, 255)
line_0_2.SetWidth(4.0)

# Chart 1.
chart_1 = vtkChartXY()
chart_scene_1 = vtkContextScene()
chart_scene_1.AddItem(chart_1)
chart_actor_1 = vtkContextActor()
chart_actor_1.SetScene(chart_scene_1)

line_1_0 = chart_1.AddPlot(vtkChartXY.LINE)
line_1_0.SetInputData(table_1, 0, 1)
line_1_0.SetColor(0, 255, 0, 255)
line_1_0.SetWidth(1.0)
line_1_1 = chart_1.AddPlot(vtkChartXY.LINE)
line_1_1.SetInputData(table_1, 0, 2)
line_1_1.SetColor(255, 0, 0, 255)
line_1_1.SetWidth(5.0)
line_1_2 = chart_1.AddPlot(vtkChartXY.LINE)
line_1_2.SetInputData(table_1, 0, 3)
line_1_2.SetColor(0, 0, 255, 255)
line_1_2.SetWidth(4.0)

# Chart 2.
chart_2 = vtkChartXY()
chart_scene_2 = vtkContextScene()
chart_scene_2.AddItem(chart_2)
chart_actor_2 = vtkContextActor()
chart_actor_2.SetScene(chart_scene_2)

line_2_0 = chart_2.AddPlot(vtkChartXY.LINE)
line_2_0.SetInputData(table_2, 0, 1)
line_2_0.SetColor(0, 255, 0, 255)
line_2_0.SetWidth(1.0)
line_2_1 = chart_2.AddPlot(vtkChartXY.LINE)
line_2_1.SetInputData(table_2, 0, 2)
line_2_1.SetColor(255, 0, 0, 255)
line_2_1.SetWidth(5.0)
line_2_2 = chart_2.AddPlot(vtkChartXY.LINE)
line_2_2.SetInputData(table_2, 0, 3)
line_2_2.SetColor(0, 0, 255, 255)
line_2_2.SetWidth(4.0)

# Chart 3.
chart_3 = vtkChartXY()
chart_scene_3 = vtkContextScene()
chart_scene_3.AddItem(chart_3)
chart_actor_3 = vtkContextActor()
chart_actor_3.SetScene(chart_scene_3)

line_3_0 = chart_3.AddPlot(vtkChartXY.LINE)
line_3_0.SetInputData(table_3, 0, 1)
line_3_0.SetColor(0, 255, 0, 255)
line_3_0.SetWidth(1.0)
line_3_1 = chart_3.AddPlot(vtkChartXY.LINE)
line_3_1.SetInputData(table_3, 0, 2)
line_3_1.SetColor(255, 0, 0, 255)
line_3_1.SetWidth(5.0)
line_3_2 = chart_3.AddPlot(vtkChartXY.LINE)
line_3_2.SetInputData(table_3, 0, 3)
line_3_2.SetColor(0, 0, 255, 255)
line_3_2.SetWidth(4.0)

# Renderers.
renderer_0 = vtkRenderer()
renderer_0.SetBackground(1.0, 1.0, 1.0)
renderer_0.SetViewport(0.0, 0.0, 0.3, 0.5)
renderer_0.AddActor(chart_actor_0)
chart_scene_0.SetRenderer(renderer_0)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(1.0, 1.0, 1.0)
renderer_1.SetViewport(0.3, 0.0, 1.0, 0.5)
renderer_1.AddActor(chart_actor_1)
chart_scene_1.SetRenderer(renderer_1)

renderer_2 = vtkRenderer()
renderer_2.SetBackground(1.0, 1.0, 1.0)
renderer_2.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_2.AddActor(chart_actor_2)
chart_scene_2.SetRenderer(renderer_2)

renderer_3 = vtkRenderer()
renderer_3.SetBackground(1.0, 1.0, 1.0)
renderer_3.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_3.AddActor(chart_actor_3)
chart_scene_3.SetRenderer(renderer_3)

# Window.
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(800, 640)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetWindowName("multiple chart renderers")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
