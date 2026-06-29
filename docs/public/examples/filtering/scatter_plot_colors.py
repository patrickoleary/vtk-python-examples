#!/usr/bin/env python
# Demonstrate colored scatter plots with lookup tables and scalar visibility.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
arr_x = vtkFloatArray()
arr_x.SetName("XAxis")
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
arr_s2 = vtkFloatArray()
arr_s2.SetName("Tan")

num_points = 40
inc = 7.5 / (num_points - 1)
for i in range(num_points):
    arr_x.InsertNextValue(i * inc)
    arr_c.InsertNextValue(math.cos(i * inc))
    arr_s.InsertNextValue(math.sin(i * inc))
    arr_s2.InsertNextValue(math.tan(i * inc) + 0.5)

table = vtkTable()
table.AddColumn(arr_x)
table.AddColumn(arr_c)
table.AddColumn(arr_s)
table.AddColumn(arr_s2)

# Generate a black-to-red lookup table with fixed alpha.
lut = vtkLookupTable()
lut.SetValueRange(0.2, 1.0)
lut.SetSaturationRange(1, 1)
lut.SetHueRange(0, 0)
lut.SetRampToLinear()
lut.SetRange(-1, 1)
lut.SetAlpha(0.75)
lut.Build()

# Generate a black-to-blue lookup table with alpha range.
lut2 = vtkLookupTable()
lut2.SetValueRange(0.2, 1.0)
lut2.SetSaturationRange(1, 1)
lut2.SetHueRange(0.6667, 0.6667)
lut2.SetAlphaRange(0.4, 0.8)
lut2.SetRampToLinear()
lut2.SetRange(-1, 1)
lut2.Build()

# Set up chart.
chart = vtkChartXY()
chart.SetShowLegend(True)

# Points 0: cross markers, no coloring.
points0 = chart.AddPlot(vtkChartXY.POINTS)
points0.SetInputData(table, 0, 1)
points0.SetColor(0, 0, 0, 255)
points0.SetWidth(1.0)
points0.SetMarkerStyle(vtkPlotPoints.CROSS)

# Points 1: diamond markers, colored by cosine via lut.
points1 = chart.AddPlot(vtkChartXY.POINTS)
points1.SetInputData(table, 0, 2)
points1.SetColor(0, 0, 0, 255)
points1.SetMarkerStyle(vtkPlotPoints.DIAMOND)
points1.SetScalarVisibility(1)
points1.SetLookupTable(lut)
points1.SelectColorArray(1)

# Points 2: default markers, colored by cosine via lut2.
points2 = chart.AddPlot(vtkChartXY.POINTS)
points2.SetInputData(table, 0, 3)
points2.SetColor(0, 0, 0, 255)
points2.ScalarVisibilityOn()
points2.SetLookupTable(lut2)
points2.SelectColorArray("Cosine")
points2.SetWidth(4.0)

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
render_window.SetWindowName("scatter plot colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
