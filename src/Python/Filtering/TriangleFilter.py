#!/usr/bin/env python

# Triangulate a cylinder (which has quad and polygon faces) using
# vtkTriangleFilter and display the original and triangulated meshes.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_salmon_rgb = (1.0, 0.627, 0.478)
sky_blue_rgb = (0.529, 0.808, 0.922)
background_rgb = (0.2, 0.2, 0.2)

# Source: generate a cylinder with quad faces and polygon caps
cylinder_source = vtkCylinderSource()
cylinder_source.SetResolution(20)

# Mapper: map the original cylinder (has quads + polygons)
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(cylinder_source.GetOutputPort())

# Actor: assign the original cylinder (light salmon), offset left
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(light_salmon_rgb)
original_actor.GetProperty().EdgeVisibilityOn()
original_actor.SetPosition(-1.5, 0, 0)

# Filter: convert all polygons to triangles
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(cylinder_source.GetOutputPort())

# Mapper: map the triangulated cylinder
triangulated_mapper = vtkPolyDataMapper()
triangulated_mapper.SetInputConnection(triangle_filter.GetOutputPort())

# Actor: assign the triangulated cylinder (sky blue), offset right
triangulated_actor = vtkActor()
triangulated_actor.SetMapper(triangulated_mapper)
triangulated_actor.GetProperty().SetColor(sky_blue_rgb)
triangulated_actor.GetProperty().EdgeVisibilityOn()
triangulated_actor.SetPosition(1.5, 0, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(triangulated_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TriangleFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
