#!/usr/bin/env python
# Demonstrate vtkAxis with various configurations including custom labels and log scale.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingContextOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkChartsCore import vtkAxis
from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkStringArray
from vtkmodules.vtkRenderingContext2D import vtkContextActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Set up custom label arrays for the axes.
positions = vtkDoubleArray()
labels = vtkStringArray()

positions.InsertNextValue(0.0)
labels.InsertNextValue("0.0")
positions.InsertNextValue(42.0)
labels.InsertNextValue("The Answer")
positions.InsertNextValue(99.0)
labels.InsertNextValue("99")

# Standard rendering pipeline with vtkContextActor.
context_actor = vtkContextActor()
scene = context_actor.GetScene()

renderer = vtkRenderer()
renderer.SetBackground(1.0, 1.0, 1.0)
scene.SetRenderer(renderer)
renderer.AddActor(context_actor)

# Create vertical axes.
vaxis_0 = vtkAxis()
vaxis_0.SetPoint1(30, 10)
vaxis_0.SetPoint2(30, 290)
vaxis_0.SetPosition(vtkAxis.RIGHT)
vaxis_0.SetRange(-1, 50)
scene.AddItem(vaxis_0)

vaxis_1 = vtkAxis()
vaxis_1.SetPoint1(99, 10)
vaxis_1.SetPoint2(99, 290)
vaxis_1.SetPosition(vtkAxis.LEFT)
vaxis_1.SetRange(-1, 50)
scene.AddItem(vaxis_1)

vaxis_2 = vtkAxis()
vaxis_2.SetPoint1(168, 10)
vaxis_2.SetPoint2(168, 290)
vaxis_2.SetPosition(vtkAxis.RIGHT)
vaxis_2.SetRange(-1, 50)
scene.AddItem(vaxis_2)

vaxis_3 = vtkAxis()
vaxis_3.SetPoint1(237, 10)
vaxis_3.SetPoint2(237, 290)
vaxis_3.SetPosition(vtkAxis.LEFT)
vaxis_3.SetRange(-1, 50)
scene.AddItem(vaxis_3)

# Exercise some API.
vaxis_0.AutoScale()
vaxis_0.SetLabelOffset(9)

vaxis_1.SetBehavior(vtkAxis.FIXED)
vaxis_1.AutoScale()
vaxis_1.SetLabelOffset(13)

vaxis_2.SetNotation(vtkAxis.SCIENTIFIC_NOTATION)
vaxis_2.SetPosition(vtkAxis.LEFT)
vaxis_2.SetPrecision(0)
vaxis_2.SetRange(3.2, 97.0)
vaxis_2.SetRangeLabelsVisible(True)
vaxis_2.SetRangeLabelFormat("{:3.1f}")

vaxis_3.SetTitle("Custom vertical labels")
vaxis_3.SetCustomTickPositions(positions, labels)
vaxis_3.SetPoint1(3 * 69 + 80, 10)
vaxis_3.SetPoint2(3 * 69 + 80, 290)
vaxis_3.AutoScale()

vaxis_0.Update()
vaxis_1.Update()
vaxis_2.Update()
vaxis_3.Update()

# Create horizontal axes.
haxis_0 = vtkAxis()
haxis_0.SetPoint1(310, 30)
haxis_0.SetPoint2(490, 30)
haxis_0.SetPosition(vtkAxis.BOTTOM)
haxis_0.SetRange(-1, 50)
scene.AddItem(haxis_0)
haxis_0.Update()

haxis_1 = vtkAxis()
haxis_1.SetPoint1(310, 80)
haxis_1.SetPoint2(490, 80)
haxis_1.SetPosition(vtkAxis.TOP)
haxis_1.SetRange(-1, 50)
scene.AddItem(haxis_1)
haxis_1.Update()

haxis_2 = vtkAxis()
haxis_2.SetPoint1(310, 130)
haxis_2.SetPoint2(490, 130)
haxis_2.SetPosition(vtkAxis.BOTTOM)
haxis_2.SetRange(-1, 50)
scene.AddItem(haxis_2)
haxis_2.Update()

haxis_3 = vtkAxis()
haxis_3.SetPoint1(310, 180)
haxis_3.SetPoint2(490, 180)
haxis_3.SetPosition(vtkAxis.TOP)
haxis_3.SetRange(-1, 50)
scene.AddItem(haxis_3)
haxis_3.Update()

haxis_4 = vtkAxis()
haxis_4.SetPoint1(310, 230)
haxis_4.SetPoint2(490, 230)
haxis_4.SetPosition(vtkAxis.BOTTOM)
haxis_4.SetRange(-1, 50)
scene.AddItem(haxis_4)
haxis_4.Update()

haxis_5 = vtkAxis()
haxis_5.SetPoint1(310, 280)
haxis_5.SetPoint2(490, 280)
haxis_5.SetPosition(vtkAxis.TOP)
haxis_5.SetRange(-1, 50)
scene.AddItem(haxis_5)
haxis_5.Update()

# Exercise more API.
haxis_0.LogScaleOn()
haxis_0.SetUnscaledRange(1, 100)
haxis_0.LogScaleOff()
haxis_0.AutoScale()
haxis_0.SetRange(20, 60)

haxis_1.SetRange(10, -10)
haxis_1.AutoScale()

haxis_2.SetRange(10, -5)
haxis_2.SetBehavior(vtkAxis.FIXED)
haxis_2.AutoScale()
haxis_2.SetTitle("Test")

haxis_3.SetTickLabelAlgorithm(vtkAxis.TICK_WILKINSON_EXTENDED)
haxis_3.AutoScale()

haxis_4.SetNumberOfTicks(5)

haxis_5.SetTitle("Custom horizontal labels")
haxis_5.SetCustomTickPositions(positions, labels)
haxis_5.SetPosition(vtkAxis.BOTTOM)

haxis_0.Update()
haxis_1.Update()
haxis_2.Update()
haxis_3.Update()
haxis_4.Update()
haxis_5.Update()

# Window
render_window = vtkRenderWindow()
render_window.SetSize(500, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("axes")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
