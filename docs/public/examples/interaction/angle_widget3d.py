#!/usr/bin/env python
# Demonstrate vtkAngleWidget with 3D angle representation on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkAngleRepresentation3D,
    vtkAngleWidget,
    vtkPointHandleRepresentation3D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere actor
sphere = vtkSphereSource()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("angle widget3d")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Angle representation
handle = vtkPointHandleRepresentation3D()
handle.GetProperty().SetColor(1, 0, 0)

rep = vtkAngleRepresentation3D()
rep.SetHandleRepresentation(handle)
rep.SetScale(math.pi / 180.0)
rep.SetLabelFormat("{:<#6.3g} rad")


# Callback for angle widget events
def angle_callback(widget, event_string):
    point1 = rep.GetPoint1WorldPosition()
    center = rep.GetCenterWorldPosition()
    point2 = rep.GetPoint2WorldPosition()
    print(f"Angle: {rep.GetAngle():.3f} rad")


# Widget
angle_widget = vtkAngleWidget()
angle_widget.SetInteractor(interactor)
angle_widget.CreateDefaultRepresentation()
angle_widget.SetRepresentation(rep)
angle_widget.AddObserver("PlacePointEvent", angle_callback)
angle_widget.AddObserver("InteractionEvent", angle_callback)
angle_widget.On()

interactor.Initialize()
interactor.Start()
