#!/usr/bin/env python
# Demonstrate a 2D histogram chart with color transfer function using vtkChartHistogram2D.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartHistogram2D, vtkChartXY, vtkPlotLine
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkImageData, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

size = 400

# Define a chart.
chart = vtkChartHistogram2D()

# Add only a plot without image data first.
table = vtkTable()
x_arr = vtkDoubleArray()
x_arr.SetName("X")
x_arr.SetNumberOfComponents(1)
x_arr.SetNumberOfTuples(size)
y_arr = vtkDoubleArray()
y_arr.SetName("Y")
y_arr.SetNumberOfComponents(1)
y_arr.SetNumberOfTuples(size)

for i in range(size):
    x_arr.SetTuple1(i, i)
    y_arr.SetTuple1(i, i)
table.AddColumn(x_arr)
table.AddColumn(y_arr)

plot = vtkPlotLine.SafeDownCast(chart.AddPlot(vtkChartXY.LINE))
plot.SetInputData(table, 0, 1)
plot.SetColorF(1.0, 0.0, 0.0)
plot.SetWidth(5)

# Remove the plot and add image data.
plot_id = chart.GetPlotIndex(plot)
chart.RemovePlot(plot_id)

data = vtkImageData()
data.SetExtent(0, size - 1, 0, size - 1, 0, 0)
data.AllocateScalars(11, 1)  # VTK_DOUBLE = 11

data.SetOrigin(100.0, 0.0, 0.0)
data.SetSpacing(2.0, 1.0, 1.0)

for i in range(size):
    for j in range(size):
        val = math.sin(math.radians(2 * i)) * math.cos(math.radians(j))
        data.SetScalarComponentFromDouble(j, i, 0, 0, val)
chart.SetInputData(data)

transfer_function = vtkColorTransferFunction()
transfer_function.AddHSVSegment(0.0, 0.0, 1.0, 1.0, 0.3333, 0.3333, 1.0, 1.0)
transfer_function.AddHSVSegment(0.3333, 0.3333, 1.0, 1.0, 0.6666, 0.6666, 1.0, 1.0)
transfer_function.AddHSVSegment(0.6666, 0.6666, 1.0, 1.0, 1.0, 0.2, 1.0, 0.3)
transfer_function.Build()
chart.SetTransferFunction(transfer_function)

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
render_window.SetSize(size, size)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("histogram2d test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
