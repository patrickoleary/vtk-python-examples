#!/usr/bin/env python

# Line plot of sine and cosine using a chart overlay on the VTK pipeline.

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
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: generate sine and cosine values
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X")
table.AddColumn(arr_x)

arr_sin = vtkFloatArray()
arr_sin.SetName("Sine")
table.AddColumn(arr_sin)

arr_cos = vtkFloatArray()
arr_cos.SetName("Cosine")
table.AddColumn(arr_cos)

num_points = 80
inc = 2.0 * math.pi / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, math.sin(x))
    table.SetValue(i, 2, math.cos(x))

# Chart: create a 2D XY chart with two line series
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.SetTitle("Sine and Cosine")

line_sin = chart.AddPlot(vtkChart.LINE)
line_sin.SetInputData(table, 0, 1)
line_sin.SetColor(220, 20, 60, 255)
line_sin.SetWidth(2.0)

line_cos = chart.AddPlot(vtkChart.LINE)
line_cos.SetInputData(table, 0, 2)
line_cos.SetColor(30, 144, 255, 255)
line_cos.SetWidth(2.0)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(white_smoke_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("LinePlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
