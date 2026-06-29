#!/usr/bin/env python
# Demonstrate vtkCaptionWidget with a text caption anchored to a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkCaptionRepresentation,
    vtkCaptionWidget,
)
from vtkmodules.vtkRenderingAnnotation import vtkCaptionActor2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere actor offset in world space
sphere = vtkSphereSource()
sphere.SetCenter(100, 250, 500)
sphere.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("caption widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
rep = vtkCaptionRepresentation()
rep.SetAnchorPosition(sphere.GetOutput().GetPoint(0))
vtkCaptionActor2D.SafeDownCast(rep.GetCaptionActor2D()).SetCaption("This is a test caption\nAnd it has two lines")
vtkCaptionActor2D.SafeDownCast(rep.GetCaptionActor2D()).GetTextActor().GetTextProperty().SetJustificationToCentered()
vtkCaptionActor2D.SafeDownCast(rep.GetCaptionActor2D()).GetTextActor().GetTextProperty().SetVerticalJustificationToCentered()

caption_widget = vtkCaptionWidget()
caption_widget.SetInteractor(interactor)
caption_widget.SetRepresentation(rep)
caption_widget.On()

interactor.Initialize()
interactor.Start()
