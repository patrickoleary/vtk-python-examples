#!/usr/bin/env python

# Render a sphere with axes actor offset by a transform.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: generate sphere polygon data
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetRadius(0.5)

# Mapper: map polygon data to graphics primitives
poly_data_mapper = vtkPolyDataMapper()
poly_data_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the mapped geometry
sphere_actor = vtkActor()
sphere_actor.SetMapper(poly_data_mapper)

# Axes: position with a user transform offset along the x-axis
transform = vtkTransform()
transform.Translate(1.0, 0.0, 0.0)

axes_actor = vtkAxesActor()
axes_actor.SetUserTransform(transform)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(axes_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.GetActiveCamera().Azimuth(50)
renderer.GetActiveCamera().Elevation(-30)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Axes")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
