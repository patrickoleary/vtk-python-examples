#!/usr/bin/env python

# Display balloon popups when hovering over actors.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkRegularPolygonSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkBalloonRepresentation,
    vtkBalloonWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
misty_rose_rgb = (1.0, 0.894, 0.882)
cornsilk_rgb = (1.0, 0.973, 0.863)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetCenter(-4.0, 0.0, 0.0)
sphere_source.SetRadius(4.0)

# Mapper: map sphere polygon data to graphics primitives
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the sphere geometry
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(misty_rose_rgb)

# Source: generate a regular polygon
polygon_source = vtkRegularPolygonSource()
polygon_source.SetCenter(4.0, 0.0, 0.0)
polygon_source.SetRadius(4.0)

# Mapper: map polygon data to graphics primitives
polygon_mapper = vtkPolyDataMapper()
polygon_mapper.SetInputConnection(polygon_source.GetOutputPort())

# Actor: assign the polygon geometry
polygon_actor = vtkActor()
polygon_actor.SetMapper(polygon_mapper)
polygon_actor.GetProperty().SetColor(cornsilk_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(polygon_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("BalloonWidget")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# BalloonWidget: show tooltips when hovering over actors
balloon_rep = vtkBalloonRepresentation()
balloon_rep.SetBalloonLayoutToImageRight()

balloon_widget = vtkBalloonWidget()
balloon_widget.SetInteractor(render_window_interactor)
balloon_widget.SetRepresentation(balloon_rep)
balloon_widget.AddBalloon(sphere_actor, "This is a sphere")
balloon_widget.AddBalloon(polygon_actor, "This is a regular polygon")

# Launch the interactive visualization
render_window.Render()
balloon_widget.EnabledOn()
render_window_interactor.Initialize()
render_window_interactor.Start()
