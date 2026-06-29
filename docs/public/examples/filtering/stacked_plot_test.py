#!/usr/bin/env python
# Demonstrate a stacked area chart with library circulation data and custom month labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY, vtkPlotStacked
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIntArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data arrays.
month_labels = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
book = [5675, 5902, 6388, 5990, 5575, 7393, 9878, 8082, 6417, 5946, 5526, 5166]
new_popular = [701, 687, 736, 696, 750, 814, 923, 860, 786, 735, 680, 741]
periodical = [184, 176, 166, 131, 171, 191, 231, 166, 197, 162, 152, 143]
audiobook = [903, 1038, 987, 1073, 1144, 1203, 1173, 1196, 1213, 1076, 926, 874]
video = [1524, 1565, 1627, 1445, 1179, 1816, 2293, 1811, 1588, 1561, 1542, 1563]

# Create the table.
table = vtkTable()

arr_month_label = vtkStringArray()
arr_month_label.SetNumberOfValues(12)
arr_x_tick_positions = vtkDoubleArray()
arr_x_tick_positions.SetNumberOfValues(12)

arr_month = vtkIntArray()
arr_month.SetName("Month")
table.AddColumn(arr_month)

arr_book = vtkIntArray()
arr_book.SetName("Books")
table.AddColumn(arr_book)

arr_new_popular = vtkIntArray()
arr_new_popular.SetName("New / Popular")
table.AddColumn(arr_new_popular)

arr_periodical = vtkIntArray()
arr_periodical.SetName("Periodical")
table.AddColumn(arr_periodical)

arr_audiobook = vtkIntArray()
arr_audiobook.SetName("Audiobook")
table.AddColumn(arr_audiobook)

arr_video = vtkIntArray()
arr_video.SetName("Video")
table.AddColumn(arr_video)

table.SetNumberOfRows(12)
for i in range(12):
    arr_month_label.SetValue(i, month_labels[i])
    arr_x_tick_positions.SetValue(i, i)
    arr_book.SetValue(i, book[i])
    arr_new_popular.SetValue(i, new_popular[i])
    arr_periodical.SetValue(i, periodical[i])
    arr_audiobook.SetValue(i, audiobook[i])
    arr_video.SetValue(i, video[i])

# Set up the chart.
chart = vtkChartXY()

chart.GetAxis(1).SetCustomTickPositions(arr_x_tick_positions, arr_month_label)
chart.GetAxis(1).SetRange(0, 11)
chart.GetAxis(1).SetBehavior(vtkAxis.FIXED)
chart.SetShowLegend(True)

# Stacked plot.
stack = vtkPlotStacked.SafeDownCast(chart.AddPlot(vtkChartXY.STACKED))
stack.SetUseIndexForXSeries(True)
stack.SetInputData(table)
stack.SetInputArray(1, "Books")
stack.SetInputArray(2, "New / Popular")
stack.SetInputArray(3, "Periodical")
stack.SetInputArray(4, "Audiobook")
stack.SetInputArray(5, "Video")

color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.COOL)
stack.SetColorSeries(color_series)

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
render_window.SetWindowName("stacked plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
