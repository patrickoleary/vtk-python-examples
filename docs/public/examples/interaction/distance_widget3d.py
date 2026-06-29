#!/usr/bin/env python
# Demonstrate vtkDistanceWidget with 3D distance measurement on a sphere actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkDistanceRepresentation3D,
    vtkDistanceWidget,
    vtkPointHandleRepresentation3D,
)
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
render_window.SetWindowName("distance widget3d")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Render the window to ensure it's ready
render_window.Render()

# Callback prints distance on interaction
def distance_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    pos1 = widget_rep.GetPoint1WorldPosition()
    pos2 = widget_rep.GetPoint2WorldPosition()
    dist = math.sqrt(sum((a - b) ** 2 for a, b in zip(pos1, pos2)))
    print(f"Distance: {dist:.4f}")


# Widget
handle_rep = vtkPointHandleRepresentation3D()
handle_rep.GetProperty().SetColor(1, 0, 0)

distance_rep = vtkDistanceRepresentation3D()
distance_rep.SetHandleRepresentation(handle_rep)
distance_rep.RulerModeOn()
distance_rep.SetRulerDistance(0.1)
distance_rep.SetNumberOfRulerTicks(4)
distance_rep.SetGlyphScale(0.1)
distance_rep.GetLineProperty().SetColor(1.0, 0.0, 1.0)
distance_rep.SetLabelPosition(0.45)
distance_rep.GetGlyphActor().GetProperty().SetColor(1.0, 0.0, 0.0)
distance_rep.GetLabelActor().GetProperty().SetColor(0.0, 1.0, 0.0)

distance_widget = vtkDistanceWidget()
distance_widget.SetInteractor(interactor)
distance_widget.SetRepresentation(distance_rep)
distance_widget.AddObserver("InteractionEvent", distance_callback)
distance_widget.AddObserver("EndInteractionEvent", distance_callback)
distance_widget.On()

interactor.Initialize()
interactor.Start()
