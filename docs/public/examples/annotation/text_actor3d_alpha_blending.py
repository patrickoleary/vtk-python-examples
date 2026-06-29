#!/usr/bin/env python

# Test vtkTextActor3D rendering with alpha blending.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingCore import vtkTextActor3D

# Text actor
text_actor = vtkTextActor3D()
text_actor.SetInput("0123456789.")
text_actor.SetPosition(3, 4, 5)
text_actor.GetTextProperty().SetJustificationToCentered()
text_actor.GetTextProperty().SetVerticalJustificationToCentered()
text_actor.GetTextProperty().SetFontFamilyToArial()
text_actor.GetTextProperty().SetFontSize(36)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.0, 0.0, 0.5)
renderer.AddActor(text_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("text actor3d alpha blending")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()
renderer.ResetCamera()
render_window.Render()
interactor.Initialize()
interactor.Start()
