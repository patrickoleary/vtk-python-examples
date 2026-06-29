#!/usr/bin/env python
# Demonstrate clearing all axis selections in a parallel coordinates chart.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
from vtkmodules.vtkCommonCore import vtkDoubleArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create dummy data.
table = vtkTable()
arr_x = vtkDoubleArray()
arr_x.SetName("x")
table.AddColumn(arr_x)
arr_c = vtkDoubleArray()
arr_c.SetName("cosine")
table.AddColumn(arr_c)
arr_s = vtkDoubleArray()
arr_s.SetName("sine")
table.AddColumn(arr_s)
arr_s2 = vtkDoubleArray()
arr_s2.SetName("tangent")
table.AddColumn(arr_s2)

num_points = 200
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))
    table.SetValue(i, 3, math.tan(i * inc) + 0.5)

# Set up a parallel coordinates chart.
chart = vtkChartParallelCoordinates()
chart.GetPlot(0).SetInputData(table)

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
render_window.SetSize(600, 400)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("parallel coordinates clear all axes selections")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
