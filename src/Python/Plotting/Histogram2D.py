#!/usr/bin/env python

# 2D histogram (heatmap) of correlated random data using a chart overlay.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartHistogram2D, vtkPlotHistogram2D
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Data: build a 2D histogram from correlated random points.
# Accumulate counts in a vtkImageData (2D grid of bins).
num_bins = 60
histogram = vtkImageData()
histogram.SetDimensions(num_bins + 1, num_bins + 1, 1)
histogram.AllocateScalars(10, 1)  # VTK_INT = 10

# Zero the bins
for i in range(histogram.GetNumberOfPoints()):
    histogram.GetPointData().GetScalars().SetTuple1(i, 0)

# Generate correlated random samples and bin them
rand_seq = vtkMinimalStandardRandomSequence()
rand_seq.SetSeed(12345)

num_samples = 50000
for _ in range(num_samples):
    u1 = rand_seq.GetValue()
    rand_seq.Next()
    u2 = rand_seq.GetValue()
    rand_seq.Next()
    # Box-Muller transform for Gaussian samples
    z0 = math.sqrt(-2.0 * math.log(max(u1, 1e-30))) * math.cos(2.0 * math.pi * u2)
    z1 = math.sqrt(-2.0 * math.log(max(u1, 1e-30))) * math.sin(2.0 * math.pi * u2)
    # Introduce correlation
    x = z0
    y = 0.6 * z0 + 0.8 * z1
    # Map to bin indices
    bx = int((x + 4.0) / 8.0 * num_bins)
    by = int((y + 4.0) / 8.0 * num_bins)
    if 0 <= bx < num_bins and 0 <= by < num_bins:
        idx = by * (num_bins + 1) + bx
        old = histogram.GetPointData().GetScalars().GetTuple1(idx)
        histogram.GetPointData().GetScalars().SetTuple1(idx, old + 1)

# ColorFunction: map bin counts to colors (white → blue → red)
ctf = vtkColorTransferFunction()
ctf.AddRGBPoint(0, 1.0, 1.0, 1.0)
ctf.AddRGBPoint(10, 0.2, 0.4, 0.8)
ctf.AddRGBPoint(50, 0.8, 0.2, 0.2)
ctf.AddRGBPoint(200, 0.5, 0.0, 0.0)

# Chart: create a 2D histogram chart
chart = vtkChartHistogram2D()
chart.SetInputData(histogram)
chart.SetTitle("2D Histogram (Correlated Gaussian)")

plot = chart.GetPlot(0)
plot.SetTransferFunction(ctf)

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
render_window.SetWindowName("Histogram2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
