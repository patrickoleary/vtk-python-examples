#!/usr/bin/env python

# Bag plot (statistical contour plot) of 2D data using a chart overlay.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import (
    vtkChart,
    vtkChartXY,
    vtkPlotBag,
)
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

# Data: generate 2D Gaussian samples with correlation
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(99)

num_samples = 200

table = vtkTable()

arr_x = vtkFloatArray()
arr_x.SetName("X")
table.AddColumn(arr_x)

arr_y = vtkFloatArray()
arr_y.SetName("Y")
table.AddColumn(arr_y)

arr_density = vtkFloatArray()
arr_density.SetName("Density")
table.AddColumn(arr_density)

table.SetNumberOfRows(num_samples)
for i in range(num_samples):
    u1 = max(rand_seq.GetValue(), 1e-30)
    rand_seq.Next()
    u2 = rand_seq.GetValue()
    rand_seq.Next()
    # Box-Muller transform
    z0 = math.sqrt(-2.0 * math.log(u1)) * math.cos(2.0 * math.pi * u2)
    z1 = math.sqrt(-2.0 * math.log(u1)) * math.sin(2.0 * math.pi * u2)
    x = z0 * 2.0
    y = 0.5 * z0 + z1 * 1.5
    # Density: distance from center (used for bag depth)
    density = math.exp(-0.5 * (x * x / 4.0 + y * y / 2.25))
    table.SetValue(i, 0, x)
    table.SetValue(i, 1, y)
    table.SetValue(i, 2, density)

# Chart: create a bag plot
chart = vtkChartXY()
chart.SetTitle("Bag Plot (2D Gaussian)")
chart.SetShowLegend(True)

bag = vtkPlotBag()
bag.SetInputData(table, "X", "Y", "Density")
chart.AddPlot(bag)

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
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("BagPlot")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
