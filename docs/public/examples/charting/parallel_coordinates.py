#!/usr/bin/env python

# Parallel coordinates plot of multi-dimensional data using a chart overlay.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
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

# Data: five car attributes for 30 samples
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(77)

attributes = [
    ("Horsepower", 80, 400),
    ("Weight (kg)", 900, 2500),
    ("MPG", 10, 50),
    ("Cylinders", 3, 12),
    ("Displacement", 1.0, 7.0),
]

table = vtkTable()
arr_horsepower = vtkFloatArray()
arr_horsepower.SetName("Horsepower")
table.AddColumn(arr_horsepower)
arr_weight = vtkFloatArray()
arr_weight.SetName("Weight (kg)")
table.AddColumn(arr_weight)
arr_mpg = vtkFloatArray()
arr_mpg.SetName("MPG")
table.AddColumn(arr_mpg)
arr_cylinders = vtkFloatArray()
arr_cylinders.SetName("Cylinders")
table.AddColumn(arr_cylinders)
arr_displacement = vtkFloatArray()
arr_displacement.SetName("Displacement")
table.AddColumn(arr_displacement)

num_samples = 30
table.SetNumberOfRows(num_samples)
for i in range(num_samples):
    for c, (_, lo, hi) in enumerate(attributes):
        val = rand_seq.GetRangeValue(lo, hi)
        rand_seq.Next()
        table.SetValue(i, c, val)

# Chart: create a parallel coordinates chart
chart = vtkChartParallelCoordinates()
chart.GetPlot(0).SetInputData(table)

# ContextActor: overlay the chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(white_smoke_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("parallel coordinates")
render_window.SetMultiSamples(0)
render_window.SetSize(800, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
