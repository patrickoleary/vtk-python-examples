#!/usr/bin/env python
# Demonstrate a scatter plot matrix with selective column visibility.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkScatterPlotMatrix
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("x")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("cos(x)")
table.AddColumn(arr_c)
arr_s = vtkFloatArray()
arr_s.SetName("sin(x)")
table.AddColumn(arr_s)
arr_s2 = vtkFloatArray()
arr_s2.SetName("sin(x + 0.5)")
table.AddColumn(arr_s2)
tangent = vtkFloatArray()
tangent.SetName("tan(x)")
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

# Set up the scatter plot matrix with selective column visibility.
matrix = vtkScatterPlotMatrix()
matrix.SetInput(table)
matrix.SetColumnVisibilityAll(False)
matrix.SetColumnVisibility("x", True)
matrix.SetColumnVisibility("sin(x)", True)
matrix.SetColumnVisibility("cos(x)", True)
matrix.SetColumnVisibility("tan(x)", True)

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(800, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("scatter plot matrix visible")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
