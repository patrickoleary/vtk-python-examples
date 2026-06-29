#!/usr/bin/env python
# Demonstrate functional bag plots with quantile bands and per-column line plots.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartLegend, vtkChartXY, vtkPlotFunctionalBag
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create an input table.
num_cols = 7
num_vals = 100

input_table = vtkTable()

arr_y0 = vtkDoubleArray()
arr_y0.SetName("Y0")
arr_y0.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y0.SetValue(j, 1 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 0)
input_table.AddColumn(arr_y0)

arr_y1 = vtkDoubleArray()
arr_y1.SetName("Y1")
arr_y1.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y1.SetValue(j, 2 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 20)
input_table.AddColumn(arr_y1)

arr_y2 = vtkDoubleArray()
arr_y2.SetName("Y2")
arr_y2.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y2.SetValue(j, 3 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 40)
input_table.AddColumn(arr_y2)

arr_y3 = vtkDoubleArray()
arr_y3.SetName("Y3")
arr_y3.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y3.SetValue(j, 4 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 60)
input_table.AddColumn(arr_y3)

arr_y4 = vtkDoubleArray()
arr_y4.SetName("Y4")
arr_y4.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y4.SetValue(j, 5 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 80)
input_table.AddColumn(arr_y4)

arr_y5 = vtkDoubleArray()
arr_y5.SetName("Y5")
arr_y5.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y5.SetValue(j, 6 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 100)
input_table.AddColumn(arr_y5)

arr_y6 = vtkDoubleArray()
arr_y6.SetName("Y6")
arr_y6.SetNumberOfValues(num_vals)
for j in range(num_vals):
    arr_y6.SetValue(j, 7 * abs(math.sin((j * 2.0 * math.pi) / float(num_vals))) * j + 120)
input_table.AddColumn(arr_y6)

arrays = [arr_y0, arr_y1, arr_y2, arr_y3, arr_y4, arr_y5, arr_y6]

# Create an X-axis column.
x_arr = vtkDoubleArray()
x_arr.SetName("X")
x_arr.SetNumberOfValues(num_vals)
for j in range(num_vals):
    x_arr.SetValue(j, j * 2.0)
input_table.AddColumn(x_arr)

# Create the bag columns.
q3_arr = vtkDoubleArray()
q3_arr.SetName("Q3")
q3_arr.SetNumberOfComponents(2)
q3_arr.SetNumberOfTuples(num_vals)

q2_arr = vtkDoubleArray()
q2_arr.SetName("Q2")
q2_arr.SetNumberOfComponents(2)
q2_arr.SetNumberOfTuples(num_vals)

for i in range(num_vals):
    v0 = arrays[1].GetValue(i)
    v1 = arrays[5].GetValue(i)
    q3_arr.SetTuple2(i, v0, v1)

    v0 = arrays[2].GetValue(i)
    v1 = arrays[4].GetValue(i)
    q2_arr.SetTuple2(i, v0, v1)

input_table.AddColumn(q3_arr)
input_table.AddColumn(q2_arr)

# Set up a chart.
chart = vtkChartXY()
chart.SetShowLegend(True)
chart.GetLegend().SetHorizontalAlignment(vtkChartLegend.LEFT)
chart.GetLegend().SetVerticalAlignment(vtkChartLegend.TOP)

# Create functional bag plots for quantile bands.
q3_plot = vtkPlotFunctionalBag()
q3_plot.SetColorF(0.5, 0, 0)
q3_plot.SetInputData(input_table, "X", "Q3")
chart.AddPlot(q3_plot)

q2_plot = vtkPlotFunctionalBag()
q2_plot.SetColorF(1.0, 0, 0)
q2_plot.SetInputData(input_table, "X", "Q2")
chart.AddPlot(q2_plot)

# Add individual line plots with lookup table colors.
lookup = vtkLookupTable()
lookup.SetNumberOfColors(num_cols)
lookup.SetRange(0, num_cols - 1)
lookup.Build()
rgb_0 = [0.0, 0.0, 0.0]
lookup.GetColor(0, rgb_0)
plot_0 = vtkPlotFunctionalBag()
plot_0.SetColorF(rgb_0[0], rgb_0[1], rgb_0[2])
plot_0.SetInputData(input_table, "X", "Y0")
chart.AddPlot(plot_0)

rgb_1 = [0.0, 0.0, 0.0]
lookup.GetColor(1, rgb_1)
plot_1 = vtkPlotFunctionalBag()
plot_1.SetColorF(rgb_1[0], rgb_1[1], rgb_1[2])
plot_1.SetInputData(input_table, "X", "Y1")
chart.AddPlot(plot_1)

rgb_2 = [0.0, 0.0, 0.0]
lookup.GetColor(2, rgb_2)
plot_2 = vtkPlotFunctionalBag()
plot_2.SetColorF(rgb_2[0], rgb_2[1], rgb_2[2])
plot_2.SetInputData(input_table, "X", "Y2")
chart.AddPlot(plot_2)

rgb_3 = [0.0, 0.0, 0.0]
lookup.GetColor(3, rgb_3)
plot_3 = vtkPlotFunctionalBag()
plot_3.SetColorF(rgb_3[0], rgb_3[1], rgb_3[2])
plot_3.SetInputData(input_table, "X", "Y3")
chart.AddPlot(plot_3)

rgb_4 = [0.0, 0.0, 0.0]
lookup.GetColor(4, rgb_4)
plot_4 = vtkPlotFunctionalBag()
plot_4.SetColorF(rgb_4[0], rgb_4[1], rgb_4[2])
plot_4.SetInputData(input_table, "X", "Y4")
chart.AddPlot(plot_4)

rgb_5 = [0.0, 0.0, 0.0]
lookup.GetColor(5, rgb_5)
plot_5 = vtkPlotFunctionalBag()
plot_5.SetColorF(rgb_5[0], rgb_5[1], rgb_5[2])
plot_5.SetInputData(input_table, "X", "Y5")
chart.AddPlot(plot_5)

rgb_6 = [0.0, 0.0, 0.0]
lookup.GetColor(6, rgb_6)
plot_6 = vtkPlotFunctionalBag()
plot_6.SetColorF(rgb_6[0], rgb_6[1], rgb_6[2])
plot_6.SetInputData(input_table, "X", "Y6")
chart.AddPlot(plot_6)

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
render_window.SetWindowName("functional bag plot")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
