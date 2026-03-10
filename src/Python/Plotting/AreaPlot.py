#!/usr/bin/env python

# Plot of a damped sine wave with its decay envelope using a chart overlay.

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

# Data: a damped sine wave with upper and lower envelopes
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X")
table.AddColumn(arr_x)

arr_signal = vtkFloatArray()
arr_signal.SetName("Signal")
table.AddColumn(arr_signal)

arr_upper = vtkFloatArray()
arr_upper.SetName("Upper Envelope")
table.AddColumn(arr_upper)

arr_lower = vtkFloatArray()
arr_lower.SetName("Lower Envelope")
table.AddColumn(arr_lower)

num_points = 100
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * 6.0 * math.pi / (num_points - 1)
    decay = math.exp(-0.15 * x)
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, decay * math.sin(x))
    table.SetValue(i, 2, decay)
    table.SetValue(i, 3, -decay)

# Chart: create a 2D XY chart with signal and envelope lines
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.SetTitle("Damped Oscillation")

# Signal line
signal = chart.AddPlot(vtkChart.LINE)
signal.SetInputData(table, 0, 1)
signal.SetColor(66, 133, 244, 255)
signal.SetWidth(2.0)

# Upper envelope (dashed)
upper = chart.AddPlot(vtkChart.LINE)
upper.SetInputData(table, 0, 2)
upper.SetColor(220, 20, 60, 200)
upper.SetWidth(1.5)
upper.GetPen().SetLineType(2)

# Lower envelope (dashed)
lower = chart.AddPlot(vtkChart.LINE)
lower.SetInputData(table, 0, 3)
lower.SetColor(220, 20, 60, 200)
lower.SetWidth(1.5)
lower.GetPen().SetLineType(2)

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
render_window.SetWindowName("AreaPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
