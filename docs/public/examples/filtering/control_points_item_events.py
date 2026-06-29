#!/usr/bin/env python
# Demonstrate control points item events with add, drag, move, and double-click.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkColorTransferControlPointsItem
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

# Create control points item.
control_points = vtkColorTransferControlPointsItem()
control_points.SetColorTransferFunction(transfer_function)

# Set up a chart.
chart = vtkChartXY()
chart.AddPlot(control_points)

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
render_window.SetWindowName("control points item events")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
