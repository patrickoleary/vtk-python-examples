#!/usr/bin/env python
# Demonstrate AdjustLowerBoundForLogPlot with a log-scale Y axis.

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

x_array = vtkFloatArray()
x_array.SetName("X")
table.AddColumn(x_array)

data_array = vtkFloatArray()
data_array.SetName("Data")
table.AddColumn(data_array)

num_rows = 100
table.SetNumberOfRows(num_rows)
for i in range(num_rows):
    x = 0.1 * ((-0.5 * (num_rows - 1)) + i)
    table.SetValue(i, 0, x)
    y = abs(x * x - 10.0)
    table.SetValue(i, 1, y)

# Set up a chart.
chart = vtkChartXY()
chart.AdjustLowerBoundForLogPlotOn()

plot = chart.AddPlot(vtkChartXY.LINE)
plot.SetInputData(table, 0, 1)

axis = chart.GetAxis(vtkAxis.LEFT)
axis.LogScaleOn()
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
render_window.SetSize(300, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("adjust lower bound for log plot")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
