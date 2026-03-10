#!/usr/bin/env python

# Use a compass widget to control camera heading, tilt, and distance.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkCommand,
    vtkMath,
)
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

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Actor: an annotated cube to orient the camera around
actor = vtkAnnotatedCubeActor()
actor.GetCubeProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("CompassWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# CompassWidget: heading / tilt / distance controls
compass_rep = vtkCompassRepresentation()
compass_rep.SetMinimumDistance(2)
compass_rep.SetMaximumDistance(10)

compass_widget = vtkCompassWidget()
compass_widget.SetInteractor(render_window_interactor)
compass_widget.SetRepresentation(compass_rep)
compass_widget.SetDistance(5)
compass_widget.SetTiltSpeed(45)
compass_widget.SetDistanceSpeed(2)


def compass_callback(widget, event):
    try:
        camera = widget.GetCurrentRenderer().GetActiveCamera()
    except AttributeError:
        return

    distance = widget.GetDistance()
    tilt = widget.GetTilt()
    heading = widget.GetHeading()

    x = distance * math.cos(vtkMath.RadiansFromDegrees(heading)) * math.cos(vtkMath.RadiansFromDegrees(tilt))
    y = distance * math.sin(vtkMath.RadiansFromDegrees(heading)) * math.cos(vtkMath.RadiansFromDegrees(tilt))
    z = distance * math.sin(vtkMath.RadiansFromDegrees(tilt))

    camera.SetPosition(x, y, z)
    camera.SetFocalPoint(0, 0, 0)
    camera.SetViewUp(0, 0, 1)
    camera.SetClippingRange(0.1, distance + 1)

    widget.GetCurrentRenderer().Render()


compass_widget.AddObserver(vtkCommand.WidgetValueChangedEvent, compass_callback)

# Launch the interactive visualization
render_window.Render()
compass_widget.EnabledOn()

# Camera is moved by widget callback — disable default interactor style
render_window_interactor.SetInteractorStyle(None)
compass_widget.InvokeEvent(vtkCommand.WidgetValueChangedEvent)

render_window_interactor.Start()
