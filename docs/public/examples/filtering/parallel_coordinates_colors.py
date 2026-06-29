#!/usr/bin/env python
# Demonstrate colored parallel coordinates plot with diverging color transfer function.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartParallelCoordinates
from vtkmodules.vtkCommonCore import vtkFloatArray, vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
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

num_points = 200
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

# Create blue to gray to red lookup table using a diverging color transfer function.
lut_num = 256
lut = vtkLookupTable()
lut.SetNumberOfTableValues(lut_num)
lut.Build()

ctf = vtkColorTransferFunction()
ctf.SetColorSpaceToDiverging()
# Variant of Colorbrewer RdBu 5.
colors = [
    [202 / 255.0, 0 / 255.0, 32 / 255.0],
    [244 / 255.0, 165 / 255.0, 130 / 255.0],
    [140 / 255.0, 140 / 255.0, 140 / 255.0],
    [146 / 255.0, 197 / 255.0, 222 / 255.0],
    [5 / 255.0, 113 / 255.0, 176 / 255.0],
]
values = [float(xx) / float(len(colors) - 1) for xx in range(len(colors))]
values.reverse()
for pt, color in zip(values, colors):
    ctf.AddRGBPoint(pt, color[0], color[1], color[2])

for ii in range(lut_num):
    ss = float(ii) / float(lut_num)
    cc = ctf.GetColor(ss)
    lut.SetTableValue(ii, cc[0], cc[1], cc[2], 1.0)

lut.SetAlpha(0.25)
lut.SetRange(-1, 1)

# Set up the chart.
chart = vtkChartParallelCoordinates()

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
render_window.SetSize(600, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("parallel coordinates colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Set the plot data and color mapping.
render_window.Render()
chart.GetPlot(0).SetInputData(table)
chart.GetPlot(0).SetScalarVisibility(1)
chart.GetPlot(0).SetLookupTable(lut)
chart.GetPlot(0).SelectColorArray("Cosine")

render_window.Render()
interactor.Initialize()
interactor.Start()
