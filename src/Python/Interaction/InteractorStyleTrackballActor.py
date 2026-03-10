#!/usr/bin/env python

# Demonstrate vtkInteractorStyleTrackballActor, which allows the user to
# rotate, pan, and scale individual actors independently with the mouse.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
chartreuse_rgb = (0.498, 1.0, 0.0)
pale_goldenrod_rgb = (0.933, 0.910, 0.667)

# Source: generate a sphere
sphere = vtkSphereSource()

# Mapper: map sphere polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(chartreuse_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(pale_goldenrod_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("InteractorStyleTrackballActor")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Style: trackball-actor mode (mouse manipulates individual actors)
style = vtkInteractorStyleTrackballActor()
interactor.SetInteractorStyle(style)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
