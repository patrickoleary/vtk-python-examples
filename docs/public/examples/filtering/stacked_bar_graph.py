#!/usr/bin/env python
# Demonstrate stacked bar graphs with library circulation data and custom month labels.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartLegend, vtkChartXY, vtkPlotBar
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
month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]

book_2008 = [5675, 5902, 6388, 5990, 5575, 7393, 9878, 8082, 6417, 5946, 5526, 5166]
new_popular_2008 = [701, 687, 736, 696, 750, 814, 923, 860, 786, 735, 680, 741]
periodical_2008 = [184, 176, 166, 131, 171, 191, 231, 166, 197, 162, 152, 143]
audiobook_2008 = [903, 1038, 987, 1073, 1144, 1203, 1173, 1196, 1213, 1076, 926, 874]
video_2008 = [1524, 1565, 1627, 1445, 1179, 1816, 2293, 1811, 1588, 1561, 1542, 1563]

book_2009 = [6388, 5990, 5575, 9878, 8082, 5675, 7393, 5902, 5526, 5166, 5946, 6417]
new_popular_2009 = [696, 735, 786, 814, 736, 860, 750, 687, 923, 680, 741, 701]
periodical_2009 = [197, 166, 176, 231, 171, 152, 166, 131, 184, 191, 143, 162]
audiobook_2009 = [1213, 1076, 926, 987, 903, 1196, 1073, 1144, 1203, 1038, 874, 1173]
video_2009 = [2293, 1561, 1542, 1627, 1588, 1179, 1563, 1445, 1811, 1565, 1524, 1816]

arr_month = vtkIntArray()
arr_month.SetName("Month")
for v in month:
    arr_month.InsertNextValue(v)

arr_book_2008 = vtkIntArray()
arr_book_2008.SetName("Books 2008")
for v in book_2008:
    arr_book_2008.InsertNextValue(v)

arr_new_popular_2008 = vtkIntArray()
arr_new_popular_2008.SetName("New / Popular 2008")
for v in new_popular_2008:
    arr_new_popular_2008.InsertNextValue(v)

arr_periodical_2008 = vtkIntArray()
arr_periodical_2008.SetName("Periodical 2008")
for v in periodical_2008:
    arr_periodical_2008.InsertNextValue(v)

arr_audiobook_2008 = vtkIntArray()
arr_audiobook_2008.SetName("Audiobook 2008")
for v in audiobook_2008:
    arr_audiobook_2008.InsertNextValue(v)

arr_video_2008 = vtkIntArray()
arr_video_2008.SetName("Video 2008")
for v in video_2008:
    arr_video_2008.InsertNextValue(v)

arr_book_2009 = vtkIntArray()
arr_book_2009.SetName("Books 2009")
for v in book_2009:
    arr_book_2009.InsertNextValue(v)

arr_new_popular_2009 = vtkIntArray()
arr_new_popular_2009.SetName("New / Popular 2009")
for v in new_popular_2009:
    arr_new_popular_2009.InsertNextValue(v)

arr_periodical_2009 = vtkIntArray()
arr_periodical_2009.SetName("Periodical 2009")
for v in periodical_2009:
    arr_periodical_2009.InsertNextValue(v)

arr_audiobook_2009 = vtkIntArray()
arr_audiobook_2009.SetName("Audiobook 2009")
for v in audiobook_2009:
    arr_audiobook_2009.InsertNextValue(v)

arr_video_2009 = vtkIntArray()
arr_video_2009.SetName("Video 2009")
for v in video_2009:
    arr_video_2009.InsertNextValue(v)

# Create the table.
table = vtkTable()
table.AddColumn(arr_month)
table.AddColumn(arr_book_2008)
table.AddColumn(arr_new_popular_2008)
table.AddColumn(arr_periodical_2008)
table.AddColumn(arr_audiobook_2008)
table.AddColumn(arr_video_2008)
table.AddColumn(arr_book_2009)
table.AddColumn(arr_new_popular_2009)
table.AddColumn(arr_periodical_2009)
table.AddColumn(arr_audiobook_2009)
table.AddColumn(arr_video_2009)

# Set up the chart.
chart = vtkChartXY()

# Stacked bar for 2008.
color_series_1 = vtkColorSeries()
color_series_1.SetColorScheme(vtkColorSeries.WILD_FLOWER)

bar = vtkPlotBar.SafeDownCast(chart.AddPlot(vtkChartXY.BAR))
bar.SetColorSeries(color_series_1)
bar.SetInputData(table, "Month", "Books 2008")
bar.SetInputArray(2, "New / Popular 2008")
bar.SetInputArray(3, "Periodical 2008")
bar.SetInputArray(4, "Audiobook 2008")
bar.SetInputArray(5, "Video 2008")

# Stacked bar for 2009.
color_series_2 = vtkColorSeries()
color_series_2.SetColorScheme(vtkColorSeries.WILD_FLOWER)

bar = vtkPlotBar.SafeDownCast(chart.AddPlot(vtkChartXY.BAR))
bar.SetColorSeries(color_series_2)
bar.SetInputData(table, "Month", "Books 2009")
bar.SetInputArray(2, "New / Popular 2009")
bar.SetInputArray(3, "Periodical 2009")
bar.SetInputArray(4, "Audiobook 2009")
bar.SetInputArray(5, "Video 2009")

chart.SetShowLegend(True)
axis = chart.GetAxis(vtkAxis.BOTTOM)
axis.SetBehavior(1)
axis.SetMaximum(13.0)
axis.SetTitle("Month")
chart.GetAxis(vtkAxis.LEFT).SetTitle("")
chart.SetTitle("Circulation 2008, 2009")

# Legend placement.
chart.GetLegend().SetInline(False)
chart.GetLegend().SetHorizontalAlignment(vtkChartLegend.RIGHT)
chart.GetLegend().SetVerticalAlignment(vtkChartLegend.TOP)

# Custom month labels.
dates = vtkDoubleArray()
strings = vtkStringArray()
month_names = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]
for i, name in enumerate(month_names):
    dates.InsertNextValue(i + 1)
    strings.InsertNextValue(name)
axis.SetCustomTickPositions(dates, strings)
axis.GetLabelProperties().SetOrientation(90)
axis.GetLabelProperties().SetVerticalJustification(1)  # VTK_TEXT_CENTERED
axis.GetLabelProperties().SetJustification(2)  # VTK_TEXT_RIGHT

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
render_window.SetSize(500, 350)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("stacked bar graph")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
