#!/usr/bin/env python
# Demonstrate bar graph selection highlighting using vtkIdTypeArray.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY
from vtkmodules.vtkCommonCore import vtkIdTypeArray, vtkIntArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
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

arr_month = vtkIntArray()
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

table.SetNumberOfRows(12)
for i in range(12):
    table.SetValue(i, 0, i + 1)
    table.SetValue(i, 1, data_2008[i])
    table.SetValue(i, 2, data_2009[i])
    table.SetValue(i, 3, data_2010[i])

# Build a selection object.
selection = vtkIdTypeArray()
selection.InsertNextValue(1)
selection.InsertNextValue(3)
selection.InsertNextValue(5)

# Set up a chart.
chart = vtkChartXY()

plot = chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 1)
plot.SetColor(0, 255, 0, 255)
plot.SetSelection(selection)

plot = chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 2)
plot.SetColor(255, 0, 0, 255)

plot = chart.AddPlot(vtkChartXY.BAR)
plot.SetInputData(table, 0, 3)
plot.SetColor(0, 0, 255, 255)
plot.SetSelection(selection)

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
render_window.SetWindowName("bar graph selection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
