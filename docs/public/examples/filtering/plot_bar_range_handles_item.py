#!/usr/bin/env python
# Demonstrate bar plot range handles with vertical and horizontal orientation and event replay.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkAxis,
    vtkChartXY,
    vtkPlotBar,
    vtkPlotBarRangeHandlesItem,
)
from vtkmodules.vtkCommonCore import vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create table data.
table = vtkTable()

arr_month = vtkIntArray()
arr_month.SetName("Months")
arr_month.SetNumberOfComponents(1)
arr_month.SetNumberOfTuples(12)
for i in range(12):
    arr_month.SetValue(i, i)
table.AddColumn(arr_month)

books = [5675, 5902, 6388, 5990, 5575, 7393, 9878, 8082, 6417, 5946, 5526, 5166]
arr_books = vtkIntArray()
arr_books.SetName("Books")
arr_books.SetNumberOfComponents(1)
arr_books.SetNumberOfTuples(12)
for i in range(12):
    arr_books.SetValue(i, books[i])
table.AddColumn(arr_books)

# Set up chart and scene.
chart = vtkChartXY()
chart.GetAxis(vtkAxis.BOTTOM).SetRange(-5, 15)
chart.GetAxis(vtkAxis.LEFT).SetRange(-5, 15)

# Context actor and scene wiring.
context_actor = vtkContextActor()
scene = context_actor.GetScene()
scene.AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
scene.SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 350)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("plot bar range handles item")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Add bar plot and range handles.
bar_plot = vtkPlotBar.SafeDownCast(chart.AddPlot(vtkChartXY.BAR))
bar_plot.GetLookupTable()
bar_plot.SetInputData(table, "Months", "Books")
chart.SetBarWidthFraction(1.0)

range_item = vtkPlotBarRangeHandlesItem()
range_item.SetPlotBar(bar_plot)
range_item.SetExtent(0, 12, 0, 1)
chart.AddPlot(range_item)
range_item.ComputeHandlesDrawRange()
chart.RaisePlot(range_item)
chart.Update()

interactor.Initialize()
interactor.Start()
