#!/usr/bin/env python

# NxN scatter plot matrix of correlated random data using a chart overlay.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkScatterPlotMatrix
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMinimalStandardRandomSequence,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: four correlated variables
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(321)

num_samples = 100

table = vtkTable()
var_names = ["Height", "Weight", "Age", "Income"]
for name in var_names:
    arr = vtkFloatArray()
    arr.SetName(name)
    table.AddColumn(arr)

table.SetNumberOfRows(num_samples)
for i in range(num_samples):
    # Generate correlated Gaussian samples via Box-Muller
    u1 = max(rand_seq.GetValue(), 1e-30)
    rand_seq.Next()
    u2 = rand_seq.GetValue()
    rand_seq.Next()
    u3 = max(rand_seq.GetValue(), 1e-30)
    rand_seq.Next()
    u4 = rand_seq.GetValue()
    rand_seq.Next()
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
    z2 = math.sqrt(-2.0 * math.log(u3)) * math.cos(2.0 * math.pi * u4)
    z3 = math.sqrt(-2.0 * math.log(u3)) * math.sin(2.0 * math.pi * u4)
    # Introduce correlations
    height = 170 + 10 * z0
    weight = 70 + 8 * (0.7 * z0 + 0.71 * z1)
    age = 40 + 12 * z2
    income = 50000 + 15000 * (0.3 * z2 + 0.95 * z3)
    table.SetValue(i, 0, height)
    table.SetValue(i, 1, weight)
    table.SetValue(i, 2, age)
    table.SetValue(i, 3, income)

# Chart: create an NxN scatter plot matrix
matrix = vtkScatterPlotMatrix()
matrix.SetInput(table)
matrix.SetTitle("Scatter Plot Matrix")

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(matrix)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(white_smoke_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(800, 800)
render_window.SetMultiSamples(0)
render_window.SetWindowName("ScatterPlotMatrix")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
