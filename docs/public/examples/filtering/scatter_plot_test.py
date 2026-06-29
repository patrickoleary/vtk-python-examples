#!/usr/bin/env python
# Demonstrate a scatter plot with multiple marker styles using vtkChartXY.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkStringArray
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

arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)

arr_t = vtkFloatArray()
arr_t.SetName("Tan")
table.AddColumn(arr_t)

labels = vtkStringArray()
labels.SetName("Labels")
table.AddColumn(labels)

num_points = 40
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.tan(i * inc) + 0.5)
    table.SetValue(i, 4, "Odd" if i % 2 else "Even")

# Set up a chart.
chart = vtkChartXY()
chart.SetShowLegend(True)

# Add multiple scatter plots.
points = chart.AddPlot(vtkChartXY.POINTS)
points.SetInputData(table, 0, 1)
points.SetColor(0, 0, 0, 255)
points.SetWidth(1.0)
points.SetIndexedLabels(labels)
points.SetTooltipLabelFormat("{i} from {l} ({x}, {y})")
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
points.SetIndexedLabels(labels)

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
render_window.SetWindowName("scatter plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
