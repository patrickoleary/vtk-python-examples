#!/usr/bin/env python
# Demonstrate vtkLightWidget with two light widgets showing positional and default configurations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkLightRepresentation,
    vtkLightWidget,
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
render_window.SetWindowName("light widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

# Widget: first light widget (positional light)
light_rep = vtkLightRepresentation()
light_rep.SetPositional(True)

light_widget = vtkLightWidget()
light_widget.SetInteractor(interactor)
light_widget.SetRepresentation(light_rep)
light_widget.On()

# Widget: second light widget (yellow light, default settings)
light_rep_2 = vtkLightRepresentation()
light_rep_2.SetLightColor([1.0, 1.0, 0.0])

light_widget_2 = vtkLightWidget()
light_widget_2.SetInteractor(interactor)
light_widget_2.SetRepresentation(light_rep_2)
light_widget_2.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
