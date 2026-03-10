#!/usr/bin/env python

# Side-by-side cosine and sine scatter plots using chart overlays.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import (
    vtkAxis,
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
alice_blue_rgb = (0.941, 0.973, 1.0)
lavender_rgb = (0.902, 0.902, 0.980)
misty_rose_rgba = (1.0, 0.894, 0.882, 1.0)
thistle_rgba = (0.847, 0.749, 0.847, 1.0)
light_grey_ub = (211, 211, 211, 255)
light_cyan_ub = (224, 255, 255, 255)
black_ub = (0, 0, 0, 255)

# Data: generate trig function values
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)

arr_cos = vtkFloatArray()
arr_cos.SetName("Cosine")
table.AddColumn(arr_cos)

arr_sin = vtkFloatArray()
arr_sin.SetName("Sine")
table.AddColumn(arr_sin)

num_points = 40
inc = 7.5 / (num_points - 1.0)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))

# ---- Left chart: cosine ----
left_chart = vtkChartXY()
left_chart.SetTitle("Cosine")
left_chart.GetBackgroundBrush().SetColorF(*misty_rose_rgba)
left_chart.GetBackgroundBrush().SetOpacityF(0.4)
left_chart.GetAxis(vtkAxis.BOTTOM).SetTitle("x")
left_chart.GetAxis(vtkAxis.BOTTOM).GetGridPen().SetColor(*light_grey_ub)
left_chart.GetAxis(vtkAxis.LEFT).SetTitle("cos(x)")
left_chart.GetAxis(vtkAxis.LEFT).GetGridPen().SetColor(*light_grey_ub)

points = left_chart.AddPlot(vtkChart.POINTS)
points.SetInputData(table, 0, 1)
points.SetColor(*black_ub)
points.SetWidth(1.0)
points.SetMarkerStyle(vtkPlotPoints.CROSS)

# ContextActor: overlay the left chart on the VTK pipeline
left_context = vtkContextActor()
left_context.GetScene().AddItem(left_chart)

# Left renderer
left_renderer = vtkRenderer()
left_renderer.SetBackground(alice_blue_rgb)
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(left_context)
left_context.GetScene().SetRenderer(left_renderer)

# ---- Right chart: sine ----
right_chart = vtkChartXY()
right_chart.SetTitle("Sine")
right_chart.GetBackgroundBrush().SetColorF(*thistle_rgba)
right_chart.GetBackgroundBrush().SetOpacityF(0.4)
right_chart.GetAxis(vtkAxis.BOTTOM).SetTitle("x")
right_chart.GetAxis(vtkAxis.BOTTOM).GetGridPen().SetColor(*light_cyan_ub)
right_chart.GetAxis(vtkAxis.LEFT).SetTitle("sin(x)")
right_chart.GetAxis(vtkAxis.LEFT).GetGridPen().SetColor(*light_cyan_ub)

points = right_chart.AddPlot(vtkChart.POINTS)
points.SetInputData(table, 0, 2)
points.SetColor(*black_ub)
points.SetWidth(1.0)
points.SetMarkerStyle(vtkPlotPoints.PLUS)

# ContextActor: overlay the right chart on the VTK pipeline
right_context = vtkContextActor()
right_context.GetScene().AddItem(right_chart)

# Right renderer
right_renderer = vtkRenderer()
right_renderer.SetBackground(lavender_rgb)
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(right_context)
right_context.GetScene().SetRenderer(right_renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("MultiplePlots")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
