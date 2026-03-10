#!/usr/bin/env python

# Animate a sphere using a repeating timer event.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.200, 0.631, 0.788)
misty_rose_rgb = (1.0, 0.894, 0.882)


class TimerCallback:
    """Move the actor on each timer tick, then destroy the timer."""

    def __init__(self, steps, actor, interactor):
        self.timer_count = 0
        self.steps = steps
        self.actor = actor
        self.interactor = interactor
        self.timer_id = None

    def execute(self, obj, event):
        step = 0
        while step < self.steps:
            self.actor.SetPosition(
                self.timer_count / 100.0, self.timer_count / 100.0, 0
            )
            obj.GetRenderWindow().Render()
            self.timer_count += 1
            step += 1
        if self.timer_id:
            obj.DestroyTimer(self.timer_id)


# Source: generate a sphere
sphere = vtkSphereSource()
sphere.SetRadius(2.0)
sphere.SetPhiResolution(30)
sphere.SetThetaResolution(30)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peacock_rgb)
actor.GetProperty().SetSpecular(0.6)
actor.GetProperty().SetSpecularPower(30)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(misty_rose_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(0.8)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Animation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Timer: create a repeating timer that drives the animation callback
cb = TimerCallback(200, actor, render_window_interactor)
render_window_interactor.AddObserver("TimerEvent", cb.execute)

# Launch the interactive visualization
render_window_interactor.Initialize()
cb.timer_id = render_window_interactor.CreateRepeatingTimer(500)
render_window_interactor.Start()
