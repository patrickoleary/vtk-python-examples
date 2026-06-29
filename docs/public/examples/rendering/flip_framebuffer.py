#!/usr/bin/env python

# Demonstrate framebuffer Y-flip with a cone, text overlay, and axes in a viewport.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Main renderer
renderer = vtkRenderer()

# Overlay renderer for axes
overlay = vtkRenderer()
overlay.SetLayer(1)
overlay.SetViewport(0, 0, 0.4, 0.4)

# Cone
cone = vtkConeSource()
cone.SetDirection(0, 1, 0)
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())
actor = vtkActor()
actor.SetMapper(mapper)
renderer.AddActor(actor)

# Text actor
text_actor = vtkTextActor()
text_actor.SetInput("FlipY Tests")
text_actor.GetTextProperty().SetFontSize(30)
renderer.AddActor(text_actor)

# Axes in overlay
axes = vtkAxesActor()
overlay.AddActor(axes)

# Render window with framebuffer flip
render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer)
render_window.AddRenderer(overlay)
render_window.FramebufferFlipYOn()
render_window.SetWindowName("flip framebuffer")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
