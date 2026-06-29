#!/usr/bin/env python
# Demonstrate vtkSphereWidget zoom in/out interaction.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import vtkSphereWidget
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("sphere widget zoom in out")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
sphere_widget = vtkSphereWidget()
sphere_widget.SetInteractor(interactor)
sphere_widget.SetPlaceFactor(1.25)
sphere_widget.PlaceWidget(-1, 1, -1, 1, -1, 1)
sphere_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
