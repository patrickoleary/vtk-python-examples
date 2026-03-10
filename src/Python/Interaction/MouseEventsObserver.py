#!/usr/bin/env python

# Demonstrate observer callbacks with priorities on the interactor.  Two
# observers are registered for LeftButtonPressEvent with different priorities;
# the higher-priority observer executes first.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.0, 0.894, 0.882)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: generate a sphere
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1)

# Mapper: map sphere polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(misty_rose_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("MouseEventsObserver")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetInteractorStyle(vtkInteractorStyleTrackballCamera())
interactor.SetRenderWindow(render_window)


# Observer callbacks: priority controls execution order (highest first)
def before_event(obj, ev):
    print("Before Event")


def after_event(obj, ev):
    print("After Event")


interactor.RemoveObservers("LeftButtonPressEvent")
interactor.AddObserver("LeftButtonPressEvent", before_event, 1.0)
interactor.AddObserver("LeftButtonPressEvent", after_event, -1.0)

# Launch the interactive visualization
interactor.Initialize()
interactor.Start()
