#!/usr/bin/env python
# Demonstrate a chart matrix with sub-matrices and chart spanning.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartMatrix, vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRecti, vtkTable, vtkVector2f, vtkVector2i
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)
arr_s2 = vtkFloatArray()
arr_s2.SetName("Sine2")
table.AddColumn(arr_s2)
tangent = vtkFloatArray()
tangent.SetName("Tangent")
table.AddColumn(tangent)

num_points = 42
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.sin(i * inc) + 0.5)
    table.SetValue(i, 4, math.tan(i * inc))

# Set up a chart matrix.
matrix = vtkChartMatrix()
matrix.SetRect(vtkRecti(10, 10, 390, 390))
matrix.SetSize(vtkVector2i(2, 3))
matrix.SetGutter(vtkVector2f(30.0, 30.0))

# Bottom-left: points of cosine.
chart = matrix.GetChart(vtkVector2i(0, 0))
line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)

# Middle-left: points of sine.
chart = matrix.GetChart(vtkVector2i(0, 1))
line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)

# Top-left: points of sine.
chart = matrix.GetChart(vtkVector2i(0, 2))
line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)

# Bottom-right: line of sine2.
chart = matrix.GetChart(vtkVector2i(1, 0))
line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 3)
line.SetColor(0, 0, 255, 255)

# Sub-matrix spanning (1,1) to (1,2).
sub_matrix = matrix.GetChartMatrix(vtkVector2i(1, 1))
matrix.SetChartSpan(vtkVector2i(1, 1), vtkVector2i(1, 2))
sub_matrix.SetGutter(vtkVector2f(30.0, 30.0))
sub_matrix.SetBorders(0, 0, 0, 0)
sub_matrix.SetSize(vtkVector2i(1, 3))

chart = sub_matrix.GetChart(vtkVector2i(0, 0))
line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 1)
line.SetColor(0, 255, 0, 255)

chart = sub_matrix.GetChart(vtkVector2i(0, 1))
line = chart.AddPlot(vtkChartXY.POINTS)
line.SetInputData(table, 0, 2)
line.SetColor(255, 0, 0, 255)

chart = sub_matrix.GetChart(vtkVector2i(0, 2))
line = chart.AddPlot(vtkChartXY.LINE)
line.SetInputData(table, 0, 3)
line.SetColor(0, 0, 255, 255)

sub_matrix.LabelOuter(vtkVector2i(0, 0), vtkVector2i(0, 2))

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

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
render_window.SetWindowName("chart matrix spanning")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
