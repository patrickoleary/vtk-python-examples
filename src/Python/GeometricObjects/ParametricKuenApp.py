#!/usr/bin/env python

# Interactive demo of a Kuen surface (a parametric surface with constant
# negative Gaussian curvature).  Four sliders control the U and V parameter
# ranges.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricKuen
from vtkmodules.vtkCommonCore import (
    vtkCommand,
    vtkMath,
)
from vtkmodules.vtkFiltersSources import vtkParametricFunctionSource
from vtkmodules.vtkInteractionWidgets import (
    vtkSliderRepresentation2D,
    vtkSliderWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
banana_rgb = (0.890, 0.812, 0.341)
background_rgb = (0.102, 0.200, 0.400)

# Source: parametric Kuen surface
surface = vtkParametricKuen()
surface.SetMinimumU(-4.5)
surface.SetMaximumU(4.5)
surface.SetMinimumV(0.05)
surface.SetMaximumV(vtkMath.Pi() - 0.05)

source = vtkParametricFunctionSource()
source.SetParametricFunction(surface)

# Mapper: map the parametric source output
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: front face banana, back face tomato
back_property = vtkProperty()
back_property.SetColor(tomato_rgb)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetBackfaceProperty(back_property)
actor.GetProperty().SetDiffuseColor(banana_rgb)
actor.GetProperty().SetSpecular(0.5)
actor.GetProperty().SetSpecularPower(20)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(-30)
renderer.GetActiveCamera().Zoom(0.9)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ParametricKuenApp")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Shared slider dimensions
tube_width = 0.008
slider_length = 0.008
title_height = 0.02
label_height = 0.02

# ---- Slider: U min (bottom edge, horizontal) ----
u_min_rep = vtkSliderRepresentation2D()
u_min_rep.SetMinimumValue(-4.5)
u_min_rep.SetMaximumValue(4.5)
u_min_rep.SetValue(-4.5)
u_min_rep.SetTitleText("U min")
u_min_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
u_min_rep.GetPoint1Coordinate().SetValue(0.1, 0.1)
u_min_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
u_min_rep.GetPoint2Coordinate().SetValue(0.9, 0.1)
u_min_rep.SetTubeWidth(tube_width)
u_min_rep.SetSliderLength(slider_length)
u_min_rep.SetTitleHeight(title_height)
u_min_rep.SetLabelHeight(label_height)

u_min_widget = vtkSliderWidget()
u_min_widget.SetInteractor(render_window_interactor)
u_min_widget.SetRepresentation(u_min_rep)
u_min_widget.SetAnimationModeToAnimate()
u_min_widget.EnabledOn()


def on_u_min_changed(caller, ev):
    value = caller.GetRepresentation().GetValue()
    if value > 0.9 * surface.GetMaximumU():
        value = 0.99 * surface.GetMaximumU()
        caller.GetRepresentation().SetValue(value)
    surface.SetMinimumU(value)


u_min_widget.AddObserver(vtkCommand.InteractionEvent, on_u_min_changed)

# ---- Slider: U max (top edge, horizontal) ----
u_max_rep = vtkSliderRepresentation2D()
u_max_rep.SetMinimumValue(-4.5)
u_max_rep.SetMaximumValue(4.5)
u_max_rep.SetValue(4.5)
u_max_rep.SetTitleText("U max")
u_max_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
u_max_rep.GetPoint1Coordinate().SetValue(0.1, 0.9)
u_max_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
u_max_rep.GetPoint2Coordinate().SetValue(0.9, 0.9)
u_max_rep.SetTubeWidth(tube_width)
u_max_rep.SetSliderLength(slider_length)
u_max_rep.SetTitleHeight(title_height)
u_max_rep.SetLabelHeight(label_height)

u_max_widget = vtkSliderWidget()
u_max_widget.SetInteractor(render_window_interactor)
u_max_widget.SetRepresentation(u_max_rep)
u_max_widget.SetAnimationModeToAnimate()
u_max_widget.EnabledOn()


def on_u_max_changed(caller, ev):
    value = caller.GetRepresentation().GetValue()
    if value < surface.GetMinimumU() + 0.01:
        value = surface.GetMinimumU() + 0.01
        caller.GetRepresentation().SetValue(value)
    surface.SetMaximumU(value)


u_max_widget.AddObserver(vtkCommand.InteractionEvent, on_u_max_changed)

# ---- Slider: V min (left edge, vertical) ----
v_min_rep = vtkSliderRepresentation2D()
v_min_rep.SetMinimumValue(0.05)
v_min_rep.SetMaximumValue(vtkMath.Pi())
v_min_rep.SetValue(0.0)
v_min_rep.SetTitleText("V min")
v_min_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
v_min_rep.GetPoint1Coordinate().SetValue(0.1, 0.1)
v_min_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
v_min_rep.GetPoint2Coordinate().SetValue(0.1, 0.9)
v_min_rep.SetTubeWidth(tube_width)
v_min_rep.SetSliderLength(slider_length)
v_min_rep.SetTitleHeight(title_height)
v_min_rep.SetLabelHeight(label_height)

v_min_widget = vtkSliderWidget()
v_min_widget.SetInteractor(render_window_interactor)
v_min_widget.SetRepresentation(v_min_rep)
v_min_widget.SetAnimationModeToAnimate()
v_min_widget.EnabledOn()


def on_v_min_changed(caller, ev):
    value = caller.GetRepresentation().GetValue()
    if value > 0.9 * surface.GetMaximumV():
        value = 0.99 * surface.GetMaximumV()
        caller.GetRepresentation().SetValue(value)
    surface.SetMinimumV(value)


v_min_widget.AddObserver(vtkCommand.InteractionEvent, on_v_min_changed)

# ---- Slider: V max (right edge, vertical) ----
v_max_rep = vtkSliderRepresentation2D()
v_max_rep.SetMinimumValue(0.05)
v_max_rep.SetMaximumValue(vtkMath.Pi() - 0.05)
v_max_rep.SetValue(vtkMath.Pi())
v_max_rep.SetTitleText("V max")
v_max_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
v_max_rep.GetPoint1Coordinate().SetValue(0.9, 0.1)
v_max_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
v_max_rep.GetPoint2Coordinate().SetValue(0.9, 0.9)
v_max_rep.SetTubeWidth(tube_width)
v_max_rep.SetSliderLength(slider_length)
v_max_rep.SetTitleHeight(title_height)
v_max_rep.SetLabelHeight(label_height)

v_max_widget = vtkSliderWidget()
v_max_widget.SetInteractor(render_window_interactor)
v_max_widget.SetRepresentation(v_max_rep)
v_max_widget.SetAnimationModeToAnimate()
v_max_widget.EnabledOn()


def on_v_max_changed(caller, ev):
    value = caller.GetRepresentation().GetValue()
    if value < surface.GetMinimumV() + 0.01:
        value = surface.GetMinimumV() + 0.01
        caller.GetRepresentation().SetValue(value)
    surface.SetMaximumV(value)


v_max_widget.AddObserver(vtkCommand.InteractionEvent, on_v_max_changed)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
