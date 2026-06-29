#!/usr/bin/env python
# Demonstrate adding, retrieving, and removing duplicate control points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkCompositeControlPointsItem
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create control points item and add points.
control_points = vtkCompositeControlPointsItem()

control_points.AddPoint([0.0, 0.0, 0.5, 0.0])
control_points.AddPoint([50.0, 0.2, 0.5, 0.0])
control_points.AddPoint([50.0, 0.8, 0.5, 0.0])
control_points.AddPoint([100.0, 1.0, 0.5, 0.0])

# Verify control point positions.
point0 = [0.0] * 4
point1 = [0.0] * 4
point2 = [0.0] * 4
point3 = [0.0] * 4
control_points.GetControlPoint(0, point0)
control_points.GetControlPoint(1, point1)
control_points.GetControlPoint(2, point2)
control_points.GetControlPoint(3, point3)
print(f"Points: {point0[0]}, {point1[0]}, {point2[0]}, {point3[0]}")

# Remove duplicate point at index 2.
control_points.RemovePoint(2)
control_points.GetControlPoint(1, point1)
print(f"After remove: point1 = ({point1[0]}, {point1[1]})")

print("CompositeControlPointsItem completed successfully.")

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
render_window.SetWindowName("composite control points item")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
