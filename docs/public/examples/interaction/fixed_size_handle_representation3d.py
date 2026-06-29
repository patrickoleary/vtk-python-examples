#!/usr/bin/env python
# Demonstrate vtkFixedSizeHandleRepresentation3D with a handle on a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkFixedSizeHandleRepresentation3D,
    vtkHandleWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source + Mapper + Actor
sphere = vtkSphereSource()
sphere.SetRadius(10.0)
sphere.SetCenter(0, 0, 0)
sphere.Update()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("fixed size handle representation3d")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Render the window to ensure it's ready
render_window.Render()

# Callback prints handle position during interaction
def handle_callback(caller, event_string):
    pos = caller.GetRepresentation().GetWorldPosition()
    print(f"Handle position: ({pos[0]},{pos[1]},{pos[2]})")


# Widget
handle_rep = vtkFixedSizeHandleRepresentation3D()
handle_rep.SetHandleSizeInPixels(10.0)
handle_rep.SetHandleSizeToleranceInPixels(1.0)
handle_rep.GetProperty().SetColor(1, 0, 0)
handle_rep.SetWorldPosition((0, 0, 10))

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetDefaultRenderer(renderer)
handle_widget.SetRepresentation(handle_rep)
handle_widget.AddObserver("InteractionEvent", handle_callback)
handle_widget.On()

interactor.Initialize()
interactor.Start()
