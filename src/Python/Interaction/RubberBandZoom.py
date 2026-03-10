#!/usr/bin/env python

# Demonstrate vtkInteractorStyleRubberBandZoom, which allows the user to
# draw a rectangle to zoom into a region of the scene.  A grid of spheres
# provides visual context for the zoom operation.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleRubberBandZoom
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.SetBackground(dark_slate_gray_rgb)

# Grid: create a 5x5 grid of spheres
for row in range(5):
    for col in range(5):
        sphere = vtkSphereSource()
        sphere.SetCenter(col * 2.5, row * 2.5, 0)
        sphere.SetRadius(0.8)
        sphere.SetPhiResolution(16)
        sphere.SetThetaResolution(16)

        mapper = vtkPolyDataMapper()
        mapper.SetInputConnection(sphere.GetOutputPort())

        actor = vtkActor()
        actor.SetMapper(mapper)
        hue = (row * 5 + col) / 25.0
        actor.GetProperty().SetColor(
            0.5 + 0.5 * abs(2.0 * hue - 1.0),
            0.7 * (1.0 - hue),
            0.7 * hue,
        )
        renderer.AddActor(actor)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("RubberBandZoom")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Style: rubber-band zoom (draw a rectangle to zoom)
style = vtkInteractorStyleRubberBandZoom()
interactor.SetInteractorStyle(style)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
