#!/usr/bin/env python
# Demonstrate vtkPolyLineWidget for creating and manipulating polylines.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkInteractionWidgets import (
    vtkPolyLineRepresentation,
    vtkPolyLineWidget,
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
render_window.SetWindowName("polyline widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
points = vtkPoints()
points.InsertNextPoint(0.25, 0.5, 0.0)
points.InsertNextPoint(0.75, 0.5, 0.0)

polyline_rep = vtkPolyLineRepresentation()
polyline_rep.InitializeHandles(points)

polyline_widget = vtkPolyLineWidget()
polyline_widget.SetInteractor(interactor)
polyline_widget.SetRepresentation(polyline_rep)
polyline_widget.On()

# Scene
renderer.ResetCamera(0.0, 1.0, 0.0, 1.0, 0.0, 0.0)

interactor.Initialize()
interactor.Start()
