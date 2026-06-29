#!/usr/bin/env python

# Demonstrate vtkOutlineCornerFilter to draw corner-only bounding box
# brackets around a sphere.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkOutlineCornerFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
white_rgb = (1.0, 1.0, 1.0)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: sphere
sphere_source = vtkSphereSource()
sphere_source.SetPhiResolution(32)
sphere_source.SetThetaResolution(32)

# Filter: corner-only outline
outline_filter = vtkOutlineCornerFilter()
outline_filter.SetInputConnection(sphere_source.GetOutputPort())
outline_filter.SetCornerFactor(0.3)

# Mapper: map the sphere to graphics primitives
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the sphere geometry
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(cornflower_blue_rgb)

# Mapper: map the outline to graphics primitives
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())

# Actor: assign the outline geometry
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(white_rgb)
outline_actor.GetProperty().SetLineWidth(3)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(slate_gray_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("outline corner")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
