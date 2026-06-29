#!/usr/bin/env python
# Demonstrate vtkPointHandleRepresentation3D PlaceWidget with translation mode changes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import (
    vtkPointHandleRepresentation3D,
    vtkSeedRepresentation,
    vtkSeedWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("point handle representation3d")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
handle_rep = vtkPointHandleRepresentation3D()
handle_rep.AllOn()
handle_rep.GetProperty().SetColor(1.0, 0.0, 1.0)

seed_rep = vtkSeedRepresentation()
seed_rep.SetHandleRepresentation(handle_rep)

seed_widget = vtkSeedWidget()
seed_widget.SetRepresentation(seed_rep)
seed_widget.SetInteractor(interactor)
seed_widget.On()
seed_widget.ProcessEventsOff()

# Place two handles with different translation modes
bounds_1 = [0, 0.05, 0, 0.05, 0, 0.05]
bounds_2 = [-0.05, 0, -0.05, 0, -0.05, 0]

# First handle: default translation mode
handle_1 = seed_widget.CreateNewHandle()
handle_1.SetEnabled(1)
rep_1 = handle_1.GetRepresentation()
rep_1.PlaceWidget(bounds_1)

# Second handle: translation mode off
handle_2 = seed_widget.CreateNewHandle()
handle_2.SetEnabled(1)
rep_2 = handle_2.GetRepresentation()
rep_2.TranslationModeOff()
rep_2.PlaceWidget(bounds_2)

interactor.Initialize()
interactor.Start()
