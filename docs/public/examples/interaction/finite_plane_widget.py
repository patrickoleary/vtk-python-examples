#!/usr/bin/env python
# Demonstrate vtkFinitePlaneWidget with two plane widgets showing different configurations.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkFinitePlaneRepresentation,
    vtkFinitePlaneWidget,
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
render_window.SetWindowName("finite plane widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_trackball_camera = vtkInteractorStyleTrackballCamera()
interactor.SetInteractorStyle(interactor_style_trackball_camera)

# Widget 0: tubing, plane drawn, handles visible
plane_rep_0 = vtkFinitePlaneRepresentation()
plane_rep_0.SetTubing(True)
plane_rep_0.SetDrawPlane(True)
plane_rep_0.SetHandles(True)
plane_rep_0.PlaceWidget([0, 1, 0, 1, 0, 1])

finite_plane_widget_0 = vtkFinitePlaneWidget()
finite_plane_widget_0.SetInteractor(interactor)
finite_plane_widget_0.SetRepresentation(plane_rep_0)
finite_plane_widget_0.On()

# Widget 1: no tubing, no plane, no handles, non-rectangular
plane_rep_1 = vtkFinitePlaneRepresentation()
plane_rep_1.SetTubing(False)
plane_rep_1.SetDrawPlane(False)
plane_rep_1.SetHandles(False)
plane_rep_1.SetRectangularShape(False)
plane_rep_1.PlaceWidget([1.2, 2.2, 0, 1, 0, 1])

finite_plane_widget_1 = vtkFinitePlaneWidget()
finite_plane_widget_1.SetInteractor(interactor)
finite_plane_widget_1.SetRepresentation(plane_rep_1)
finite_plane_widget_1.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
