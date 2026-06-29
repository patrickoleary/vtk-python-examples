#!/usr/bin/env python
# Demonstrate a line plot with multiple series using vtkChartXY.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Number of points and x increment.
num_points = 65
inc_x = 7.5 / (num_points - 1)

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

arr_1 = vtkFloatArray()
arr_1.SetName("One")
table.AddColumn(arr_1)

table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc_x
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, math.cos(x))
    table.SetValue(i, 2, math.sin(x))
    table.SetValue(i, 3, 1.0)

# Also create a sine+0.5 table for the third plot via direct arrays.
arr_x2 = vtkFloatArray()
arr_x2.SetName("X Axis")
arr_y2 = vtkFloatArray()
arr_y2.SetName("Sine2")
arr_x2.SetNumberOfTuples(num_points)
arr_y2.SetNumberOfTuples(num_points)
for i in range(num_points):
    x = i * inc_x
    arr_x2.SetTuple1(i, x)
    arr_y2.SetTuple1(i, math.sin(x) + 0.5)

table2 = vtkTable()
table2.AddColumn(arr_x2)
table2.AddColumn(arr_y2)
table2.SetNumberOfRows(num_points)

# Set up a chart.
chart = vtkChartXY()

# Add multiple line plots.
line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)
line.SetWidth(1.0)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)
line.SetWidth(5.0)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table2, 0, 1)
line.SetColor(0, 0, 255, 255)
line.SetWidth(4.0)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(400, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("line plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
