#!/usr/bin/env python
# Demonstrate chart tick mark consistency with tile scaling enabled.

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
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)
arr_1 = vtkFloatArray()
arr_1.SetName("One")
table.AddColumn(arr_1)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.sin(i * inc))
    table.SetValue(i, 2, 1.0)

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
render_window.SwapBuffersOn()
render_window.SetTileScale(2)
render_window.AddRenderer(renderer)
render_window.SetWindowName("chart tile scaling")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
