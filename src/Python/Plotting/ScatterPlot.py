#!/usr/bin/env python

# Scatter plot of trig functions using a chart overlay on the VTK pipeline.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartXY,
    vtkPlotPoints,
)
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Data: generate trig function values
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X Axis")

arr_cos = vtkFloatArray()
arr_cos.SetName("Cosine")

arr_sin = vtkFloatArray()
arr_sin.SetName("Sine")

arr_diff = vtkFloatArray()
arr_diff.SetName("Sine-Cosine")

table.AddColumn(arr_x)
table.AddColumn(arr_cos)
table.AddColumn(arr_sin)
table.AddColumn(arr_diff)

num_points = 40
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.sin(i * inc) - math.cos(i * inc))

# Chart: create a 2D XY chart with three scatter series
chart = vtkChartXY()
chart.SetShowLegend(True)

points = chart.AddPlot(vtkChart.POINTS)
points.SetInputData(table, 0, 1)
points.SetColor(0, 0, 0, 255)
points.SetWidth(1.0)
points.SetMarkerStyle(vtkPlotPoints.CROSS)

points = chart.AddPlot(vtkChart.POINTS)
points.SetInputData(table, 0, 2)
points.SetColor(0, 0, 0, 255)
points.SetWidth(1.0)
points.SetMarkerStyle(vtkPlotPoints.PLUS)

points = chart.AddPlot(vtkChart.POINTS)
points.SetInputData(table, 0, 3)
points.SetColor(0, 0, 255, 255)
points.SetWidth(1.0)
points.SetMarkerStyle(vtkPlotPoints.CIRCLE)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(slate_gray_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("ScatterPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
