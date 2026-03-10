#!/usr/bin/env python

# Stacked area plot of three data series using a chart overlay on the VTK pipeline.

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
    vtkPlotStacked,
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

# Data: three positive-valued series that stack
table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("Month")
table.AddColumn(arr_x)

arr_a = vtkFloatArray()
arr_a.SetName("Desktop")
table.AddColumn(arr_a)

arr_b = vtkFloatArray()
arr_b.SetName("Mobile")
table.AddColumn(arr_b)

arr_c = vtkFloatArray()
arr_c.SetName("Tablet")
table.AddColumn(arr_c)

num_points = 12
table.SetNumberOfRows(num_points)
for i in range(num_points):
    t = i * 2.0 * math.pi / (num_points - 1)
    table.SetValue(i, 0, i + 1)
    table.SetValue(i, 1, 40 + 10 * math.sin(t))
    table.SetValue(i, 2, 25 + 8 * math.cos(t + 1.0))
    table.SetValue(i, 3, 15 + 5 * math.sin(t + 2.0))

# Chart: create a 2D XY chart with stacked area series
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.SetTitle("Web Traffic by Device")

stack_a = chart.AddPlot(vtkChart.STACKED)
stack_a.SetInputData(table, 0, 1)
stack_a.SetColor(70, 130, 180, 200)

stack_b = chart.AddPlot(vtkChart.STACKED)
stack_b.SetInputData(table, 0, 2)
stack_b.SetColor(60, 179, 113, 200)

stack_c = chart.AddPlot(vtkChart.STACKED)
stack_c.SetInputData(table, 0, 3)
stack_c.SetColor(255, 165, 0, 200)

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
render_window.SetWindowName("StackedPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
