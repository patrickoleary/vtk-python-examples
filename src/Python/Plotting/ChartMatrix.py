#!/usr/bin/env python

# Grid of four sub-charts using vtkChartMatrix as a chart overlay.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartMatrix,
    vtkChartXY,
    vtkPlotPoints,
)
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkTable,
    vtkVector2f,
    vtkVector2i,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: generate trig function values
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X")
table.AddColumn(arr_x)

arr_sin = vtkFloatArray()
arr_sin.SetName("sin(x)")
table.AddColumn(arr_sin)

arr_cos = vtkFloatArray()
arr_cos.SetName("cos(x)")
table.AddColumn(arr_cos)

arr_tan = vtkFloatArray()
arr_tan.SetName("sin(2x)")
table.AddColumn(arr_tan)

arr_exp = vtkFloatArray()
arr_exp.SetName("cos(2x)")
table.AddColumn(arr_exp)

num_points = 60
inc = 2.0 * math.pi / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, math.sin(x))
    table.SetValue(i, 2, math.cos(x))
    table.SetValue(i, 3, math.sin(2 * x))
    table.SetValue(i, 4, math.cos(2 * x))

# ChartMatrix: create a 2x2 grid of sub-charts
matrix = vtkChartMatrix()
matrix.SetSize(vtkVector2i(2, 2))
matrix.SetGutter(vtkVector2f(40, 40))

# Define chart configs: (row, col, plot_type, data_col, color_rgba, title)
chart_configs = [
    (0, 0, vtkChart.LINE, 1, (220, 20, 60, 255), "sin(x)"),
    (0, 1, vtkChart.LINE, 2, (30, 144, 255, 255), "cos(x)"),
    (1, 0, vtkChart.POINTS, 3, (34, 139, 34, 255), "sin(2x)"),
    (1, 1, vtkChart.POINTS, 4, (255, 140, 0, 255), "cos(2x)"),
]

for row, col, plot_type, data_col, color, title in chart_configs:
    chart = matrix.GetChart(vtkVector2i(col, row))
    chart.SetTitle(title)
    plot = chart.AddPlot(plot_type)
    plot.SetInputData(table, 0, data_col)
    plot.SetColor(*color)
    plot.SetWidth(2.0)
    if plot_type == vtkChart.POINTS:
        plot.SetMarkerStyle(vtkPlotPoints.CIRCLE)

# ContextActor: overlay the chart matrix on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(white_smoke_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 600)
render_window.SetMultiSamples(0)
render_window.SetWindowName("ChartMatrix")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
