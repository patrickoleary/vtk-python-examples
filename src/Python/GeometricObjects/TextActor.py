#!/usr/bin/env python

# Display a "Hello World!" text overlay using vtkTextActor.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType font rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextActor,
)

# Colors (normalized RGB)
cornsilk_rgb = (1.0, 0.973, 0.863)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Text actor: a 2D overlay with styled text
text_actor = vtkTextActor()
text_actor.SetInput("Hello World!")
text_actor.SetDisplayPosition(20, 30)

text_prop = text_actor.GetTextProperty()
text_prop.SetFontFamilyToArial()
text_prop.BoldOn()
text_prop.SetFontSize(36)
text_prop.ShadowOn()
text_prop.SetShadowOffset(4, 4)
text_prop.SetColor(cornsilk_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(text_actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("TextActor")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
