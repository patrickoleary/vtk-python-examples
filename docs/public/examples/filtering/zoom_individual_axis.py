#!/usr/bin/env python
# Demonstrate zooming on individual axes with mouse wheel while disabling x-axis zoom.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkTable
from vtkmodules.vtkFiltersGeneral import vtkAnnotationLink
from vtkmodules.vtkRenderingContext2D import vtkContextActor, vtkContextMouseEvent
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
arr_s = vtkFloatArray()
arr_s.SetName("Sine")
table.AddColumn(arr_s)

num_points = 100
inc = 9.5 / (num_points - 1)
table.SetNumberOfRows(num_points)
for i in range(num_points):
    table.SetValue(i, 0, i * inc)
    table.SetValue(i, 1, math.sin(i * inc))

# Set up a chart with zoom-axis action.
chart = vtkChartXY()
link = vtkAnnotationLink()
chart.SetAnnotationLink(link)
chart.SetActionToButton(vtkChartXY.ZOOM_AXIS, vtkContextMouseEvent.LEFT_BUTTON)
chart.SetSelectionMethod(vtkChartXY.SELECTION_PLOTS)

plot = chart.AddPlot(vtkChartXY.POINTS)
plot.SetInputData(table, 0, 1)
plot.SetColor(0, 255, 0, 255)
plot.SetWidth(1.0)

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
render_window.SetWindowName("zoom individual axis")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Enable mouse wheel zooming but disable x-axis zoom.
chart.SetZoomWithMouseWheel(True)
chart.SetAxisZoom(vtkAxis.BOTTOM, False)

interactor.Initialize()
interactor.Start()
