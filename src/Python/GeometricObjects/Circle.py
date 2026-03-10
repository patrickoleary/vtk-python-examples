#!/usr/bin/env python

# Draw a circle using a regular polygon source with many sides.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornsilk_rgb = (1.0, 0.973, 0.863)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Source: generate a circle as a regular polygon with 50 sides
# Comment out GeneratePolygonOff() to generate a filled disk instead.
polygon_source = vtkRegularPolygonSource()
polygon_source.GeneratePolygonOff()
polygon_source.SetNumberOfSides(50)
polygon_source.SetRadius(5.0)
polygon_source.SetCenter(0.0, 0.0, 0.0)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(polygon_source.GetOutputPort())

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(cornsilk_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Circle")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
