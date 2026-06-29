#!/usr/bin/env python
# Demonstrate a pie chart with labeled slices using vtkChartPie.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartPie, vtkPlotPie
from vtkmodules.vtkCommonColor import vtkColorSeries
from vtkmodules.vtkCommonCore import vtkIntArray, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data for the pie chart.
data = [77938, 9109, 2070, 12806, 19514]
label_strings = ["Books", "New and Popular", "Periodical", "Audiobook", "Video"]

# Create a table.
table = vtkTable()

arr_data = vtkIntArray()
arr_data.SetName("2008 Circulation")
for val in data:
    arr_data.InsertNextValue(val)

label_array = vtkStringArray()
for lbl in label_strings:
    label_array.InsertNextValue(lbl)

table.AddColumn(arr_data)

# Create a color series.
color_series = vtkColorSeries()
color_series.SetColorScheme(vtkColorSeries.WARM)

# Set up a chart.
chart = vtkChartPie()

pie = vtkPlotPie.SafeDownCast(chart.AddPlot(0))
pie.SetColorSeries(color_series)
pie.SetInputData(table)
pie.SetInputArray(0, "2008 Circulation")
pie.SetLabels(label_array)

chart.SetShowLegend(True)
chart.SetTitle("Circulation 2008")

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
render_window.SetSize(600, 350)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("pie test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
