#!/usr/bin/env python
# Demonstrate vtkTextRepresentation with styled borders and padding.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkTextRepresentation, vtkTextWidget
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
render_window.SetWindowName("text representation with borders")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
text_actor = vtkTextActor()
text_actor.SetInput("This is a test")
text_actor.GetTextProperty().SetColor(0.0, 1.0, 0.0)

text_rep = vtkTextRepresentation()
text_rep.GetPositionCoordinate().SetValue(0.15, 0.15)
text_rep.GetPosition2Coordinate().SetValue(0.7, 0.2)
text_rep.SetBorderColor(1.0, 0.0, 0.0)
text_rep.SetPolygonColor(0.0, 0.0, 1.0)
text_rep.SetPolygonOpacity(0.5)
text_rep.SetCornerRadiusStrength(0.5)
text_rep.SetBorderThickness(5.0)
text_rep.SetShowBorderToOn()
text_rep.SetPaddingLeft(30)
text_rep.SetPaddingRight(10)
text_rep.SetPaddingTop(20)
text_rep.SetPaddingBottom(10)

text_widget = vtkTextWidget()
text_widget.SetRepresentation(text_rep)
text_widget.SetInteractor(interactor)
text_widget.SetTextActor(text_actor)
text_widget.SelectableOff()
text_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
