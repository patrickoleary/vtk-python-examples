#!/usr/bin/env python
# Demonstrate vtkAxis with log scale and scientific notation.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a vertical axis with log scale.
axis_vertical = vtkAxis()
axis_vertical.LogScaleOn()
axis_vertical.SetPoint1(180, 16)
axis_vertical.SetPoint2(180, 184)
axis_vertical.SetPosition(vtkAxis.LEFT)
axis_vertical.SetNotation(vtkAxis.SCIENTIFIC_NOTATION)
axis_vertical.SetPrecision(0)
axis_vertical.SetRange(0.1, 1000000.0)
axis_vertical.SetRangeLabelsVisible(True)
axis_vertical.GetLabelProperties().SetFontSize(24)

# Standard rendering pipeline with vtkContextActor.
context_actor = vtkContextActor()
context_actor.GetScene().AddItem(axis_vertical)

renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
context_actor.GetScene().SetRenderer(renderer)
renderer.AddActor(context_actor)

axis_vertical.Update()

# Window
render_window = vtkRenderWindow()
render_window.SetSize(200, 200)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("axis log scale")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
