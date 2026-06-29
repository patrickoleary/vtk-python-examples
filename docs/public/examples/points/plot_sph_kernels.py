#!/usr/bin/env python

# Plot SPH kernel functions and derivatives (Cubic, Quartic, Quintic,
# Wendland) using vtkChartXY.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartXY,
)
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersPoints import (
    vtkSPHCubicKernel,
    vtkSPHQuarticKernel,
    vtkSPHQuinticKernel,
    vtkWendlandQuinticKernel,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextScene
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Resolution and range
width = 3.5
res = 100
inc = width / float(res)

# Table for data
table = vtkTable()

# X axis column (shared by all kernels)
x_array = vtkFloatArray()
x_array.SetName("X Axis")
x_array.SetNumberOfValues(res)
for i in range(res):
    x_array.SetValue(i, float(i) * inc)
table.AddColumn(x_array)
table.SetNumberOfRows(res)

# Cubic SPH Kernel
cubic = vtkSPHCubicKernel()
cubic.SetDimension(2)
cubic.SetSpatialStep(1.0)
cubic.Initialize(None, None, None)

cubic_function_array = vtkFloatArray()
cubic_function_array.SetName("Cubic")
cubic_function_array.SetNumberOfValues(res)
table.AddColumn(cubic_function_array)
cubic_function_col = table.GetNumberOfColumns() - 1

cubic_derivative_array = vtkFloatArray()
cubic_derivative_array.SetName("Cubic deriv")
cubic_derivative_array.SetNumberOfValues(res)
table.AddColumn(cubic_derivative_array)
cubic_derivative_col = table.GetNumberOfColumns() - 1

for i in range(res):
    r = float(i) * inc
    table.SetValue(i, cubic_function_col, cubic.ComputeFunctionWeight(r))
    table.SetValue(i, cubic_derivative_col, cubic.ComputeDerivWeight(r))

# Quartic SPH Kernel
quartic = vtkSPHQuarticKernel()
quartic.SetDimension(2)
quartic.SetSpatialStep(1.0)
quartic.Initialize(None, None, None)

quartic_function_array = vtkFloatArray()
quartic_function_array.SetName("Quartic")
quartic_function_array.SetNumberOfValues(res)
table.AddColumn(quartic_function_array)
quartic_function_col = table.GetNumberOfColumns() - 1

quartic_derivative_array = vtkFloatArray()
quartic_derivative_array.SetName("Quartic deriv")
quartic_derivative_array.SetNumberOfValues(res)
table.AddColumn(quartic_derivative_array)
quartic_derivative_col = table.GetNumberOfColumns() - 1

for i in range(res):
    r = float(i) * inc
    table.SetValue(i, quartic_function_col, quartic.ComputeFunctionWeight(r))
    table.SetValue(i, quartic_derivative_col, quartic.ComputeDerivWeight(r))

# Quintic SPH Kernel
quintic = vtkSPHQuinticKernel()
quintic.SetDimension(2)
quintic.SetSpatialStep(1.0)
quintic.Initialize(None, None, None)

quintic_function_array = vtkFloatArray()
quintic_function_array.SetName("Quintic")
quintic_function_array.SetNumberOfValues(res)
table.AddColumn(quintic_function_array)
quintic_function_col = table.GetNumberOfColumns() - 1

quintic_derivative_array = vtkFloatArray()
quintic_derivative_array.SetName("Quintic deriv")
quintic_derivative_array.SetNumberOfValues(res)
table.AddColumn(quintic_derivative_array)
quintic_derivative_col = table.GetNumberOfColumns() - 1

for i in range(res):
    r = float(i) * inc
    table.SetValue(i, quintic_function_col, quintic.ComputeFunctionWeight(r))
    table.SetValue(i, quintic_derivative_col, quintic.ComputeDerivWeight(r))

# Wendland C2 (quintic) Kernel
wendland = vtkWendlandQuinticKernel()
wendland.SetDimension(2)
wendland.SetSpatialStep(1.0)
wendland.Initialize(None, None, None)

wendland_function_array = vtkFloatArray()
wendland_function_array.SetName("Wendland")
wendland_function_array.SetNumberOfValues(res)
table.AddColumn(wendland_function_array)
wendland_function_col = table.GetNumberOfColumns() - 1

wendland_derivative_array = vtkFloatArray()
wendland_derivative_array.SetName("Wendland deriv")
wendland_derivative_array.SetNumberOfValues(res)
table.AddColumn(wendland_derivative_array)
wendland_derivative_col = table.GetNumberOfColumns() - 1

for i in range(res):
    r = float(i) * inc
    table.SetValue(i, wendland_function_col, wendland.ComputeFunctionWeight(r))
    table.SetValue(i, wendland_derivative_col, wendland.ComputeDerivWeight(r))

# Chart
chart = vtkChartXY()
chart.SetTitle("SPH Kernels")
chart.SetShowLegend(True)

cubic_line = chart.AddPlot(vtkChart.LINE)
cubic_line.SetInputData(table, 0, cubic_function_col)
cubic_line.SetColor(255, 0, 0, 255)
cubic_line.SetWidth(2.0)

cubic_derivative_line = chart.AddPlot(vtkChart.LINE)
cubic_derivative_line.SetInputData(table, 0, cubic_derivative_col)
cubic_derivative_line.SetColor(255, 0, 0, 128)
cubic_derivative_line.SetWidth(1.0)

quartic_line = chart.AddPlot(vtkChart.LINE)
quartic_line.SetInputData(table, 0, quartic_function_col)
quartic_line.SetColor(0, 255, 0, 255)
quartic_line.SetWidth(2.0)

quartic_derivative_line = chart.AddPlot(vtkChart.LINE)
quartic_derivative_line.SetInputData(table, 0, quartic_derivative_col)
quartic_derivative_line.SetColor(0, 255, 0, 128)
quartic_derivative_line.SetWidth(1.0)

quintic_line = chart.AddPlot(vtkChart.LINE)
quintic_line.SetInputData(table, 0, quintic_function_col)
quintic_line.SetColor(0, 0, 255, 255)
quintic_line.SetWidth(2.0)

quintic_derivative_line = chart.AddPlot(vtkChart.LINE)
quintic_derivative_line.SetInputData(table, 0, quintic_derivative_col)
quintic_derivative_line.SetColor(0, 0, 255, 128)
quintic_derivative_line.SetWidth(1.0)

wendland_line = chart.AddPlot(vtkChart.LINE)
wendland_line.SetInputData(table, 0, wendland_function_col)
wendland_line.SetColor(255, 0, 255, 255)
wendland_line.SetWidth(2.0)

wendland_derivative_line = chart.AddPlot(vtkChart.LINE)
wendland_derivative_line.SetInputData(table, 0, wendland_derivative_col)
wendland_derivative_line.SetColor(255, 0, 255, 128)
wendland_derivative_line.SetWidth(1.0)

left = chart.GetAxis(1)  # LEFT
bottom = chart.GetAxis(0)  # BOTTOM
left.SetTitle("Kernel Value")
bottom.SetTitle("r/h")

# Context actor + scene for 2D chart
context_actor = vtkContextActor()
scene = context_actor.GetScene()
scene.AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 300)
render_window.SetWindowName("plot sph kernels")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
