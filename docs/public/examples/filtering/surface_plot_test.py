#!/usr/bin/env python
# Demonstrate a 3D surface plot of sin(sqrt(x^2 + y^2)) with rotation via mouse event.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXYZ, vtkPlotSurface
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectf, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create the 3D chart.
chart = vtkChartXYZ()
chart.SetGeometry(vtkRectf(75.0, 20.0, 250, 260))

# Create a surface.
table = vtkTable()
num_points = 70
inc = 9.424778 / (num_points - 1)
for i in range(num_points):
    arr = vtkFloatArray()
    table.AddColumn(arr)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc
    for j in range(num_points):
        y = j * inc
        table.SetValue(i, j, math.sin(math.sqrt(x * x + y * y)))

# Set up the surface plot.
plot = vtkPlotSurface()
plot.SetXRange(0, 9.424778)
plot.SetYRange(0, 9.424778)
plot.SetInputData(table)
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
render_window.SetWindowName("surface plot test")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
