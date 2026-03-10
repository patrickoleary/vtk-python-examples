#!/usr/bin/env python

# Parallel coordinates view of multi-attribute image data using a chart overlay.
# Plots RTData gradient, RTData, elevation, and Brownian vectors from a
# vtkRTAnalyticSource pipeline on parallel axes.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)

# Source: generate an image data set with multiple attribute arrays
rt = vtkRTAnalyticSource()
rt.SetWholeExtent(-3, 3, -3, 3, -3, 3)

grad = vtkImageGradient()
grad.SetDimensionality(3)
grad.SetInputConnection(rt.GetOutputPort())

brown = vtkBrownianPoints()
brown.SetMinimumSpeed(0.5)
brown.SetMaximumSpeed(1.0)
brown.SetInputConnection(grad.GetOutputPort())

elev = vtkElevationFilter()
elev.SetLowPoint(-3, -3, -3)
elev.SetHighPoint(3, 3, 3)
elev.SetInputConnection(brown.GetOutputPort())
elev.Update()

# Data: extract point data arrays into a vtkTable for charting
output = elev.GetOutput()
pd = output.GetPointData()
num_pts = output.GetNumberOfPoints()

table = vtkTable()

# RTData scalar
arr_rt = vtkFloatArray()
arr_rt.SetName("RTData")
arr_rt.SetNumberOfTuples(num_pts)
src_rt = pd.GetArray("RTData")
for i in range(num_pts):
    arr_rt.SetValue(i, src_rt.GetValue(i))
table.AddColumn(arr_rt)

# Elevation scalar
arr_elev = vtkFloatArray()
arr_elev.SetName("Elevation")
arr_elev.SetNumberOfTuples(num_pts)
src_elev = pd.GetArray("Elevation")
for i in range(num_pts):
    arr_elev.SetValue(i, src_elev.GetValue(i))
table.AddColumn(arr_elev)

# RTDataGradient magnitude
arr_grad = vtkFloatArray()
arr_grad.SetName("GradientMag")
arr_grad.SetNumberOfTuples(num_pts)
src_grad = pd.GetArray("RTDataGradient")
for i in range(num_pts):
    gx = src_grad.GetComponent(i, 0)
    gy = src_grad.GetComponent(i, 1)
    gz = src_grad.GetComponent(i, 2)
    arr_grad.SetValue(i, math.sqrt(gx * gx + gy * gy + gz * gz))
table.AddColumn(arr_grad)

# BrownianVectors magnitude
arr_brown = vtkFloatArray()
arr_brown.SetName("BrownianMag")
arr_brown.SetNumberOfTuples(num_pts)
src_brown = pd.GetArray("BrownianVectors")
for i in range(num_pts):
    bx = src_brown.GetComponent(i, 0)
    by = src_brown.GetComponent(i, 1)
    bz = src_brown.GetComponent(i, 2)
    arr_brown.SetValue(i, math.sqrt(bx * bx + by * by + bz * bz))
table.AddColumn(arr_brown)

# Chart: parallel coordinates with all four scalar attributes
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
render_window.SetSize(800, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("ParallelCoordinatesView")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
