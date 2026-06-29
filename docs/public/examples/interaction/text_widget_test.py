#!/usr/bin/env python
# Demonstrate vtkTextWidget overlaid on a sphere actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import vtkTextWidget
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
render_window.SetWindowName("text widget test")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
text_actor = vtkTextActor()
text_actor.SetInput("This is a test")
text_actor.GetTextProperty().SetColor(0, 1, 0)

text_widget = vtkTextWidget()
text_widget.SetInteractor(interactor)
text_widget.SetTextActor(text_actor)
text_widget.GetRepresentation().GetPositionCoordinate().SetValue(0.15, 0.15)
text_widget.GetRepresentation().GetPosition2Coordinate().SetValue(0.7, 0.2)
text_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
