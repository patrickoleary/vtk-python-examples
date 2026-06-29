#!/usr/bin/env python
# Demonstrate laying out widgets in multiple viewports.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkInteractionWidgets import (
    vtkBorderRepresentation,
    vtkBorderWidget,
    vtkHandleWidget,
    vtkPointHandleRepresentation2D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
plane = vtkPlaneSource()

# Mapper + Actor
plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(plane.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderer (two viewports)
renderer_0 = vtkRenderer()
renderer_0.SetBackground(0, 0, 0)
renderer_0.SetViewport(0, 0, 0.5, 1)

renderer_1 = vtkRenderer()
renderer_1.SetBackground(0.1, 0.1, 0.1)
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(plane_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("multiple viewports")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 150)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget: border widget in first viewport
border_rep = vtkBorderRepresentation()
border_rep.GetPositionCoordinate().SetValue(0.1, 0.5)
border_rep.GetPosition2Coordinate().SetValue(0.4, 0.1)
border_rep.SetShowBorderToOn()

border_widget = vtkBorderWidget()
border_widget.SetInteractor(interactor)
border_widget.SetCurrentRenderer(renderer_0)
border_widget.SetRepresentation(border_rep)
border_widget.On()

# Widget: handle widget in second viewport
handle_rep = vtkPointHandleRepresentation2D()
handle_rep.SetWorldPosition(plane.GetOrigin())

handle_widget = vtkHandleWidget()
handle_widget.SetCurrentRenderer(renderer_1)
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(handle_rep)
handle_widget.On()

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
