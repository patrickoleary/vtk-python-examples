#!/usr/bin/env python

# Render a high-resolution cylinder using vtkCylinderSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkCylinderSource
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

# Source: generate a cylinder
cylinder_source = vtkCylinderSource()
cylinder_source.SetCenter(0.0, 0.0, 0.0)
cylinder_source.SetRadius(5.0)
cylinder_source.SetHeight(7.0)
cylinder_source.SetResolution(100)

# Mapper: map cylinder geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cylinder_source.GetOutputPort())

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
render_window.SetWindowName("Cylinder")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
