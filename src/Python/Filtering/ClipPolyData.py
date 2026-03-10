#!/usr/bin/env python

# Clip a sphere with a plane using vtkClipPolyData and display both
# the clipped region and the remaining geometry side by side.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
background_rgb = (0.2, 0.2, 0.2)

# Source: generate a high-resolution sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(40)
sphere_source.SetPhiResolution(40)

# Clip function: a plane passing through the origin with X normal
clip_plane = vtkPlane()
clip_plane.SetOrigin(0, 0, 0)
clip_plane.SetNormal(1, 0, 0)

# Filter: clip the sphere — output is the portion where plane function < 0
clip_filter = vtkClipPolyData()
clip_filter.SetInputConnection(sphere_source.GetOutputPort())
clip_filter.SetClipFunction(clip_plane)
clip_filter.GenerateClippedOutputOn()

# Mapper: map the kept half (negative side)
kept_mapper = vtkPolyDataMapper()
kept_mapper.SetInputConnection(clip_filter.GetOutputPort())

# Actor: assign the kept half (tomato)
kept_actor = vtkActor()
kept_actor.SetMapper(kept_mapper)
kept_actor.GetProperty().SetColor(tomato_rgb)
kept_actor.GetProperty().EdgeVisibilityOn()

# Mapper: map the clipped-away half (positive side)
clipped_mapper = vtkPolyDataMapper()
clipped_mapper.SetInputConnection(clip_filter.GetClippedOutputPort())

# Actor: assign the clipped half (steel blue), offset along X
clipped_actor = vtkActor()
clipped_actor.SetMapper(clipped_mapper)
clipped_actor.GetProperty().SetColor(steel_blue_rgb)
clipped_actor.GetProperty().EdgeVisibilityOn()
clipped_actor.SetPosition(2, 0, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(kept_actor)
renderer.AddActor(clipped_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ClipPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
