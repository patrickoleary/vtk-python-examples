#!/usr/bin/env python
# Demonstrate a scientific-style chart with axes drawn at the origin.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
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
arr_c.SetName("cos")
table.AddColumn(arr_c)
arr_s = vtkFloatArray()
arr_s.SetName("sin")
table.AddColumn(arr_s)
arr_s2 = vtkFloatArray()
arr_s2.SetName("x^3")
table.AddColumn(arr_s2)

num_points = 69
inc = 3.0 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    v = -1.0 + i * inc
    table.SetValue(i, 0, v)
    table.SetValue(i, 1, math.cos(v))
    table.SetValue(i, 2, math.sin(v))
    table.SetValue(i, 3, v * v * v)

# Set up a chart.
chart = vtkChartXY()

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)

line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 3)
line.SetColor(0, 0, 255, 255)

# Scientific plot settings.
chart.SetDrawAxesAtOrigin(True)
chart.SetShowLegend(True)
chart.GetAxis(vtkAxis.LEFT).SetRange(1.0, -1.5)
chart.GetAxis(vtkAxis.LEFT).SetNotation(2)
chart.GetAxis(vtkAxis.LEFT).SetPrecision(1)
chart.GetAxis(vtkAxis.LEFT).SetBehavior(vtkAxis.FIXED)
chart.GetAxis(vtkAxis.LEFT).SetTitle("")
chart.GetAxis(vtkAxis.BOTTOM).SetRange(-1.0, 1.5)
chart.GetAxis(vtkAxis.BOTTOM).SetNotation(2)
chart.GetAxis(vtkAxis.BOTTOM).SetPrecision(1)
chart.GetAxis(vtkAxis.BOTTOM).SetBehavior(vtkAxis.FIXED)
chart.GetAxis(vtkAxis.BOTTOM).SetTitle("")

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
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scientific plot")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
