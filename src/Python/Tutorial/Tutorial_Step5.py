#!/usr/bin/env python

# Tutorial Step 5: introduce interaction with a trackball camera style.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bisque_rgb = (1.0, 0.894, 0.769)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Source: create a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.GetProperty().SetColor(bisque_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(cone_actor)
renderer.SetBackground(midnight_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Tutorial_Step5")

# Interactor: the vtkRenderWindowInteractor watches for events (keypress,
# mouse) in the render window and translates them into VTK event invocations
# that observers can process.
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# InteractorStyle: by default the interactor uses vtkInteractorStyle which
# translates events into operations on cameras, actors, and properties.
# Here we explicitly set vtkInteractorStyleTrackballCamera for intuitive
# trackball-style rotation, panning, and zooming.
style = vtkInteractorStyleTrackballCamera()
render_window_interactor.SetInteractorStyle(style)

# Launch the interactive visualization.
# Unlike the previous tutorial steps which animated and exited, here we
# leave an event loop running. The user can interact with the scene using
# the mouse and keyboard. Press 'e' to exit.
render_window_interactor.Initialize()
render_window_interactor.Start()
