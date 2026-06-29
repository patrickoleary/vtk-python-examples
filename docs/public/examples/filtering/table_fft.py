#!/usr/bin/env python

# Demonstrate vtkTableFFT by creating a table with known input signals,
# computing the FFT with a rectangular window, and rendering the
# frequency-domain magnitude as a bar chart.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartXY,
)
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersGeneral import vtkTableFFT
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Input signal: impulse in column 1, constant in column 2
length = 8
col1_vals = [float(length), 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
col2_vals = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
time_vals = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]

column_1 = vtkDoubleArray()
column_1.SetNumberOfTuples(length)
column_1.SetNumberOfComponents(1)
column_1.SetName("Data1")
for i in range(length):
    column_1.SetValue(i, col1_vals[i])

column_2 = vtkDoubleArray()
column_2.SetNumberOfTuples(length)
column_2.SetNumberOfComponents(1)
column_2.SetName("Data2")
for i in range(length):
    column_2.SetValue(i, col2_vals[i])

column_time = vtkDoubleArray()
column_time.SetNumberOfTuples(length)
column_time.SetNumberOfComponents(1)
column_time.SetName("Time")
for i in range(length):
    column_time.SetValue(i, time_vals[i])

# Build input table
input_table = vtkTable()
input_table.AddColumn(column_1)
input_table.AddColumn(column_2)
input_table.AddColumn(column_time)

# Compute FFT
fft_filter = vtkTableFFT()
fft_filter.SetInputData(input_table)
fft_filter.CreateFrequencyColumnOn()
fft_filter.SetWindowingFunction(0)  # RECTANGULAR
fft_filter.Update()

# Display FFT result in a chart
fft_output = fft_filter.GetOutput()

chart = vtkChartXY()
chart.SetTitle("TableFFT")

line = chart.AddPlot(vtkChart.LINE)
line.SetInputData(fft_output, "Frequency", "Data1")
line.SetColor(0, 0, 255, 255)
line.SetWidth(2.0)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(600, 400)
render_window.SetMultiSamples(0)
render_window.SetWindowName("table fft")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
