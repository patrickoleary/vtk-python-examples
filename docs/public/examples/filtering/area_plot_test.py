#!/usr/bin/env python
# Demonstrate an area plot with valid point masking using vtkPlotArea.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY, vtkPlotArea
from vtkmodules.vtkCommonCore import vtkCharArray, vtkFloatArray
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

arr_s2 = vtkFloatArray()
arr_s2.SetName("Sine2")
table.AddColumn(arr_s2)

arr_s3 = vtkFloatArray()
arr_s3.SetName("Sine3")
table.AddColumn(arr_s3)

arr_1 = vtkFloatArray()
arr_1.SetName("One")
table.AddColumn(arr_1)

valid_mask = vtkCharArray()
valid_mask.SetName("ValidMask")
table.AddColumn(valid_mask)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc + 0.01)
    table.SetValue(i, 1, math.cos(i * inc) + 0.01)
    table.SetValue(i, 2, math.sin(i * inc) + 0.01)
    table.SetValue(i, 3, math.sin(i * inc) + 0.5)
    table.SetValue(i, 4, math.sin(i * inc) ** 2 + 0.01)
    table.SetValue(i, 5, 1.0)
    valid_mask.SetValue(i, chr(0) if (i > 30 and i < 40) else chr(1))

# Set up a chart.
chart = vtkChartXY()

area = chart.AddPlot(vtkChartXY.AREA)
area.SetInputData(table)
area.SetInputArray(0, "X Axis")
area.SetInputArray(1, "Sine")
area.SetInputArray(2, "Sine2")
area.SetValidPointMaskName("ValidMask")
area.GetBrush().SetColorF(0.5, 0.5, 0.5, 0.5)

chart.GetAxis(vtkAxis.LEFT).LogScaleOn()

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
render_window.SetWindowName("area plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
