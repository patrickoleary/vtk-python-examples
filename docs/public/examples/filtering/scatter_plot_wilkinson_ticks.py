#!/usr/bin/env python
# Demonstrate a scatter plot with Wilkinson extended tick label algorithm.

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

# Traced data from Talbot et al. paper.
data_x = [
    8.1, 8.6, 8.65, 8.9, 8.95, 9.2, 9.4, 9.6, 9.9, 10, 10.1, 10.1, 10.15,
    10.3, 10.35, 10.5, 10.52, 10.55, 10.85, 10.95, 11.05, 11.07, 11.15, 11.3,
    11.4, 11.6, 11.95, 12.6, 12.85, 13.1, 14.1,
]
data_y = [
    59.9, 60.5, 54.1, 54.25, 49, 50, 48, 45.2, 51.1, 47, 51, 45.8, 51.1,
    47.2, 52, 46, 48, 47.6, 49, 41.5, 45.5, 44.7, 46.5, 44.1, 48.5, 44.8,
    45.1, 39, 38.7, 38.9, 37.8,
]

# Create a table.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Y Axis")
table.AddColumn(arr_c)

num_points = 31
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, data_x[i])
    table.SetValue(i, 1, data_y[i])

# Set up a chart.
chart = vtkChartXY()

line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)
line.SetWidth(1.0)

# Use the Wilkinson extended tick label algorithm.
chart.GetAxis(vtkAxis.LEFT).SetTickLabelAlgorithm(vtkAxis.TICK_WILKINSON_EXTENDED)
chart.GetAxis(vtkAxis.BOTTOM).SetTickLabelAlgorithm(vtkAxis.TICK_WILKINSON_EXTENDED)

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
render_window.SetWindowName("scatter plot wilkinson ticks")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
