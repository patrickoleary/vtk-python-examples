#!/usr/bin/env python

# Pie chart of browser market share data using a chart overlay on the VTK
# rendering pipeline.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartPie
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: browser market share percentages
label_list = ["Chrome", "Safari", "Firefox", "Edge", "Other"]
value_list = [65.0, 18.0, 7.0, 5.0, 5.0]

table = vtkTable()

arr_values = vtkFloatArray()
arr_values.SetName("Share")

arr_labels = vtkStringArray()
arr_labels.SetName("Labels")

for label, value in zip(label_list, value_list):
    arr_values.InsertNextValue(value)
    arr_labels.InsertNextValue(label)

table.AddColumn(arr_values)

# ColorSeries: use a qualitative Brewer palette for the slices
color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.BREWER_QUALITATIVE_SET2)

# Chart: create a pie chart from the share column
chart = vtkChartPie()
chart.SetTitle("Browser Market Share")
chart.SetShowLegend(True)

pie = chart.AddPlot(0)
pie.SetInputData(table)
pie.SetInputArray(0, "Share")
pie.SetLabels(arr_labels)
pie.SetColorSeries(color_series)

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
render_window.SetWindowName("PieChart")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()