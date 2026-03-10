#!/usr/bin/env python

# Interactive demo of a super-ellipsoid parametric surface.  Two sliders
# control the N1 (Z squareness) and N2 (XY squareness) exponents.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonComputationalGeometry import vtkParametricSuperEllipsoid
from vtkmodules.vtkCommonCore import vtkCommand
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

# Source: parametric super-ellipsoid surface
surface = vtkParametricSuperEllipsoid()
surface.SetN1(1.0)
surface.SetN2(1.0)

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
render_window.SetWindowName("ParametricSuperEllipsoidApp")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Shared slider dimensions
tube_width = 0.008
slider_length = 0.008
title_height = 0.04
label_height = 0.04

# ---- Slider: N1 / Z squareness (bottom edge, horizontal) ----
n1_rep = vtkSliderRepresentation2D()
n1_rep.SetMinimumValue(0.0)
n1_rep.SetMaximumValue(4.0)
n1_rep.SetValue(1.0)
n1_rep.SetTitleText("Z squareness")
n1_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
n1_rep.GetPoint1Coordinate().SetValue(0.1, 0.1)
n1_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
n1_rep.GetPoint2Coordinate().SetValue(0.9, 0.1)
n1_rep.SetTubeWidth(tube_width)
n1_rep.SetSliderLength(slider_length)
n1_rep.SetTitleHeight(title_height)
n1_rep.SetLabelHeight(label_height)

n1_widget = vtkSliderWidget()
n1_widget.SetInteractor(render_window_interactor)
n1_widget.SetRepresentation(n1_rep)
n1_widget.SetAnimationModeToAnimate()
n1_widget.EnabledOn()
n1_widget.AddObserver(
    vtkCommand.InteractionEvent,
    lambda obj, ev: surface.SetN1(obj.GetRepresentation().GetValue()),
)

# ---- Slider: N2 / XY squareness (top edge, horizontal) ----
n2_rep = vtkSliderRepresentation2D()
n2_rep.SetMinimumValue(0.0001)
n2_rep.SetMaximumValue(4.0)
n2_rep.SetValue(1.0)
n2_rep.SetTitleText("XY squareness")
n2_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
n2_rep.GetPoint1Coordinate().SetValue(0.1, 0.9)
n2_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
n2_rep.GetPoint2Coordinate().SetValue(0.9, 0.9)
n2_rep.SetTubeWidth(tube_width)
n2_rep.SetSliderLength(slider_length)
n2_rep.SetTitleHeight(title_height)
n2_rep.SetLabelHeight(label_height)

n2_widget = vtkSliderWidget()
n2_widget.SetInteractor(render_window_interactor)
n2_widget.SetRepresentation(n2_rep)
n2_widget.SetAnimationModeToAnimate()
n2_widget.EnabledOn()
n2_widget.AddObserver(
    vtkCommand.InteractionEvent,
    lambda obj, ev: surface.SetN2(obj.GetRepresentation().GetValue()),
)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
