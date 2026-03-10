#!/usr/bin/env python

# Use a box widget to interactively transform a cone actor.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkInteractionWidgets import vtkBoxWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
burlywood_rgb = (0.871, 0.722, 0.529)
blue_rgb = (0.0, 0.0, 1.0)

# Source: generate a cone
cone = vtkConeSource()
cone.SetResolution(20)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(burlywood_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("BoxWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# BoxWidget: interactive 3-D box for transforming the actor
box_widget = vtkBoxWidget()
box_widget.SetInteractor(render_window_interactor)
box_widget.SetProp3D(actor)
box_widget.SetPlaceFactor(1.25)
box_widget.PlaceWidget()
box_widget.On()

box_widget.AddObserver("InteractionEvent",
                       lambda obj, event: (
                           obj.GetTransform(t := vtkTransform()),
                           obj.GetProp3D().SetUserTransform(t),
                       ))

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window.Render()
render_window_interactor.Start()
