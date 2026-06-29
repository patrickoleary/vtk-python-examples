#!/usr/bin/env python
# Demonstrate vtkColorTransferControlPointsItem API for moving and spreading control points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkColorTransferControlPointsItem
from vtkmodules.vtkCommonCore import vtkIdTypeArray
from vtkmodules.vtkCommonDataModel import vtkVector2f
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a color transfer function.
transfer_function = vtkColorTransferFunction()
transfer_function.AddHSVSegment(50.0, 0.0, 1.0, 1.0, 85.0, 0.3333, 1.0, 1.0)
transfer_function.AddHSVSegment(85.0, 0.3333, 1.0, 1.0, 170.0, 0.6666, 1.0, 1.0)
transfer_function.AddHSVSegment(170.0, 0.6666, 1.0, 1.0, 200.0, 0.0, 1.0, 1.0)

control_points = vtkColorTransferControlPointsItem()
control_points.SetColorTransferFunction(transfer_function)

# Verify number of points.
assert control_points.GetNumberOfPoints() == 4
assert control_points.GetNumberOfSelectedPoints() == 0

# Get control point IDs (excluding endpoints).
ids = vtkIdTypeArray()
control_points.GetControlPointsIds(ids, True)
assert ids.GetNumberOfValues() == 2
assert ids.GetValue(0) == 1
assert ids.GetValue(1) == 2

# Get all control point IDs.
control_points.GetControlPointsIds(ids)
assert ids.GetNumberOfValues() == 4

# Check bounds.
bounds = [0.0] * 4
control_points.GetBounds(bounds)
assert bounds[0] == 50.0
assert bounds[1] == 200.0

# Move points.
control_points.MovePoints(vtkVector2f(1.0, 0.0), ids)

point0 = [0.0] * 4
point1 = [0.0] * 4
point2 = [0.0] * 4
point3 = [0.0] * 4
control_points.GetControlPoint(0, point0)
control_points.GetControlPoint(1, point1)
control_points.GetControlPoint(2, point2)
control_points.GetControlPoint(3, point3)
assert point0[0] == 51.0
assert point1[0] == 86.0
assert point2[0] == 171.0
assert point3[0] == 200.0

# Spread points.
control_points.SpreadPoints(1.0, ids)

control_points.GetControlPoint(0, point0)
control_points.GetControlPoint(1, point1)
control_points.GetControlPoint(2, point2)
control_points.GetControlPoint(3, point3)
assert point0[0] == 51.0
assert point1[0] < 86.0
assert point2[0] > 171.0
assert point3[0] == 200.0

control_points.SpreadPoints(-1.0, ids)

control_points.GetControlPoint(0, point0)
control_points.GetControlPoint(1, point1)
control_points.GetControlPoint(2, point2)
control_points.GetControlPoint(3, point3)
assert point0[0] == 52.0
assert point3[0] == 199.0

print("All assertions passed.")

# Add the control points item to a chart for visualization.
chart = vtkChartXY()
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
render_window.SetSize(600, 350)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("color transfer control points item")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
