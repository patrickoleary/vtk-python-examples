#!/usr/bin/env python

# Display an interactive orientation marker with coordinate axes in the viewport.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose = (1.000, 0.894, 0.882)
slate_gray = (0.439, 0.502, 0.565)
carrot = (0.929, 0.569, 0.129)

# Source: generate sphere polygon data
source = vtkSphereSource()
source.SetCenter(0.0, 0.0, 0.0)
source.SetRadius(1.0)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(misty_rose)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray)
renderer.GetActiveCamera().Azimuth(50)
renderer.GetActiveCamera().Elevation(-30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("DisplayCoordinateAxes")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Widget: add an interactive orientation marker showing coordinate axes
axes = vtkAxesActor()
widget = vtkOrientationMarkerWidget()
widget.SetOutlineColor(carrot[0], carrot[1], carrot[2])
widget.SetOrientationMarker(axes)
widget.SetInteractor(render_window_interactor)
widget.SetViewport(0.0, 0.0, 0.4, 0.4)
widget.SetEnabled(1)
widget.InteractiveOn()

# Launch the interactive visualization
render_window_interactor.Start()
