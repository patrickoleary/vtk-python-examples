#!/usr/bin/env python
# Demonstrate chart picking of various items including axes, plots, range handles, and legend.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkAxis,
    vtkChartXY,
    vtkPlotBar,
    vtkPlotRangeHandlesItem,
)
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)

num_points = 12
table.SetNumberOfRows(num_points)
for i in range(1, num_points + 1):
    table.SetValue(i - 1, 0, i)
    table.SetValue(i - 1, 1, i)

# Set up a chart.
chart = vtkChartXY()

line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)
line.SetWidth(1.0)
line.SetLegendVisibility(True)

# Add vertical range handles.
range_item = vtkPlotRangeHandlesItem()
range_item.SetExtent(0, 12, 0, 30)
chart.AddPlot(range_item)

# Add horizontal range handles.
h_range_item = vtkPlotRangeHandlesItem()
h_range_item.SetHandleOrientationToHorizontal()
chart.AddPlot(h_range_item)
chart.RaisePlot(h_range_item)

chart.GetAxis(vtkAxis.TOP).SetVisible(True)
chart.GetAxis(vtkAxis.RIGHT).SetVisible(True)
chart.GetAxis(vtkAxis.BOTTOM).SetVisible(False)
chart.DrawAxesAtOriginOff()
chart.AutoAxesOff()

# Add a bar plot.
plot_bar_table = vtkTable()
arr_month = vtkIntArray()
arr_month.SetNumberOfComponents(1)
arr_month.SetName("Month")
for i in range(1, 12):
    arr_month.InsertNextTuple1(i)
plot_bar_table.AddColumn(arr_month)

books = [6, 9, 3, 9, 5, 3, 8, 0, 4, 9, 5, 1]
arr_books = vtkIntArray()
arr_books.SetName("Books")
for i in range(1, 12):
    arr_books.InsertNextTuple1(books[i])
plot_bar_table.AddColumn(arr_books)

bar1 = vtkPlotBar.SafeDownCast(chart.AddPlot(vtkChartXY.BAR))
bar1.SetInputData(plot_bar_table, "Month", "Books")

chart.RaisePlot(range_item)
chart.RaisePlot(h_range_item)
chart.RaisePlot(line)
chart.SetShowLegend(True)

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
render_window.SetWindowName("chart picking")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
