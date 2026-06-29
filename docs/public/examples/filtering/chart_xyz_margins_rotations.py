#!/usr/bin/env python
# Demonstrate a 3D chart with margins, rotation, spin, zoom, and pan via mouse events.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXYZ, vtkPlotLine3D, vtkPlotPoints3D
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkRectf, vtkTable, vtkVector4i
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create point data table (corners of a unit cube offset from origin).
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X")
table.AddColumn(arr_x)
arr_y = vtkFloatArray()
arr_y.SetName("Y")
table.AddColumn(arr_y)
arr_z = vtkFloatArray()
arr_z.SetName("Z")
table.AddColumn(arr_z)

table.SetNumberOfRows(8)
idx = 0
for x in range(2):
    for y in range(2):
        for z in range(2):
            table.SetValue(idx, 0, x + 100)
            table.SetValue(idx, 1, y - 75)
            table.SetValue(idx, 2, z + 50)
            idx += 1

# Create wireframe cube table.
table2 = vtkTable()
arr2_x = vtkFloatArray()
arr2_x.SetName("X")
table2.AddColumn(arr2_x)
arr2_y = vtkFloatArray()
arr2_y.SetName("Y")
table2.AddColumn(arr2_y)
arr2_z = vtkFloatArray()
arr2_z.SetName("Z")
table2.AddColumn(arr2_z)

wireframe_pts = [
    (0, 0, 0), (1, 0, 0), (1, 1, 0), (0, 1, 0), (0, 0, 0),
    (0, 0, 1), (1, 0, 1), (1, 0, 0), (1, 0, 1),
    (1, 1, 1), (1, 1, 0), (1, 1, 1),
    (0, 1, 1), (0, 1, 0), (0, 1, 1), (0, 0, 1),
]
table2.SetNumberOfRows(len(wireframe_pts))
for i, (px, py, pz) in enumerate(wireframe_pts):
    table2.SetValue(i, 0, px * 0.8 + 100.1)
    table2.SetValue(i, 1, py * 0.8 - 74.9)
    table2.SetValue(i, 2, pz * 0.8 + 50.1)

# Set up the chart.
chart = vtkChartXYZ()
chart.SetMargins(vtkVector4i(40, 40, 40, 40))
chart.SetFitToScene(True)

plot = vtkPlotPoints3D()
plot.SetInputData(table)
chart.AddPlot(plot)

plot2 = vtkPlotLine3D()
plot2.SetInputData(table2)
chart.AddPlot(plot2)

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
render_window.SetSize(600, 500)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("chart xyz margins rotations")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
