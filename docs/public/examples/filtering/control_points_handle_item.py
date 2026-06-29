#!/usr/bin/env python
# Demonstrate composite control points with opacity handles and event replay.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChartXY,
    vtkCompositeControlPointsItem,
    vtkCompositeTransferFunctionItem,
)
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create transfer mapping scalar value to opacity.
opacity_function = vtkPiecewiseFunction()
opacity_function.AddPoint(0.0, 0.1)
opacity_function.AddPoint(0.5, 0.5)
opacity_function.AddPoint(1.0, 1.0)

# Create transfer mapping scalar value to color.
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.SetColorSpaceToHSV()
color_transfer_function.HSVWrapOn()
color_transfer_function.AddHSVSegment(0.0, 0.0, 1.0, 1.0, 0.3333, 0.3333, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.3333, 0.3333, 1.0, 1.0, 0.6666, 0.6666, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.6666, 0.6666, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0)
color_transfer_function.Build()

# Set up the chart.
chart = vtkChartXY()
chart.ForceAxesToBoundsOn()
chart.SetAutoSize(True)
chart.SetAutoAxes(False)
chart.SetHiddenAxisBorder(0)
for i in range(4):
    chart.GetAxis(i).SetVisible(True)
    chart.GetAxis(i).SetNumberOfTicks(0)
    chart.GetAxis(i).SetBehavior(2)
    chart.GetAxis(i).SetLabelsVisible(False)
    chart.GetAxis(i).SetMargins(1, 1)
    chart.GetAxis(i).SetTitle("")

# Add composite transfer function item.
item = vtkCompositeTransferFunctionItem()
item.SetColorTransferFunction(color_transfer_function)
item.SetOpacityFunction(opacity_function)
item.SetMaskAboveCurve(True)
chart.AddPlot(item)

# Add composite control points with opacity handles.
control_points = vtkCompositeControlPointsItem()
control_points.SetColorTransferFunction(color_transfer_function)
control_points.SetOpacityFunction(opacity_function)
control_points.SetEndPointsXMovable(False)
control_points.SetUseOpacityPointHandles(True)
control_points.SetEndPointsRemovable(False)
chart.AddPlot(control_points)

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
render_window.SetWindowName("control points handle item")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
