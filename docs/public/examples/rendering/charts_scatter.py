#!/usr/bin/env python
# Demonstrate scatter plot chart with serialization manager round-trip.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChart, vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build data table.
table = vtkTable()

array_x = vtkFloatArray()
array_x.SetName("X Axis")

array_cosine = vtkFloatArray()
array_cosine.SetName("Cosine")

array_sine = vtkFloatArray()
array_sine.SetName("Sine")

array_sine_cosine = vtkFloatArray()
array_sine_cosine.SetName("Sine-Cosine")

table.AddColumn(array_cosine)
table.AddColumn(array_sine)
table.AddColumn(array_x)
table.AddColumn(array_sine_cosine)

num_points = 40
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.sin(i * inc) - math.cos(i * inc))

# Chart.
chart = vtkChartXY()
chart.SetShowLegend(True)

points_0 = chart.AddPlot(vtkChart.POINTS)
points_0.SetInputData(table, 0, 1)
points_0.SetColor(0, 0, 0, 255)
points_0.SetWidth(1.0)
points_0.SetMarkerStyle(vtkPlotPoints.CROSS)

points_1 = chart.AddPlot(vtkChart.POINTS)
points_1.SetInputData(table, 0, 2)
points_1.SetColor(0, 0, 0, 255)
points_1.SetWidth(1.0)
points_1.SetMarkerStyle(vtkPlotPoints.PLUS)

points_2 = chart.AddPlot(vtkChart.POINTS)
points_2.SetInputData(table, 0, 3)
points_2.SetColor(0, 0, 255, 255)
points_2.SetWidth(1.0)
points_2.SetMarkerStyle(vtkPlotPoints.CIRCLE)

# Context actor pipeline
slate_gray_rgb = (0.4392, 0.5020, 0.5647)

context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

renderer = vtkRenderer()
renderer.SetBackground(*slate_gray_rgb)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("charts scatter")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
