#!/usr/bin/env python
# Demonstrate range handles item events with color transfer function and event replay.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkChartXY, vtkRangeHandlesItem
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

# Create range handles.
range_handles = vtkRangeHandlesItem()
range_handles.SetColorTransferFunction(transfer_function)
range_handles.ComputeHandlesDrawRange()

# Check initialization.
handle_range = [0.0, 0.0]
range_handles.GetHandlesRange(handle_range)
print(f"Initial range: [{handle_range[0]}, {handle_range[1]}]")

# Set up chart.
chart = vtkChartXY()
chart.AddPlot(range_handles)

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
render_window.SetWindowName("range handles item events")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
