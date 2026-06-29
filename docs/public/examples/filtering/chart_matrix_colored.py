#!/usr/bin/env python
# Demonstrate a 4x4 chart matrix with colored plots using vtkNamedColors.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartMatrix, vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable, vtkVector2f, vtkVector2i
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

colors = vtkNamedColors()

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

m, n = 4, 4
matrix = vtkChartMatrix()
matrix.SetSize(vtkVector2i(m, n))
matrix.SetGutter(vtkVector2f(40, 40))

warm_grey = colors.GetColor3d("warm_grey")
sea_green = colors.GetColor3ub("sea_green")
rose_madder = colors.GetColor3ub("rose_madder")
dark_orange = colors.GetColor3ub("dark_orange")
burnt_sienna = colors.GetColor3ub("burnt_sienna")
royal_blue = colors.GetColor3ub("royal_blue")

# Quadrant (i=0, j=0).
chart_00_ll = matrix.GetChart(vtkVector2i(0, 0))
plot_00_ll = chart_00_ll.AddPlot(vtkChartXY.POINTS)
plot_00_ll.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_00_ll).SetMarkerStyle(vtkPlotPoints.DIAMOND)
plot_00_ll.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ll.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ll.SetColor(sea_green.GetRed(), sea_green.GetGreen(), sea_green.GetBlue(), 255)

chart_00_ul = matrix.GetChart(vtkVector2i(0, 1))
plot_00_ul = chart_00_ul.AddPlot(vtkChartXY.POINTS)
plot_00_ul.SetInputData(table, 0, 2)
plot_00_ul.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ul.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ul.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_00_lr = matrix.GetChart(vtkVector2i(1, 0))
plot_00_lr = chart_00_lr.AddPlot(vtkChartXY.LINE)
plot_00_lr.SetInputData(table, 0, 3)
plot_00_lr.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)

chart_00_ur = matrix.GetChart(vtkVector2i(1, 1))
plot_00_ur_bar = chart_00_ur.AddPlot(vtkChartXY.BAR)
plot_00_ur_bar.SetInputData(table, 0, 4)
plot_00_ur_bar.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ur_bar.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ur_bar.SetColor(burnt_sienna.GetRed(), burnt_sienna.GetGreen(), burnt_sienna.GetBlue(), 255)
plot_00_ur_pts = chart_00_ur.AddPlot(vtkChartXY.POINTS)
plot_00_ur_pts.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_00_ur_pts).SetMarkerStyle(vtkPlotPoints.CROSS)
plot_00_ur_pts.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ur_pts.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_ur_pts.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_00_lr2 = matrix.GetChart(vtkVector2i(1, 0))
plot_00_lr2a = chart_00_lr2.AddPlot(vtkChartXY.LINE)
plot_00_lr2a.SetInputData(table, 0, 3)
plot_00_lr2a.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr2a.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr2a.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)
plot_00_lr2b = chart_00_lr2.AddPlot(vtkChartXY.LINE)
plot_00_lr2b.SetInputData(table, 0, 3)
plot_00_lr2b.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr2b.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_00_lr2b.SetColor(royal_blue.GetRed(), royal_blue.GetGreen(), royal_blue.GetBlue(), 255)

# Quadrant (i=0, j=2).
chart_02_ll = matrix.GetChart(vtkVector2i(0, 2))
plot_02_ll = chart_02_ll.AddPlot(vtkChartXY.POINTS)
plot_02_ll.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_02_ll).SetMarkerStyle(vtkPlotPoints.DIAMOND)
plot_02_ll.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ll.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ll.SetColor(sea_green.GetRed(), sea_green.GetGreen(), sea_green.GetBlue(), 255)

chart_02_ul = matrix.GetChart(vtkVector2i(0, 3))
plot_02_ul = chart_02_ul.AddPlot(vtkChartXY.POINTS)
plot_02_ul.SetInputData(table, 0, 2)
plot_02_ul.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ul.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ul.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_02_lr = matrix.GetChart(vtkVector2i(1, 2))
plot_02_lr = chart_02_lr.AddPlot(vtkChartXY.LINE)
plot_02_lr.SetInputData(table, 0, 3)
plot_02_lr.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)

chart_02_ur = matrix.GetChart(vtkVector2i(1, 3))
plot_02_ur_bar = chart_02_ur.AddPlot(vtkChartXY.BAR)
plot_02_ur_bar.SetInputData(table, 0, 4)
plot_02_ur_bar.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ur_bar.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ur_bar.SetColor(burnt_sienna.GetRed(), burnt_sienna.GetGreen(), burnt_sienna.GetBlue(), 255)
plot_02_ur_pts = chart_02_ur.AddPlot(vtkChartXY.POINTS)
plot_02_ur_pts.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_02_ur_pts).SetMarkerStyle(vtkPlotPoints.CROSS)
plot_02_ur_pts.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ur_pts.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_ur_pts.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_02_lr2 = matrix.GetChart(vtkVector2i(1, 2))
plot_02_lr2a = chart_02_lr2.AddPlot(vtkChartXY.LINE)
plot_02_lr2a.SetInputData(table, 0, 3)
plot_02_lr2a.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr2a.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr2a.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)
plot_02_lr2b = chart_02_lr2.AddPlot(vtkChartXY.LINE)
plot_02_lr2b.SetInputData(table, 0, 3)
plot_02_lr2b.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr2b.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_02_lr2b.SetColor(royal_blue.GetRed(), royal_blue.GetGreen(), royal_blue.GetBlue(), 255)

# Quadrant (i=2, j=0).
chart_20_ll = matrix.GetChart(vtkVector2i(2, 0))
plot_20_ll = chart_20_ll.AddPlot(vtkChartXY.POINTS)
plot_20_ll.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_20_ll).SetMarkerStyle(vtkPlotPoints.DIAMOND)
plot_20_ll.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ll.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ll.SetColor(sea_green.GetRed(), sea_green.GetGreen(), sea_green.GetBlue(), 255)

chart_20_ul = matrix.GetChart(vtkVector2i(2, 1))
plot_20_ul = chart_20_ul.AddPlot(vtkChartXY.POINTS)
plot_20_ul.SetInputData(table, 0, 2)
plot_20_ul.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ul.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ul.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_20_lr = matrix.GetChart(vtkVector2i(3, 0))
plot_20_lr = chart_20_lr.AddPlot(vtkChartXY.LINE)
plot_20_lr.SetInputData(table, 0, 3)
plot_20_lr.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)

chart_20_ur = matrix.GetChart(vtkVector2i(3, 1))
plot_20_ur_bar = chart_20_ur.AddPlot(vtkChartXY.BAR)
plot_20_ur_bar.SetInputData(table, 0, 4)
plot_20_ur_bar.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ur_bar.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ur_bar.SetColor(burnt_sienna.GetRed(), burnt_sienna.GetGreen(), burnt_sienna.GetBlue(), 255)
plot_20_ur_pts = chart_20_ur.AddPlot(vtkChartXY.POINTS)
plot_20_ur_pts.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_20_ur_pts).SetMarkerStyle(vtkPlotPoints.CROSS)
plot_20_ur_pts.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ur_pts.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_ur_pts.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_20_lr2 = matrix.GetChart(vtkVector2i(3, 0))
plot_20_lr2a = chart_20_lr2.AddPlot(vtkChartXY.LINE)
plot_20_lr2a.SetInputData(table, 0, 3)
plot_20_lr2a.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr2a.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr2a.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)
plot_20_lr2b = chart_20_lr2.AddPlot(vtkChartXY.LINE)
plot_20_lr2b.SetInputData(table, 0, 3)
plot_20_lr2b.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr2b.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_20_lr2b.SetColor(royal_blue.GetRed(), royal_blue.GetGreen(), royal_blue.GetBlue(), 255)

# Quadrant (i=2, j=2).
chart_22_ll = matrix.GetChart(vtkVector2i(2, 2))
plot_22_ll = chart_22_ll.AddPlot(vtkChartXY.POINTS)
plot_22_ll.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_22_ll).SetMarkerStyle(vtkPlotPoints.DIAMOND)
plot_22_ll.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ll.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ll.SetColor(sea_green.GetRed(), sea_green.GetGreen(), sea_green.GetBlue(), 255)

chart_22_ul = matrix.GetChart(vtkVector2i(2, 3))
plot_22_ul = chart_22_ul.AddPlot(vtkChartXY.POINTS)
plot_22_ul.SetInputData(table, 0, 2)
plot_22_ul.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ul.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ul.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_22_lr = matrix.GetChart(vtkVector2i(3, 2))
plot_22_lr = chart_22_lr.AddPlot(vtkChartXY.LINE)
plot_22_lr.SetInputData(table, 0, 3)
plot_22_lr.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)

chart_22_ur = matrix.GetChart(vtkVector2i(3, 3))
plot_22_ur_bar = chart_22_ur.AddPlot(vtkChartXY.BAR)
plot_22_ur_bar.SetInputData(table, 0, 4)
plot_22_ur_bar.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ur_bar.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ur_bar.SetColor(burnt_sienna.GetRed(), burnt_sienna.GetGreen(), burnt_sienna.GetBlue(), 255)
plot_22_ur_pts = chart_22_ur.AddPlot(vtkChartXY.POINTS)
plot_22_ur_pts.SetInputData(table, 0, 1)
vtkPlotPoints.SafeDownCast(plot_22_ur_pts).SetMarkerStyle(vtkPlotPoints.CROSS)
plot_22_ur_pts.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ur_pts.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_ur_pts.SetColor(rose_madder.GetRed(), rose_madder.GetGreen(), rose_madder.GetBlue(), 255)

chart_22_lr2 = matrix.GetChart(vtkVector2i(3, 2))
plot_22_lr2a = chart_22_lr2.AddPlot(vtkChartXY.LINE)
plot_22_lr2a.SetInputData(table, 0, 3)
plot_22_lr2a.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr2a.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr2a.SetColor(dark_orange.GetRed(), dark_orange.GetGreen(), dark_orange.GetBlue(), 255)
plot_22_lr2b = chart_22_lr2.AddPlot(vtkChartXY.LINE)
plot_22_lr2b.SetInputData(table, 0, 3)
plot_22_lr2b.GetXAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr2b.GetYAxis().GetGridPen().SetColorF(warm_grey.GetRed(), warm_grey.GetGreen(), warm_grey.GetBlue())
plot_22_lr2b.SetColor(royal_blue.GetRed(), royal_blue.GetGreen(), royal_blue.GetBlue(), 255)

matrix.LabelOuter(vtkVector2i(1, 1), vtkVector2i(m - 1, n - 1))

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

# Renderer
renderer = vtkRenderer()
bg = colors.GetColor3d("navajo_white")
renderer.SetBackground(bg.GetRed(), bg.GetGreen(), bg.GetBlue())
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("chart matrix colored")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
