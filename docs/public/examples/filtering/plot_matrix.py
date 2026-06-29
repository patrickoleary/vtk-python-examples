#!/usr/bin/env python
# Demonstrate four fixed-size charts arranged in a 2x2 grid within a single scene.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectf, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
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

# Chart 1: multiple line plots (bottom-left).
chart1 = vtkChartXY()
chart1.SetAutoSize(False)
chart1.SetSize(vtkRectf(0.0, 0.0, 200.0, 150.0))
line = chart1.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)
line.SetWidth(1.0)
line = chart1.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)
line.SetWidth(5.0)
line = chart1.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 3)
line.SetColor(0, 0, 255, 255)
line.SetWidth(4.0)

# Chart 2: single line plot (bottom-right).
chart2 = vtkChartXY()
chart2.SetAutoSize(False)
chart2.SetSize(vtkRectf(200.0, 0.0, 200.0, 150.0))
line = chart2.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)

# Chart 3: point plot (top-left).
chart3 = vtkChartXY()
chart3.SetAutoSize(False)
chart3.SetSize(vtkRectf(0.0, 150.0, 200.0, 150.0))
line = chart3.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 1)

# Chart 4: bar plot (top-right).
chart4 = vtkChartXY()
chart4.SetAutoSize(False)
chart4.SetSize(vtkRectf(200.0, 150.0, 200.0, 150.0))
line = chart4.AddPlot(vtkChartXY.BAR)
line.SetInputData(table, 0, 1)
chart4.GetAxis(vtkAxis.BOTTOM).SetBehavior(vtkAxis.FIXED)
chart4.GetAxis(vtkAxis.BOTTOM).SetRange(0.0, 10.0)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart1)
context_actor.GetScene().AddItem(chart2)
context_actor.GetScene().AddItem(chart3)
context_actor.GetScene().AddItem(chart4)

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
render_window.SetWindowName("plot matrix")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
