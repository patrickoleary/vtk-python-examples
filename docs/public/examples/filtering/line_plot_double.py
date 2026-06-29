#!/usr/bin/env python
# Demonstrate a line plot with very small double values, NaN, and Inf.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkDoubleArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkDoubleArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)
arr_s = vtkDoubleArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)
arr_s2 = vtkDoubleArray()
arr_s2.SetName("Sine2")
table.AddColumn(arr_s2)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, 1.0e-80 * math.cos(i * inc - 1.0) * 1.0e-8)
    table.SetValue(i, 2, 1.0e-80 * math.sin(i * inc) * 1.0e-8)
    table.SetValue(i, 3, 1.0e80 * math.sin(i * inc - 1.0))

table.SetValue(66, 2, float("nan"))
table.SetValue(4, 3, float("inf"))

# Set up a chart.
chart = vtkChartXY()

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
chart.SetPlotCorner(line, 1)

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
render_window.SetWindowName("line plot double")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
