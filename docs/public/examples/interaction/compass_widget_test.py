#!/usr/bin/env python
# Demonstrate vtkCompassWidget controlling camera position on an annotated cube.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkInteractionWidgets import (
    vtkCompassRepresentation,
    vtkCompassWidget,
)
from vtkmodules.vtkRenderingAnnotation import vtkAnnotatedCubeActor
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Actor
actor = vtkAnnotatedCubeActor()
actor.GetCubeProperty().SetColor(0, 0, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("compass widget test")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(None)


# Callback updates camera position from compass widget parameters
def value_changed_callback(caller, event_string):
    camera = caller.GetCurrentRenderer().GetActiveCamera()
    distance = caller.GetDistance()
    tilt = caller.GetTilt()
    heading = caller.GetHeading()

    pos = [0.0, 0.0, 0.0]
    pos[0] = distance * math.cos(math.radians(heading)) * math.cos(math.radians(tilt))
    pos[1] = distance * math.sin(math.radians(heading)) * math.cos(math.radians(tilt))
    pos[2] = distance * math.sin(math.radians(tilt))

    camera.SetPosition(pos)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    camera.SetClippingRange(0.1, distance + 1)

    caller.GetCurrentRenderer().Render()


# Widget
compass_rep = vtkCompassRepresentation()
compass_rep.SetMinimumDistance(2)
compass_rep.SetMaximumDistance(10)

compass_widget = vtkCompassWidget()
compass_widget.SetInteractor(interactor)
compass_widget.SetRepresentation(compass_rep)
compass_widget.SetDistance(5.0)
compass_widget.SetTiltSpeed(45)
compass_widget.SetDistanceSpeed(2)
compass_widget.AddObserver("WidgetValueChangedEvent", value_changed_callback)
compass_widget.EnabledOn()

interactor.Initialize()
interactor.Start()
