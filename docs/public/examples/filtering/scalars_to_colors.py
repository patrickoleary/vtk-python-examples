#!/usr/bin/env python
# Demonstrate composite transfer function and control points items in a chart.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import (
    vtkChartXY,
    vtkCompositeControlPointsItem,
    vtkCompositeTransferFunctionItem,
)
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Color transfer function.
color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddHSVSegment(0.0, 0.0, 1.0, 1.0, 0.3333, 0.3333, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.3333, 0.3333, 1.0, 1.0, 0.6666, 0.6666, 1.0, 1.0)
color_transfer_function.AddHSVSegment(0.6666, 0.6666, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0)
color_transfer_function.Build()

# Opacity function.
opacity_function = vtkPiecewiseFunction()
opacity_function.AddPoint(0.2, 0.0)
opacity_function.AddPoint(0.5, 0.5)
opacity_function.AddPoint(1.0, 1.0)

# Set up a chart.
chart = vtkChartXY()
chart.SetTitle("Chart")
chart.ForceAxesToBoundsOn()

composite_item = vtkCompositeTransferFunctionItem()
composite_item.SetColorTransferFunction(color_transfer_function)
composite_item.SetOpacityFunction(opacity_function)
composite_item.SetMaskAboveCurve(True)
chart.AddPlot(composite_item)

control_points_item = vtkCompositeControlPointsItem()
control_points_item.SetOpacityFunction(opacity_function)
control_points_item.SetColorTransferFunction(color_transfer_function)
chart.AddPlot(control_points_item)

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
render_window.SetWindowName("scalars to colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
