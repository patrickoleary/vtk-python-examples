#!/usr/bin/env python
# Demonstrate chart with scalar color mapping on points and bars.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY, vtkPlotBar, vtkPlotLine, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkPen
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkDoubleArray()
arr_x.SetName("X")
table.AddColumn(arr_x)
arr_c = vtkDoubleArray()
arr_c.SetName("f1")
table.AddColumn(arr_c)
arr_s = vtkDoubleArray()
arr_s.SetName("f2")
table.AddColumn(arr_s)
arr_s2 = vtkDoubleArray()
arr_s2.SetName("f3")
table.AddColumn(arr_s2)
arr_color = vtkDoubleArray()
arr_color.SetName("color")
table.AddColumn(arr_color)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc + 0.2
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, 1.0e-80 * (math.cos(x - 1.0) + math.sin(x - math.pi / 4.0)))
    table.SetValue(i, 2, 1.0e-80 * math.sin(x) * 1e-12)
    table.SetValue(i, 3, 1.0e-80 * math.sin(x - 1.0))
    table.SetValue(i, 4, math.cos(i * inc))

# Create a lookup table.
lut = vtkLookupTable()
lut.SetValueRange(0.0, 1.0)
lut.SetSaturationRange(1.0, 1.0)
lut.SetHueRange(0.4, 0.9)
lut.SetAlphaRange(0.2, 0.8)
lut.SetRange(-1.0, 1.0)
lut.SetRampToLinear()
lut.Build()

# Set up a chart.
chart = vtkChartXY()

points = vtkPlotPoints()
chart.AddPlot(points)
points.SetInputData(table, 0, 1)
points.SetMarkerSize(10.0)
points.ScalarVisibilityOn()
points.SelectColorArray("color")
points.SetLookupTable(lut)

line = vtkPlotLine()
chart.AddPlot(line)
line.SetInputData(table, 0, 2)
line.SetColorF(1.0, 0.0, 0.0)
# Put this plot in a different corner.
chart.SetPlotCorner(line, 1)

bar = vtkPlotBar()
chart.AddPlot(bar)
bar.SetInputData(table, 0, 3)
bar.ScalarVisibilityOn()
bar.SelectColorArray("color")
bar.SetLookupTable(lut)
bar.GetPen().SetLineType(vtkPen.NO_PEN)

chart.GetAxis(vtkAxis.LEFT).SetTitle("A tiny range")
chart.GetAxis(vtkAxis.BOTTOM).SetTitle("A normal range")
chart.GetAxis(vtkAxis.RIGHT).SetTitle("An even tinier range")
chart.SetBarWidthFraction(1.0)

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
render_window.SetWindowName("chart double colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
