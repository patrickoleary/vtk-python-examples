#!/usr/bin/env python
# Demonstrate vtkSphereWidget2 with center cursor visibility.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import vtkSphereWidget2
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
render_window.SetWindowName("sphere widget center cursor")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget 1 (no center cursor)
sphere_widget_1 = vtkSphereWidget2()
sphere_widget_1.SetInteractor(interactor)
sphere_widget_1.CreateDefaultRepresentation()

sphere_rep_1 = sphere_widget_1.GetRepresentation()
sphere_rep_1.HandleVisibilityOff()
sphere_rep_1.SetCenter(4, 0, 0)
sphere_rep_1.SetRadius(3)

sphere_widget_1.On()

# Widget 2 (with center cursor)
sphere_widget_2 = vtkSphereWidget2()
sphere_widget_2.SetInteractor(interactor)
sphere_widget_2.CreateDefaultRepresentation()

sphere_rep_2 = sphere_widget_2.GetRepresentation()
sphere_rep_2.HandleVisibilityOff()
sphere_rep_2.SetCenter(-4, 0, 0)
sphere_rep_2.SetRadius(3)
sphere_rep_2.SetCenterCursor(True)

sphere_widget_2.On()

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0.0, 0.0, 20.0)
camera.SetFocalPoint(0.0, 0.0, -1)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
