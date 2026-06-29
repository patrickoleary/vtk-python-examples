#!/usr/bin/env python
# Demonstrate chart handling of NaN values in line and point plots.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotLine, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

nan = float("nan")

# Create a table with polyline points.
table = vtkTable()
arr_x = vtkDoubleArray()
arr_x.SetName("X")
table.AddColumn(arr_x)
arr_c = vtkDoubleArray()
arr_c.SetName("f1")
table.AddColumn(arr_c)
table.SetNumberOfRows(7)
for i, (xv, yv) in enumerate([(0, 1.7), (1, 1.9), (2, nan), (3, 2), (4, nan), (5, 2.3), (6, 2.1)]):
    table.SetValue(i, 0, xv)
    table.SetValue(i, 1, yv)

# Create a table with non-polyline points.
table2 = vtkTable()
arr_x2 = vtkDoubleArray()
arr_x2.SetName("X")
table2.AddColumn(arr_x2)
arr_c2 = vtkDoubleArray()
arr_c2.SetName("f1")
table2.AddColumn(arr_c2)
x_vals2 = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6]
y_vals2 = [3.7, 3.9, 3.9, nan, nan, 4, 5, nan, nan, 5.3, 5.3, 4.3]
table2.SetNumberOfRows(12)
for i in range(12):
    table2.SetValue(i, 0, x_vals2[i])
    table2.SetValue(i, 1, y_vals2[i])

# Set up a chart.
chart = vtkChartXY()

points = vtkPlotPoints()
chart.AddPlot(points)
points.SetInputData(table, 0, 1)
points.SetMarkerSize(10.0)

line = vtkPlotLine()
chart.AddPlot(line)
line.SetInputData(table, 0, 1)

line2 = vtkPlotLine()
line2.SetPolyLine(False)
chart.AddPlot(line2)
line2.SetInputData(table2, 0, 1)

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
render_window.SetWindowName("chart bad points")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
