#!/usr/bin/env python
# Demonstrate plot range handles with vertical and horizontal orientation and synchronization.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis, vtkChartXY, vtkPlotRangeHandlesItem
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Set up chart.
chart = vtkChartXY()
chart.GetAxis(vtkAxis.BOTTOM).SetRange(0, 50)
chart.GetAxis(vtkAxis.LEFT).SetRange(0, 50)

# Vertical handles.
v_range_item = vtkPlotRangeHandlesItem()
v_range_item.SetExtent(0, 10, 0, 30)
v_range_item.SynchronizeRangeHandlesOn()
chart.AddPlot(v_range_item)
v_range_item.ComputeHandlesDrawRange()

# Horizontal handles.
h_range_item = vtkPlotRangeHandlesItem()
h_range_item.SetHandleOrientationToHorizontal()
h_range_item.SynchronizeRangeHandlesOn()
h_range_item.SetExtent(0, 20, 0, 10)
chart.AddPlot(h_range_item)
h_range_item.ComputeHandlesDrawRange()

# Context actor and scene wiring.
context_actor = vtkContextActor()
scene = context_actor.GetScene()
scene.AddItem(chart)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
scene.SetRenderer(renderer)
renderer.AddActor(context_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 350)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("plot range handles item")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
