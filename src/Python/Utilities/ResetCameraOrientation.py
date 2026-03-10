#!/usr/bin/env python

# Save, change, and restore camera orientation programmatically.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bisque_rgb = (1.0, 0.894, 0.769)
midnight_blue_rgb = (0.098, 0.098, 0.439)

# Source: a cone
cone = vtkConeSource()
cone.SetHeight(3.0)
cone.SetRadius(1.0)
cone.SetResolution(10)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(bisque_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(midnight_blue_rgb)

# Camera: set an initial orientation
camera = renderer.GetActiveCamera()
camera.SetRoll(15)
camera.Elevation(-15)
camera.Azimuth(30)
renderer.ResetCamera()

# Save the original camera parameters
original_position = camera.GetPosition()
original_focal_point = camera.GetFocalPoint()
original_view_up = camera.GetViewUp()
original_distance = camera.GetDistance()
original_clipping_range = camera.GetClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ResetCameraOrientation")
render_window.Render()

# Change the camera to a different orientation
camera.SetPosition(-3.568, 5.220, 2.353)
camera.SetFocalPoint(-0.399, -0.283, 0.131)
camera.SetViewUp(0.623, 0.574, -0.531)
camera.SetDistance(6.728)
camera.SetClippingRange(3.001, 11.434)
render_window.Render()

# Restore the original camera orientation
camera.SetPosition(original_position)
camera.SetFocalPoint(original_focal_point)
camera.SetViewUp(original_view_up)
camera.SetDistance(original_distance)
camera.SetClippingRange(original_clipping_range)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
