#!/usr/bin/env python

# Display a movable text overlay on a sphere using a text widget.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkTextRepresentation,
    vtkTextWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.0, 0.894, 0.882)
midnight_blue_rgb = (0.098, 0.098, 0.439)
lime_rgb = (0.0, 1.0, 0.0)

# Source: generate a sphere
source = vtkSphereSource()

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("TextWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# TextActor: the text to display
text_actor = vtkTextActor()
text_actor.SetInput("This is a test")
text_actor.GetTextProperty().SetColor(lime_rgb)

# TextRepresentation: position the text overlay
text_representation = vtkTextRepresentation()
text_representation.GetPositionCoordinate().SetValue(0.15, 0.15)
text_representation.GetPosition2Coordinate().SetValue(0.7, 0.2)

# TextWidget: interactive text overlay (SelectableOff allows moving the widget)
text_widget = vtkTextWidget()
text_widget.SetRepresentation(text_representation)
text_widget.SetInteractor(render_window_interactor)
text_widget.SetTextActor(text_actor)
text_widget.SelectableOff()

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window.Render()
text_widget.On()
render_window_interactor.Start()
