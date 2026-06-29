#!/usr/bin/env python
# Demonstrate vtkOrientationMarkerWidget with a text actor in a sub-viewport.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkTextSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import vtkOrientationMarkerWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
text_source = vtkTextSource()
text_source.SetText("Hello")
text_source.SetForegroundColor(1.0, 0.0, 0.0)
text_source.BackingOff()
text_source.Update()

# Mapper + Actor
text_mapper = vtkPolyDataMapper()
text_mapper.SetInputConnection(text_source.GetOutputPort())

text_actor = vtkActor()
text_actor.SetMapper(text_mapper)

# Renderer (two viewports)
small_view_renderer = vtkRenderer()
small_view_renderer.SetViewport(0.5, 0.5, 0.75, 0.75)
small_view_renderer.SetBackground(0.5, 0.5, 0.5)

background_renderer = vtkRenderer()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(background_renderer)
render_window.AddRenderer(small_view_renderer)
render_window.SetWindowName("orientation marker text")
render_window.SetMultiSamples(0)
render_window.SetSize(450, 300)

# Interactor
style = vtkInteractorStyleImage()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

# Widget
orientation_widget = vtkOrientationMarkerWidget()
orientation_widget.SetInteractor(interactor)
orientation_widget.SetDefaultRenderer(small_view_renderer)
orientation_widget.SetViewport(0, 0, 1, 1)
orientation_widget.SetOrientationMarker(text_actor)
orientation_widget.On()

# Scene
small_view_renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
