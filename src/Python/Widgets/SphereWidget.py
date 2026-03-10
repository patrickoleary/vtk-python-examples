#!/usr/bin/env python

# Use a sphere widget to interactively position a sphere in the scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkInteractionWidgets import vtkSphereWidget
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
midnight_blue_rgb = (0.098, 0.098, 0.439)
burlywood_rgb = (0.871, 0.722, 0.529)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("SphereWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# SphereWidget: interactive sphere that can be repositioned and resized
sphere_widget = vtkSphereWidget()
sphere_widget.SetInteractor(render_window_interactor)
sphere_widget.SetRepresentationToSurface()
sphere_widget.GetSphereProperty().SetColor(burlywood_rgb)

sphere_widget.AddObserver("InteractionEvent",
                          lambda obj, event: print(
                              "Center: {:.3f}, {:.3f}, {:.3f}".format(*obj.GetCenter())))

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window.Render()
sphere_widget.On()
render_window_interactor.Start()
