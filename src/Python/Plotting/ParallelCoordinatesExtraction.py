#!/usr/bin/env python

# Parallel coordinates chart linked to a 3D view via annotation-based selection.
# The left viewport shows a parallel coordinates chart of RTAnalytic data attributes.
# The right viewport shows a 3D outline of the data with selected points rendered
# inside. Select data on the chart axes to see corresponding 3D points appear.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
)
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkBrownianPoints
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
white_smoke_rgb = (0.961, 0.961, 0.961)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

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

arr_rt = vtkFloatArray()
arr_rt.SetName("RTData")
arr_rt.SetNumberOfTuples(num_pts)
src_rt = pd.GetArray("RTData")
for i in range(num_pts):
    arr_rt.SetValue(i, src_rt.GetValue(i))
table.AddColumn(arr_rt)

arr_elev = vtkFloatArray()
arr_elev.SetName("Elevation")
arr_elev.SetNumberOfTuples(num_pts)
src_elev = pd.GetArray("Elevation")
for i in range(num_pts):
    arr_elev.SetValue(i, src_elev.GetValue(i))
table.AddColumn(arr_elev)

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

# ---- Left viewport: parallel coordinates chart ----
chart = vtkChartParallelCoordinates()
chart.GetPlot(0).SetInputData(table)

left_context = vtkContextActor()
left_context.GetScene().AddItem(chart)

left_renderer = vtkRenderer()
left_renderer.SetBackground(white_smoke_rgb)
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(left_context)
left_context.GetScene().SetRenderer(left_renderer)

# ---- Right viewport: 3D outline with elevation-colored points ----

# Outline of the image data bounds
outline = vtkOutlineFilter()
outline.SetInputConnection(elev.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Lookup table: brown to white for elevation coloring
lut = vtkLookupTable()
lut.SetTableRange(0, 1)
lut.SetHueRange(0.1, 0.1)
lut.SetSaturationRange(1.0, 0.1)
lut.SetValueRange(0.4, 1.0)
lut.Build()

# Data points: show all points colored by elevation
data_mapper = vtkDataSetMapper()
data_mapper.SetInputConnection(elev.GetOutputPort())
data_mapper.SetScalarModeToUsePointFieldData()
data_mapper.SetColorModeToMapScalars()
data_mapper.ScalarVisibilityOn()
elev_range = pd.GetArray("Elevation").GetRange()
data_mapper.SetScalarRange(elev_range)
data_mapper.SetLookupTable(lut)
data_mapper.SelectColorArray("Elevation")

data_actor = vtkActor()
data_actor.SetMapper(data_mapper)
data_actor.GetProperty().SetRepresentationToPoints()
data_actor.GetProperty().SetPointSize(6)

right_renderer = vtkRenderer()
right_renderer.SetBackground(dark_slate_gray_rgb)
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(outline_actor)
right_renderer.AddActor(data_actor)
right_renderer.ResetCamera()

# Window: display both viewports
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(1200, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("ParallelCoordinatesExtraction")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
