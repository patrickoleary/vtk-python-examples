#!/usr/bin/env python
# Demonstrate a 3D scatter chart with auto-rotation using vtkChartXYZ.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXYZ, vtkPlotPoints3D
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkColor4ub, vtkRectf, vtkTable
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a table with some points in it.
table = vtkTable()
arr_x = vtkFloatArray()
arr_x.SetName("X Axis")
table.AddColumn(arr_x)
arr_c = vtkFloatArray()
arr_c.SetName("Cosine")
table.AddColumn(arr_c)
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)

num_points = 69
inc = 7.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.cos(i * inc))
    table.SetValue(i, 2, math.sin(i * inc))

# Set up the first chart with auto-rotation.
chart = vtkChartXYZ()
chart.SetAutoRotate(True)
chart.SetFitToScene(False)
chart.SetDecorateAxes(False)
chart.SetGeometry(vtkRectf(75.0, 20.0, 250, 260))

plot = vtkPlotPoints3D()
plot.SetInputData(table, "X Axis", "Sine", "Cosine")
chart.AddPlot(plot)
chart.SetAxisColor(vtkColor4ub(20, 200, 30, 255))
chart.GetAxis(0).SetUnscaledRange(-0.1, 7.6)
chart.GetAxis(1).SetUnscaledRange(-1.1, 1.1)
chart.GetAxis(2).SetUnscaledRange(-1.1, 1.1)
chart.RecalculateTransform()

# Set up the second chart (stationary duplicate).
chart2 = vtkChartXYZ()
chart2.SetAutoRotate(True)
chart2.SetFitToScene(False)
chart2.SetDecorateAxes(False)
chart2.SetGeometry(vtkRectf(75.0, 20.0, 250, 260))

plot2 = vtkPlotPoints3D()
plot2.SetInputData(table, "X Axis", "Sine", "Cosine")
chart2.AddPlot(plot2)
chart2.GetAxis(0).SetUnscaledRange(-0.1, 7.6)
chart2.GetAxis(1).SetUnscaledRange(-1.1, 1.1)
chart2.GetAxis(2).SetUnscaledRange(-1.1, 1.1)
chart2.RecalculateTransform()

# Context actor and scene wiring.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)
context_actor.GetScene().AddItem(chart2)

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
render_window.SetWindowName("chart xyz")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Timer-based animation callback.
angle = [0.0]

def process_events(caller, event):
    angle[0] += 2
    chart.SetAngle(angle[0])
    caller.Render()
    if angle[0] >= 90:
        caller.DestroyTimer()

interactor.AddObserver("TimerEvent", process_events)

interactor.Initialize()
interactor.CreateRepeatingTimer(1000 // 25)
interactor.Start()
