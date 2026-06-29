#!/usr/bin/env python
# Demonstrate vtkTensorWidget and vtkTensorRepresentation with default placement.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkInteractionWidgets import (
    vtkTensorRepresentation,
    vtkTensorWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("tensor widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback for widget interaction
def select_polygons(widget, event_string):
    pass


# Widget
bounds = [-1, 1, -1, 1, -1, 1]
tensor_rep = vtkTensorRepresentation()
tensor_rep.GetEllipsoidProperty().SetColor(0, 0, 0)
tensor_rep.GetEllipsoidProperty().SetRepresentationToWireframe()
tensor_rep.GetOutlineProperty().SetColor(0, 0, 0)
tensor_rep.SetPlaceFactor(1)
tensor_rep.PlaceWidget(bounds)

tensor_widget = vtkTensorWidget()
tensor_widget.SetInteractor(interactor)
tensor_widget.SetRepresentation(tensor_rep)
tensor_widget.AddObserver("EndInteractionEvent", select_polygons)
tensor_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
