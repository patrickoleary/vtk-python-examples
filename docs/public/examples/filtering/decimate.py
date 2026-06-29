#!/usr/bin/env python

# Reduce the polygon count of a sphere using vtkDecimatePro and display
# the original and decimated meshes side by side with visible edges.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkDecimatePro
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
bisque_rgb = (1.0, 0.894, 0.769)
cornflower_rgb = (0.392, 0.584, 0.929)
background_rgb = (0.2, 0.2, 0.2)

# Source: generate a high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(40)
sphere_source.SetPhiResolution(40)

# Mapper: map the original sphere
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the original sphere (bisque), offset left
original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(bisque_rgb)
original_actor.GetProperty().EdgeVisibilityOn()
original_actor.SetPosition(-1.2, 0, 0)

# Filter: decimate the sphere by 80%
decimate_filter = vtkDecimatePro()
decimate_filter.SetInputConnection(sphere_source.GetOutputPort())
decimate_filter.SetTargetReduction(0.8)
decimate_filter.PreserveTopologyOn()

# Mapper: map the decimated sphere
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimate_filter.GetOutputPort())

# Actor: assign the decimated sphere (cornflower blue), offset right
decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetColor(cornflower_rgb)
decimated_actor.GetProperty().EdgeVisibilityOn()
decimated_actor.SetPosition(1.2, 0, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(original_actor)
renderer.AddActor(decimated_actor)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("decimate")
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
