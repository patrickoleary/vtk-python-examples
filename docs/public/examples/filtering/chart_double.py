#!/usr/bin/env python
# Demonstrate chart with very small double values on multiple axes.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY
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
arr_x.SetName("X")
table.AddColumn(arr_x)
arr_c = vtkDoubleArray()
arr_c.SetName("f1")
table.AddColumn(arr_c)
arr_s = vtkDoubleArray()
arr_s.SetName("f2")
table.AddColumn(arr_s)
arr_s2 = vtkDoubleArray()
arr_s2.SetName("f3")
table.AddColumn(arr_s2)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc + 0.2
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, 1.0e-80 * (math.cos(x - 1.0) + math.sin(x - math.pi / 4.0)))
    table.SetValue(i, 2, 1.0e-80 * math.sin(x) * 1e-12)
    table.SetValue(i, 3, 1.0e-80 * math.sin(x - 1.0))

# Set up a chart.
chart = vtkChartXY()

line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 1)

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
# Put this plot in a different corner.
chart.SetPlotCorner(line, 1)

line = chart.AddPlot(vtkChartXY.BAR)
line.SetInputData(table, 0, 3)

chart.GetAxis(vtkAxis.LEFT).SetTitle("A tiny range")
chart.GetAxis(vtkAxis.BOTTOM).SetTitle("A normal range")
chart.GetAxis(vtkAxis.RIGHT).SetTitle("An even tinier range")

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
render_window.SetWindowName("chart double")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
