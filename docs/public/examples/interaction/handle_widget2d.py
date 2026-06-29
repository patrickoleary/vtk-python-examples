#!/usr/bin/env python
# Demonstrate vtkHandleWidget with 2D point handle representations and disk actors.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkCursor2D
from vtkmodules.vtkFiltersSources import vtkDiskSource
from vtkmodules.vtkInteractionWidgets import (
    vtkHandleWidget,
    vtkPointHandleRepresentation2D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source + Mapper + Actor: disk 0
disk_source_0 = vtkDiskSource()
disk_source_0.SetInnerRadius(0.0)
disk_source_0.SetOuterRadius(2)

disk_mapper_0 = vtkPolyDataMapper2D()
disk_mapper_0.SetInputConnection(disk_source_0.GetOutputPort())

disk_actor_0 = vtkActor2D()
disk_actor_0.SetMapper(disk_mapper_0)
disk_actor_0.SetPosition(165, 180)

# Source + Mapper + Actor: disk 1
disk_source_1 = vtkDiskSource()
disk_source_1.SetInnerRadius(0.0)
disk_source_1.SetOuterRadius(2)

disk_mapper_1 = vtkPolyDataMapper2D()
disk_mapper_1.SetInputConnection(disk_source_1.GetOutputPort())

disk_actor_1 = vtkActor2D()
disk_actor_1.SetMapper(disk_mapper_1)
disk_actor_1.SetPosition(50, 50)

# Cursor shape for handles
cursor_2d = vtkCursor2D()
cursor_2d.AllOff()
cursor_2d.AxesOn()
cursor_2d.OutlineOn()
cursor_2d.SetRadius(4)
cursor_2d.Update()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(disk_actor_0)
renderer.AddActor(disk_actor_1)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("handle widget2d")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callbacks
def handle_callback_0(caller, event_string):
    pos = [0.0, 0.0, 0.0]
    caller.GetRepresentation().GetDisplayPosition(pos)
    disk_actor_0.SetPosition(pos[0], pos[1])


def handle_callback_1(caller, event_string):
    pos = [0.0, 0.0, 0.0]
    caller.GetRepresentation().GetDisplayPosition(pos)
    disk_actor_1.SetPosition(pos[0], pos[1])


# Widget 0: tracks disk_actor_0
handle_rep_0 = vtkPointHandleRepresentation2D()
pos0 = list(disk_actor_0.GetPosition()) + [0.0] if len(disk_actor_0.GetPosition()) < 3 else list(disk_actor_0.GetPosition())
handle_rep_0.SetDisplayPosition(pos0)
handle_rep_0.ActiveRepresentationOn()
handle_rep_0.SetCursorShape(cursor_2d.GetOutput())

handle_widget_0 = vtkHandleWidget()
handle_widget_0.SetInteractor(interactor)
handle_widget_0.SetRepresentation(handle_rep_0)
handle_widget_0.AddObserver("InteractionEvent", handle_callback_0)
handle_widget_0.On()

# Widget 1: tracks disk_actor_1
handle_rep_1 = vtkPointHandleRepresentation2D()
pos1 = list(disk_actor_1.GetPosition()) + [0.0] if len(disk_actor_1.GetPosition()) < 3 else list(disk_actor_1.GetPosition())
handle_rep_1.SetDisplayPosition(pos1)
handle_rep_1.SetCursorShape(cursor_2d.GetOutput())

handle_widget_1 = vtkHandleWidget()
handle_widget_1.SetInteractor(interactor)
handle_widget_1.SetRepresentation(handle_rep_1)
handle_widget_1.AddObserver("InteractionEvent", handle_callback_1)
handle_widget_1.On()

interactor.Initialize()
interactor.Start()
