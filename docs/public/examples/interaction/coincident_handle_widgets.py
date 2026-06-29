#!/usr/bin/env python
# Test coincident handle widgets with picking manager enabled.

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

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("coincident handle widgets")
render_window.SetMultiSamples(0)
render_window.SetSize(301, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.GetPickingManager().EnabledOn()

# Widget
handle_rep = vtkPointHandleRepresentation3D()
handle_rep.GetProperty().SetColor(1, 0, 0)
handle_rep.GetProperty().SetLineWidth(2)
handle_rep.GetSelectedProperty().SetColor(1, 1, 0)
handle_rep.GetSelectedProperty().SetLineWidth(4)

seed_rep = vtkSeedRepresentation()
seed_rep.SetHandleRepresentation(handle_rep)

seed_widget = vtkSeedWidget()
seed_widget.SetRepresentation(seed_rep)
seed_widget.CompleteInteraction()
seed_widget.RestartInteraction()
seed_widget.SetInteractor(interactor)
seed_widget.On()

render_window.Render()

# Create first handle (visible and enabled)
handle_widget_1 = seed_widget.CreateNewHandle()
handle_widget_1.EnabledOn()
handle_rep_1 = seed_rep.GetHandleRepresentation(0)
coords = [150, 150, 0]
seed_rep.SetSeedDisplayPosition(0, coords)
handle_rep_1.VisibilityOn()
seed_widget.GetSeed(0).EnabledOn()

# Create second handle (invisible and disabled, at same position)
handle_widget_2 = seed_widget.CreateNewHandle()
handle_widget_2.EnabledOff()
handle_rep_2 = seed_rep.GetHandleRepresentation(1)
seed_rep.SetSeedDisplayPosition(1, coords)
handle_rep_2.VisibilityOff()
seed_widget.GetSeed(1).EnabledOff()

seed_widget.CompleteInteraction()

interactor.Initialize()
interactor.Start()
