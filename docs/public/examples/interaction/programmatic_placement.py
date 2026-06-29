#!/usr/bin/env python
# Demonstrate programmatic placement of vtkDistanceWidget in 2D and 3D.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkDistanceRepresentation2D,
    vtkDistanceRepresentation3D,
    vtkDistanceWidget,
    vtkPointHandleRepresentation2D,
    vtkPointHandleRepresentation3D,
)
from vtkmodules.vtkRenderingAnnotation import vtkAxisActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
sphere_source = vtkSphereSource()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("programmatic placement")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget 1: 2D distance widget with ruler mode
handle_2d = vtkPointHandleRepresentation2D()
handle_2d.GetProperty().SetColor(1, 0, 0)

d_rep = vtkDistanceRepresentation2D()
d_rep.SetHandleRepresentation(handle_2d)
d_rep.InstantiateHandleRepresentation()
vtkAxisActor2D.SafeDownCast(d_rep.GetAxis()).SetTickLength(9)
vtkAxisActor2D.SafeDownCast(d_rep.GetAxis()).SetTitlePosition(0.2)
d_rep.RulerModeOn()
d_rep.SetRulerDistance(0.25)

d_widget = vtkDistanceWidget()
d_widget.SetInteractor(interactor)
d_widget.SetRepresentation(d_rep)
d_widget.SetWidgetStateToManipulate()

# Widget 2: 3D distance widget with ruler mode
handle_3d = vtkPointHandleRepresentation3D()
handle_3d.GetProperty().SetColor(1, 1, 0)

d_rep_2 = vtkDistanceRepresentation3D()
d_rep_2.SetHandleRepresentation(handle_3d)
d_rep_2.InstantiateHandleRepresentation()
d_rep_2.RulerModeOn()
d_rep_2.SetRulerDistance(0.25)

d_widget_2 = vtkDistanceWidget()
d_widget_2.SetInteractor(interactor)
d_widget_2.SetRepresentation(d_rep_2)
d_widget_2.SetWidgetStateToManipulate()

# Render to establish display coordinate system before enabling widgets
render_window.Render()
d_widget.On()
d_widget_2.On()

# Set 2D widget endpoints in display coordinates
d_rep.SetPoint1DisplayPosition((25, 50, 0))
d_rep.SetPoint2DisplayPosition((275, 250, 0))

# Set 3D widget endpoints in world coordinates
d_rep_2.SetPoint1WorldPosition((-0.75, 0.75, 0))
d_rep_2.SetPoint2WorldPosition((0.75, -0.75, 0))

interactor.Initialize()
interactor.Start()
