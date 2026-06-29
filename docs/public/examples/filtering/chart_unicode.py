#!/usr/bin/env python
# Demonstrate a chart with Unicode text in title and axis labels.

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

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc) + math.sin(i * (inc - math.pi)))

# Set up a chart with Unicode labels.
chart = vtkChartXY()
chart.SetTitle("\u03c5\u03c4\u03ba")

axis1 = chart.GetAxis(0)
axis1.SetTitle("\u03c7(m)")

axis2 = chart.GetAxis(1)
axis2.SetTitle("\u03c0\u03c6")

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(42, 55, 69, 255)

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
render_window.SetWindowName("chart unicode")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
