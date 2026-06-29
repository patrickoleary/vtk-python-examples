#!/usr/bin/env python

# Test vtkXYPlotActor with multiple function plots, legend, and custom formatting.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkPoints, VTK_ARIAL, VTK_TIMES, VTK_COURIER
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkRenderingAnnotation import vtkXYPlotActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data parameters
n_plots = 4
names = [
    "sqrt(x)",
    "sqrt(x)sin(10ln(sqrt(x)))",
    "sqrt(x)cos(x/10)",
    "-sqrt(x)",
]
n_steps = 10
step_size = 50
n_vals = n_steps * step_size + 1

# Create points and data arrays
points = vtkPoints()
data_0 = vtkDoubleArray()
data_0.SetNumberOfComponents(1)
data_0.SetName(names[0])

data_1 = vtkDoubleArray()
data_1.SetNumberOfComponents(1)
data_1.SetName(names[1])

data_2 = vtkDoubleArray()
data_2.SetNumberOfComponents(1)
data_2.SetName(names[2])

data_3 = vtkDoubleArray()
data_3.SetNumberOfComponents(1)
data_3.SetName(names[3])

data = [data_0, data_1, data_2, data_3]

for i in range(n_vals):
    points.InsertNextPoint(i, 0.0, 0.0)
    val0 = math.sqrt(float(i + 1))
    data[0].InsertNextValue(val0)
    val1 = val0 * math.sin(10 * math.log(val0))
    data[1].InsertNextValue(val1)
    val2 = val0 * math.cos(2.0 * val0)
    data[2].InsertNextValue(val2)
    data[3].InsertNextValue(-val0)

# Determine extrema
range_min = data[0].GetRange()[0]
range_max = data[0].GetRange()[1]
for i in range(1, n_plots):
    r = data[i].GetRange()
    range_min = min(range_min, r[0])
    range_max = max(range_max, r[1])

# Create polydata for each plot
polydata_0 = vtkPolyData()
polydata_0.SetPoints(points)
polydata_0.GetPointData().SetScalars(data[0])

polydata_1 = vtkPolyData()
polydata_1.SetPoints(points)
polydata_1.GetPointData().SetScalars(data[1])

polydata_2 = vtkPolyData()
polydata_2.SetPoints(points)
polydata_2.GetPointData().SetScalars(data[2])

polydata_3 = vtkPolyData()
polydata_3.SetPoints(points)
polydata_3.GetPointData().SetScalars(data[3])

polydata = [polydata_0, polydata_1, polydata_2, polydata_3]

# Plot colors
colors = [
    0.54, 0.21, 0.06,
    1.0, 0.38, 0.01,
    0.24, 0.57, 0.25,
    0.0, 0.0, 0.502,
]

# XY plot actor
xy_plot = vtkXYPlotActor()
for i in range(n_plots):
    xy_plot.AddDataSetInput(polydata[i])
    xy_plot.SetPlotColor(i, colors[3 * i], colors[3 * i + 1], colors[3 * i + 2])

xy_plot.GetPositionCoordinate().SetValue(0.01, 0.01, 0.0)
xy_plot.GetPosition2Coordinate().SetValue(0.99, 0.99, 0.0)
xy_plot.SetLineWidth(2)
xy_plot.SetBorder(10)

# Title
xy_plot.SetTitleItalic(0)
xy_plot.SetTitleBold(1)
xy_plot.SetTitleFontFamily(VTK_ARIAL)
xy_plot.SetTitleColor(0.9, 0.06, 0.02)
xy_plot.SetTitle("XY Plot Actor Test")

# Legend
xy_plot.SetLegend(1)
xy_plot.SetLegendPosition(0.7, 0.6)
xy_plot.SetLegendPosition2(0.25, 0.2)
xy_plot.SetLegendBorder(1)
xy_plot.SetLegendBox(0)
xy_plot.SetLegendUseBackground(1)
xy_plot.SetLegendBackgroundColor(0.86, 0.86, 0.86)
for i in range(n_plots):
    xy_plot.GetLegendActor().SetEntryString(i, names[i])

# Axes
xy_plot.SetAxisTitleFontFamily(VTK_TIMES)
xy_plot.SetAxisTitleColor(0.0, 0.0, 1.0)
xy_plot.SetYTitlePositionToVCenter()
xy_plot.SetXTitle("x")
xy_plot.SetYTitle("f(x)")
xy_plot.SetXValuesToIndex()
xy_plot.SetXRange(0, n_vals - 1)
xy_plot.SetYRange(math.floor(range_min), math.ceil(range_max))
xy_plot.SetXAxisColor(0.0, 0.0, 0.0)
xy_plot.SetYAxisColor(0.0, 0.0, 0.0)

# Labels
xy_plot.SetAxisLabelFontFamily(VTK_COURIER)
xy_plot.SetAxisLabelColor(0.0, 0.0, 0.9)
xy_plot.SetLabelFormat("{:g}")
xy_plot.SetAdjustXLabels(0)
xy_plot.SetNumberOfXLabels(n_steps + 1)
xy_plot.SetAdjustYLabels(0)
xy_plot.SetNumberOfYLabels(3)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.99, 1.0, 0.94)
renderer.AddActor(xy_plot)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("xy plot actor")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
