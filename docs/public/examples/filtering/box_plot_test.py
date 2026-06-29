#!/usr/bin/env python
# Demonstrate a box plot with labeled columns using vtkChartBox.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartBox, vtkPlotBox
from vtkmodules.vtkCommonCore import vtkIntArray, vtkLookupTable, vtkStringArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create the input table for the box plot.
num_param = 5
table = vtkTable()

arr_0 = vtkIntArray()
arr_0.SetName("P0")
table.AddColumn(arr_0)

arr_1 = vtkIntArray()
arr_1.SetName("P1")
table.AddColumn(arr_1)

arr_2 = vtkIntArray()
arr_2.SetName("P2")
table.AddColumn(arr_2)

arr_3 = vtkIntArray()
arr_3.SetName("P3")
table.AddColumn(arr_3)

arr_4 = vtkIntArray()
arr_4.SetName("P4")
table.AddColumn(arr_4)

table.SetNumberOfRows(5)

# Scaling parameter.
scale = 1e02

table.SetValue(0, 0, int(0 * scale))          # Q0
table.SetValue(1, 0, int(2 * scale))           # Q1
table.SetValue(2, 0, int(4 * scale))           # Q2
table.SetValue(3, 0, int(7 * scale))           # Q3
table.SetValue(4, 0, int(8 * scale))           # Q4

table.SetValue(0, 1, int(0 * scale))          # Q0
table.SetValue(1, 1, int(3 * scale))           # Q1
table.SetValue(2, 1, int(6 * scale))           # Q2
table.SetValue(3, 1, int(9 * scale))           # Q3
table.SetValue(4, 1, int(10 * scale))          # Q4

table.SetValue(0, 2, int(1 * scale))          # Q0
table.SetValue(1, 2, int(4 * scale))           # Q1
table.SetValue(2, 2, int(8 * scale))           # Q2
table.SetValue(3, 2, int(11 * scale))          # Q3
table.SetValue(4, 2, int(12 * scale))          # Q4

table.SetValue(0, 3, int(1 * scale))          # Q0
table.SetValue(1, 3, int(5 * scale))           # Q1
table.SetValue(2, 3, int(10 * scale))          # Q2
table.SetValue(3, 3, int(13 * scale))          # Q3
table.SetValue(4, 3, int(14 * scale))          # Q4

table.SetValue(0, 4, int(2 * scale))          # Q0
table.SetValue(1, 4, int(6 * scale))           # Q1
table.SetValue(2, 4, int(12 * scale))          # Q2
table.SetValue(3, 4, int(15 * scale))          # Q3
table.SetValue(4, 4, int(16 * scale))          # Q4

lookup = vtkLookupTable()
lookup.SetNumberOfColors(5)
lookup.SetRange(0, 4)
lookup.Build()

# Set up the chart.
chart = vtkChartBox()
chart.GetPlot(0).SetInputData(table)
chart.SetColumnVisibilityAll(True)
chart.SetShowLegend(True)

# Hide one box plot.
chart.SetColumnVisibility(3, False)

# Set the labels.
labels = vtkStringArray()
labels.SetNumberOfValues(5)
labels.SetValue(0, "Param 0")
labels.SetValue(1, "Param 1")
labels.SetValue(2, "Param 2")
labels.SetValue(3, "Param 3")
labels.SetValue(4, "Param 4")
chart.GetPlot(0).SetLabels(labels)

# Manually change the color of one series.
vtkPlotBox.SafeDownCast(chart.GetPlot(0)).SetColumnColor("P1", (0.5, 0.5, 0.5))

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
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("box plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
