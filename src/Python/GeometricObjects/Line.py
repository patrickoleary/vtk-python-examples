#!/usr/bin/env python

# Render a line between two points using vtkLineSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkLineSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.2, 0.631, 0.788)
silver_background_rgb = (0.75, 0.75, 0.75)

# Source: generate a line between two points
line_source = vtkLineSource()
line_source.SetPoint1(1.0, 0.0, 0.0)
line_source.SetPoint2(0.0, 1.0, 0.0)

# Mapper: map line geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(line_source.GetOutputPort())

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetLineWidth(4)
actor.GetProperty().SetColor(peacock_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(silver_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Line")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
