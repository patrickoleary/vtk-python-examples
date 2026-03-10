#!/usr/bin/env python

# 3D surface plot of sin(sqrt(x^2 + y^2)) using a chart overlay on the VTK pipeline.

from math import sin, sqrt

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkChartsCore import (
    vtkChartXYZ,
    vtkPlotSurface,
)
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
tomato_rgb = (1.0, 0.388, 0.278)
silver_rgb = (0.753, 0.753, 0.753)

# Data: generate a 2D table of sin(sqrt(x^2 + y^2)) values
table = vtkTable()
num_points = 70
inc = 9.424778 / (num_points - 1)
for i in range(num_points):
    arr = vtkFloatArray()
    table.AddColumn(arr)

table.SetNumberOfRows(num_points)
for i in range(num_points):
    x = i * inc
    for j in range(num_points):
        y = j * inc
        table.SetValue(i, j, sin(sqrt(x * x + y * y)))

# Chart: create a 3D XYZ chart with a surface plot
chart = vtkChartXYZ()
chart.SetGeometry(vtkRectf(10.0, 10.0, 630, 470))

plot = vtkPlotSurface()
plot.SetXRange(0, 10.0)
plot.SetYRange(0, 10.0)
plot.SetInputData(table)
plot.GetPen().SetColorF(tomato_rgb)
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
render_window.SetWindowName("SurfacePlot")

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
