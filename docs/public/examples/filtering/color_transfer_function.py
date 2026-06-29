#!/usr/bin/env python
# Demonstrate color transfer function visualization with control points and range handles.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChartXY,
    vtkColorTransferControlPointsItem,
    vtkColorTransferFunctionItem,
    vtkRangeHandlesItem,
)
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a color transfer function.
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddHSVSegment(50.0, 0.0, 1.0, 1.0, 85.0, 0.3333, 1.0, 1.0)
color_transfer_function.AddHSVSegment(85.0, 0.3333, 1.0, 1.0, 170.0, 0.6666, 1.0, 1.0)
color_transfer_function.AddHSVSegment(170.0, 0.6666, 1.0, 1.0, 200.0, 0.0, 1.0, 1.0)
color_transfer_function.Build()

# Set up a chart.
chart = vtkChartXY()
chart.SetTitle("Chart")

color_transfer_item = vtkColorTransferFunctionItem()
color_transfer_item.SetColorTransferFunction(color_transfer_function)
chart.AddPlot(color_transfer_item)

control_points_item = vtkColorTransferControlPointsItem()
control_points_item.SetColorTransferFunction(color_transfer_function)
control_points_item.SetUserBounds(0.0, 255.0, 0.0, 1.0)
chart.AddPlot(control_points_item)

range_handles_item = vtkRangeHandlesItem()
range_handles_item.SetColorTransferFunction(color_transfer_function)
range_handles_item.SetHandleWidth(40.0)
chart.AddPlot(range_handles_item)

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
render_window.SetMultiSamples(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("color transfer function")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
