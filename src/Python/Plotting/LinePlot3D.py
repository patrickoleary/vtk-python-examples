#!/usr/bin/env python

# 3D line plot of a helix using a chart overlay on the VTK pipeline.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import vtkChartXYZ, vtkPlotLine3D
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import (
    vtkRectf,
    vtkTable,
    vtkVector2i,
)
from vtkmodules.vtkRenderingContext2D import (
    vtkContextActor,
    vtkContextMouseEvent,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
silver_rgb = (0.753, 0.753, 0.753)

# Data: parametric helix x=cos(t), y=sin(t), z=t/(2*pi)
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

num_points = 200
table.SetNumberOfRows(num_points)
for i in range(num_points):
    t = i * 4.0 * math.pi / (num_points - 1)
    table.SetValue(i, 0, math.cos(t))
    table.SetValue(i, 1, math.sin(t))
    table.SetValue(i, 2, t / (2.0 * math.pi))

# Chart: create a 3D XYZ chart with a line plot
chart = vtkChartXYZ()
chart.SetGeometry(vtkRectf(10.0, 10.0, 630, 470))

plot = vtkPlotLine3D()
plot.SetInputData(table)
plot.GetPen().SetColorF(0.2, 0.5, 0.9)
plot.GetPen().SetWidth(3.0)
chart.AddPlot(plot)

# ContextActor: overlay the 3D chart on the normal VTK rendering pipeline
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(chart)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(silver_rgb)
renderer.AddActor(context_actor)
context_actor.GetScene().SetRenderer(renderer)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("LinePlot3D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Rotate the chart to an initial oblique view using a synthetic mouse event
render_window.Render()
mouse_event = vtkContextMouseEvent()
mouse_event.SetInteractor(render_window_interactor)
mouse_event.SetButton(vtkContextMouseEvent.LEFT_BUTTON)
last_pos = vtkVector2i()
last_pos.Set(100, 50)
mouse_event.SetLastScreenPos(last_pos)
pos = vtkVector2i()
pos.Set(150, 100)
mouse_event.SetScreenPos(pos)
chart.MouseMoveEvent(mouse_event)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
