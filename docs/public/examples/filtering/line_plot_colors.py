#!/usr/bin/env python
# Demonstrate colored line plots with lookup tables and scalar visibility.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkPlotPoints
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkPen
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
arr_s2.SetName("Sine2")

num_points = 69
inc = 7.5 / (num_points - 1)
for i in range(num_points):
    arr_x.InsertNextValue(i * inc)
    arr_c.InsertNextValue(math.cos(i * inc))
    arr_s.InsertNextValue(math.sin(i * inc))
    arr_s2.InsertNextValue(math.sin(i * inc) + 0.5)

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
lut2.SetAlphaRange(0.2, 0.8)
lut2.SetRampToLinear()
lut2.SetRange(-1, 1)
lut2.Build()

# Set up chart.
chart = vtkChartXY()
chart.SetShowLegend(True)

# Line 0: solid line with circle markers, colored by cosine via lut.
line0 = chart.AddPlot(vtkChartXY.LINE)
line0.SetInputData(table, 0, 1)
line0.SetColor(50, 50, 50, 255)
line0.SetWidth(3.0)
line0.GetPen().SetLineType(vtkPen.SOLID_LINE)
line0.SetMarkerStyle(vtkPlotPoints.CIRCLE)
line0.SetScalarVisibility(1)
line0.SetLookupTable(lut)
line0.SelectColorArray(1)

# Line 1: no pen, plus markers.
line1 = chart.AddPlot(vtkChartXY.LINE)
line1.SetInputData(table, 0, 2)
line1.GetPen().SetLineType(vtkPen.NO_PEN)
line1.SetMarkerStyle(vtkPlotPoints.PLUS)
line1.SetColor(150, 100, 0, 255)

# Line 2: dash line with square markers, colored by sine via lut2.
line2 = chart.AddPlot(vtkChartXY.LINE)
line2.SetInputData(table, 0, 3)
line2.SetColor(100, 100, 100, 255)
line2.SetWidth(3.0)
line2.GetPen().SetLineType(vtkPen.DASH_LINE)
line2.SetMarkerStyle(vtkPlotPoints.SQUARE)
line2.ScalarVisibilityOn()
line2.SetLookupTable(lut2)
line2.SelectColorArray("Sine")

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
render_window.SetWindowName("line plot colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
