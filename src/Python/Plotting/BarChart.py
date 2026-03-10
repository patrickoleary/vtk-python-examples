#!/usr/bin/env python

# Bar chart of quarterly revenue data using a chart overlay on the VTK pipeline.

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
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkIntArray,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: quarterly revenue for two product lines
table = vtkTable()

arr_quarter = vtkIntArray()
arr_quarter.SetName("Quarter")
table.AddColumn(arr_quarter)

arr_product_a = vtkFloatArray()
arr_product_a.SetName("Product A")
table.AddColumn(arr_product_a)

arr_product_b = vtkFloatArray()
arr_product_b.SetName("Product B")
table.AddColumn(arr_product_b)

quarters = [1, 2, 3, 4]
product_a = [12.5, 18.3, 15.7, 22.1]
product_b = [8.2, 14.6, 19.4, 16.8]

table.SetNumberOfRows(4)
for i in range(4):
    table.SetValue(i, 0, quarters[i])
    table.SetValue(i, 1, product_a[i])
    table.SetValue(i, 2, product_b[i])

# Chart: create a 2D XY chart with grouped bar series
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.SetTitle("Quarterly Revenue")

bar_a = chart.AddPlot(vtkChart.BAR)
bar_a.SetInputData(table, 0, 1)
bar_a.SetColor(65, 105, 225, 255)

bar_b = chart.AddPlot(vtkChart.BAR)
bar_b.SetInputData(table, 0, 2)
bar_b.SetColor(220, 20, 60, 255)

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
render_window.SetWindowName("BarChart")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
