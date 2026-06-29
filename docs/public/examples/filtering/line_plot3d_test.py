#!/usr/bin/env python
# Demonstrate a 3D line plot of the Lorenz attractor using vtkChartXYZ.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXYZ, vtkPlotLine3D
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectf, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create the data.
sigma = 10.0
rho = 28.0
beta = 2.66666666666

var_x_solution = vtkTable()
arr_x0 = vtkFloatArray()
arr_x0.SetName("X")
var_x_solution.AddColumn(arr_x0)
arr_x1 = vtkFloatArray()
arr_x1.SetName("Y")
var_x_solution.AddColumn(arr_x1)
arr_x2 = vtkFloatArray()
arr_x2.SetName("Z")
var_x_solution.AddColumn(arr_x2)

num_time_points = 1000
var_x_solution.SetNumberOfRows(num_time_points)
var_x = [0.0, 1.0, 1.05]
delta_t = 0.01

for ii in range(num_time_points):
    var_x_solution.SetValue(ii, 0, var_x[0])
    var_x_solution.SetValue(ii, 1, var_x[1])
    var_x_solution.SetValue(ii, 2, var_x[2])
    dx0 = sigma * (var_x[1] - var_x[0])
    dx1 = var_x[0] * (rho - var_x[2]) - var_x[1]
    dx2 = var_x[0] * var_x[1] - beta * var_x[2]
    var_x[0] += dx0 * delta_t
    var_x[1] += dx1 * delta_t
    var_x[2] += dx2 * delta_t

# Set up the 3D chart.
chart = vtkChartXYZ()
chart.SetGeometry(vtkRectf(75.0, 20.0, 250, 260))

plot = vtkPlotLine3D()
plot.SetInputData(var_x_solution)
plot.GetPen().SetWidth(1)
plot.GetPen().SetColorF(0.1, 0.2, 0.8, 1.0)
chart.AddPlot(plot)

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
render_window.SetWindowName("line plot3d test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
