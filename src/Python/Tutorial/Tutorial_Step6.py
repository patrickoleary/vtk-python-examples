#!/usr/bin/env python

# Tutorial Step 6: introduce 3D widgets with a box widget for transforming an actor.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bisque_rgb = (1.0, 0.894, 0.769)
midnight_blue_rgb = (0.098, 0.098, 0.439)
gold_rgb = (1.0, 0.843, 0.0)

# Source: create a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(bisque_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Tutorial_Step6")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# InteractorStyle: trackball camera for intuitive navigation
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)


# BoxWidget callback: 3D widgets take advantage of the event/observer
# pattern. As the widget is manipulated it invokes InteractionEvent which
# we observe to apply the widget's transform to the actor.
class BoxWidgetCallback:
    def __call__(self, caller, event):
        t = vtkTransform()
        caller.GetTransform(t)
        caller.GetProp3D().SetUserTransform(t)


# BoxWidget: a 3D widget that can be interactively selected and manipulated
# using the mouse. SetInteractor connects the widget to the render window
# interactor via the Command/Observer mechanism. The place factor controls
# the initial size of the widget relative to the bounding box of its input.
box_widget = vtkBoxWidget()
box_widget.SetInteractor(render_window_interactor)
box_widget.SetPlaceFactor(1.25)
box_widget.GetOutlineProperty().SetColor(gold_rgb)

# Place the widget around the cone actor. The EndInteractionEvent and
# InteractionEvent are observed to apply transformations to the actor.
box_widget.SetProp3D(cone_actor)
box_widget.PlaceWidget()
box_widget.AddObserver("InteractionEvent", BoxWidgetCallback())

# Normally the user presses 'i' to bring a 3D widget to life. Here we
# manually enable it so it appears with the cone.
box_widget.On()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
