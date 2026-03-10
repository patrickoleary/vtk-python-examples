#!/usr/bin/env python

# Basic rendering and pipeline creation with a cylinder.

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
tomato_rgb = (1.0, 0.388, 0.278)
dark_blue_background_rgb = (0.102, 0.2, 0.4)

# Source: generate cylinder polygon data
cylinder_source = vtkCylinderSource()
cylinder_source.SetResolution(8)

# Mapper: map polygon data to graphics primitives
poly_data_mapper = vtkPolyDataMapper()
poly_data_mapper.SetInputConnection(cylinder_source.GetOutputPort())

# Actor: position, orient, and color the mapped geometry
actor = vtkActor()
actor.SetMapper(poly_data_mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.RotateX(30.0)
actor.RotateY(-45.0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_blue_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("CylinderExample")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
