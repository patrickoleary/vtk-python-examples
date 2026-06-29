#!/usr/bin/env python
# Demonstrate bar graphs with shift/scale in two side-by-side viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotBar
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Monthly circulation data.
data_2008 = [10822, 10941, 9979, 10370, 9460, 11228, 15093, 12231, 10160, 9816, 9384, 7892]
data_2009 = [9058, 9474, 9979, 9408, 8900, 11569, 14688, 12231, 10294, 9585, 8957, 8590]
data_2010 = [9058, 10941, 9979, 10270, 8900, 11228, 14688, 12231, 10160, 9585, 9384, 8590]

# Create a table with some points in it.
table = vtkTable()

arr_month = vtkDoubleArray()
arr_month.SetName("Month")
table.AddColumn(arr_month)

arr_2008 = vtkIntArray()
arr_2008.SetName("2008")
table.AddColumn(arr_2008)

arr_2009 = vtkIntArray()
arr_2009.SetName("2009")
table.AddColumn(arr_2009)

arr_2010 = vtkIntArray()
arr_2010.SetName("2010")
table.AddColumn(arr_2010)

table.SetNumberOfRows(2)
for i in range(2):
    arr_month.SetValue(i, (i + 3) * 1e20 + 1e24)
    arr_2008.SetValue(i, data_2008[i] + 2000000)
    arr_2009.SetValue(i, int(data_2009[i] * 1e2))
    arr_2010.SetValue(i, data_2010[i] + 3000000)

# Left chart: vertical bars.
l_chart = vtkChartXY()

plot = l_chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 1)
plot.SetColor(0, 255, 0, 255)

plot = l_chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 2)
plot.SetColor(255, 0, 0, 255)

plot = l_chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 3)
plot.SetColor(0, 0, 255, 255)

# Right chart: horizontal bars.
r_chart = vtkChartXY()

plot = r_chart.AddPlot(vtkChartXY.BAR)
vtkPlotBar.SafeDownCast(plot).SetOrientation(vtkPlotBar.HORIZONTAL)
plot.SetInputData(table, 0, 1)
plot.SetColor(0, 255, 0, 255)

plot = r_chart.AddPlot(vtkChartXY.BAR)
vtkPlotBar.SafeDownCast(plot).SetOrientation(vtkPlotBar.HORIZONTAL)
plot.SetInputData(table, 0, 2)
plot.SetColor(255, 0, 0, 255)

plot = r_chart.AddPlot(vtkChartXY.BAR)
vtkPlotBar.SafeDownCast(plot).SetOrientation(vtkPlotBar.HORIZONTAL)
plot.SetInputData(table, 0, 3)
plot.SetColor(0, 0, 255, 255)

# Left context scene wiring.
l_scene = vtkContextScene()
l_scene.AddItem(l_chart)
l_chart_actor = vtkContextActor()
l_chart_actor.SetScene(l_scene)

# Right context scene wiring.
r_scene = vtkContextScene()
r_scene.AddItem(r_chart)
r_chart_actor = vtkContextActor()
r_chart_actor.SetScene(r_scene)

# Renderer
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.SetBackground(1.0, 1.0, 1.0)
l_scene.SetRenderer(renderer_0)
renderer_0.AddActor(l_chart_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.SetBackground(1.0, 1.0, 1.0)
r_scene.SetRenderer(renderer_1)
renderer_1.AddActor(r_chart_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("bar graph shift scale")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Double render: first pass computes shift/scale, second pass lets
# CalculateBarPlots use the correct shift/scale for bar width.
render_window.Render()
render_window.Render()
interactor.Initialize()
interactor.Start()
