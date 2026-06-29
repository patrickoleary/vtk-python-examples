#!/usr/bin/env python
# Demonstrate turning on log scale after initial render and updating chart parameters.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartLegend, vtkChartXY
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
arr_y1 = vtkFloatArray()
arr_y1.SetName("y=x")
table.AddColumn(arr_y1)
arr_y2 = vtkFloatArray()
arr_y2.SetName("y=-x")
table.AddColumn(arr_y2)

num_points = 10
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = 1.0e-5 + i * inc
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, x)
    table.SetValue(i, 2, -x)

# Set up a chart.
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.GetLegend().SetHorizontalAlignment(vtkChartLegend.CENTER)

# Add a bar plot.
bar = chart.AddPlot(vtkChartXY.BAR)
bar.SetInputData(table, 0, 1)
bar.SetColor(255, 0, 0, 255)

# Add a line plot.
line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 2)
line.SetColor(0, 0, 255, 255)
line.SetWidth(4.0)

# Turn on log scale and update chart parameters.
x_range = [0.0, 0.0]
arr_x.GetRange(x_range, 0)
chart.GetAxis(vtkAxis.BOTTOM).SetUnscaledMinimum(x_range[0])
chart.GetAxis(vtkAxis.BOTTOM).SetUnscaledMaximum(x_range[1])
chart.GetAxis(vtkAxis.BOTTOM).LogScaleOn()
chart.GetAxis(vtkAxis.BOTTOM).SetCustomTickPositions(None)
chart.GetAxis(vtkAxis.BOTTOM).Update()
chart.Update()
chart.RecalculateBounds()

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
render_window.SetWindowName("chart log scale updates")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
