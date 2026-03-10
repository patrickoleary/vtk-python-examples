#!/usr/bin/env python

# Render a cone using vtkConeSource.

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
salmon_background_rgb = (0.980, 0.502, 0.447)

# Source: generate a cone
# Uncomment to increase resolution or reposition the cone.
cone_source = vtkConeSource()
# cone_source.SetResolution(60)
# cone_source.SetCenter(-2, 0, 0)

# Mapper: map cone geometry to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cone_source.GetOutputPort())

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetDiffuseColor(bisque_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(salmon_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Cone")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
