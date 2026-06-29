#!/usr/bin/env python
# Demonstrate vtkTextWidget with various background and border configurations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkBorderRepresentation,
    vtkBorderWidget,
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
render_window.SetWindowName("text widget background")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widgets
border_rep = vtkBorderRepresentation()
border_rep.ProportionalResizeOn()
border_rep.SetShowBorderToOn()
border_rep.SetPolygonColor(0.0, 1.0, 0.0)
border_rep.SetPolygonOpacity(0.2)

border_widget = vtkBorderWidget()
border_widget.SetInteractor(interactor)
border_widget.SetRepresentation(border_rep)
border_widget.SelectableOff()
border_widget.On()

# Top Left: default text widget
top_left_rep = vtkTextRepresentation()
top_left_rep.ProportionalResizeOff()
top_left_rep.SetShowBorderToOn()
top_left_rep.SetShowPolygonToActive()
top_left_rep.SetPosition(0.05, 0.75)
top_left_rep.SetPosition2(0.3, 0.2)
top_left_rep.SetPolygonColor(1.0, 0.0, 0.0)
top_left_rep.SetPolygonOpacity(0.5)
top_left_rep.SetCornerRadiusStrength(0.5)

top_left_widget = vtkTextWidget()
top_left_widget.SetInteractor(interactor)
top_left_widget.SetRepresentation(top_left_rep)
top_left_widget.On()

# Top Right: always on
top_right_rep = vtkTextRepresentation()
top_right_rep.ProportionalResizeOff()
top_right_rep.SetShowBorderToOn()
top_right_rep.SetShowPolygonToActive()
top_right_rep.SetPosition(0.65, 0.75)
top_right_rep.SetPosition2(0.3, 0.2)
top_right_rep.SetPolygonOpacity(0.5)
top_right_rep.SetPolygonColor(0.0, 1.0, 0.0)

top_right_widget = vtkTextWidget()
top_right_widget.SetInteractor(interactor)
top_right_widget.SetRepresentation(top_right_rep)
top_right_widget.On()

# Bottom Right: auto + always border
bottom_right_rep = vtkTextRepresentation()
bottom_right_rep.ProportionalResizeOff()
bottom_right_rep.SetShowBorderToActive()
bottom_right_rep.SetPosition(0.65, 0.05)
bottom_right_rep.SetPosition2(0.3, 0.2)
bottom_right_rep.SetPolygonColor(1.0, 0.0, 1.0)
bottom_right_rep.SetPolygonOpacity(0.3)
bottom_right_rep.EnforceNormalizedViewportBoundsOn()
bottom_right_rep.SetMinimumNormalizedViewportSize(0.3, 0.2)

bottom_right_widget = vtkTextWidget()
bottom_right_widget.SetInteractor(interactor)
bottom_right_widget.SetRepresentation(bottom_right_rep)
bottom_right_widget.SelectableOff()
bottom_right_widget.On()

# Centre: always-on background for readability
center_rep = vtkTextRepresentation()
center_rep.ProportionalResizeOff()
center_rep.SetShowBorderToActive()
center_rep.SetPosition(0.05, 0.35)
center_rep.SetPosition2(0.6, 0.2)
center_rep.SetPolygonColor(0.0, 0.0, 0.0)
center_rep.SetPolygonOpacity(0.3)
center_rep.SetShowPolygonToOn()
center_rep.EnforceNormalizedViewportBoundsOn()
center_rep.SetMinimumNormalizedViewportSize(0.3, 0.2)

center_text_actor = vtkTextActor()
center_text_actor.SetInput("Lorem Ipsum")
center_text_actor.GetTextProperty().SetColor(1.0, 1.0, 1.0)

center_widget = vtkTextWidget()
center_widget.SetInteractor(interactor)
center_widget.SetRepresentation(center_rep)
center_widget.SetTextActor(center_text_actor)
center_widget.SelectableOff()
center_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
