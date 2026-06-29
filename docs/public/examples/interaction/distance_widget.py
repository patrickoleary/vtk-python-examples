#!/usr/bin/env python
# Demonstrate vtkDistanceWidget with 2D distance measurement on a sphere actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkDistanceRepresentation2D,
    vtkDistanceWidget,
    vtkPointHandleRepresentation2D,
)
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source + Mapper + Actor
sphere = vtkSphereSource()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("distance widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback prints distance on interaction
def distance_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    pos1 = widget_rep.GetPoint1WorldPosition()
    pos2 = widget_rep.GetPoint2WorldPosition()
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    print(f"Distance: {dist:.4f}")


# Widget
handle_rep = vtkPointHandleRepresentation2D()
handle_rep.GetProperty().SetColor(1, 0, 0)

distance_rep = vtkDistanceRepresentation2D()
distance_rep.SetHandleRepresentation(handle_rep)

axis = vtkAxisActor2D.SafeDownCast(distance_rep.GetAxis())
axis.GetTitleTextProperty().SetFontSize(40)
axis.SetTickLength(9)
axis.SetTitlePosition(0.2)

distance_rep.RulerModeOn()
distance_rep.SetRulerDistance(0.25)
distance_rep.SetScale(0.5)
distance_rep.GetAxisProperty().SetColor(1.0, 0.0, 1.0)

distance_widget = vtkDistanceWidget()
distance_widget.SetInteractor(interactor)
distance_widget.CreateDefaultRepresentation()
distance_widget.SetRepresentation(distance_rep)
distance_widget.AddObserver("InteractionEvent", distance_callback)
distance_widget.AddObserver("EndInteractionEvent", distance_callback)
distance_widget.On()

interactor.Initialize()
interactor.Start()
