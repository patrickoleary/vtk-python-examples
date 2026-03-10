#!/usr/bin/env python

# Extract and highlight boundary edges of a disk using vtkFeatureEdges.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkFeatureEdges
from vtkmodules.vtkFiltersSources import vtkDiskSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
slate_gray_background_rgb = (0.439, 0.502, 0.565)
light_gray_rgb = (0.800, 0.800, 0.800)

# Source: generate a disk with a hole in the center
disk = vtkDiskSource()

# FeatureEdges: extract only boundary edges (inner and outer rings)
feature_edges = vtkFeatureEdges()
feature_edges.SetInputConnection(disk.GetOutputPort())
feature_edges.BoundaryEdgesOn()
feature_edges.FeatureEdgesOff()
feature_edges.ManifoldEdgesOff()
feature_edges.NonManifoldEdgesOff()
feature_edges.ColoringOn()

# Mapper: map boundary edges to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(feature_edges.GetOutputPort())

# Actor: boundary edges (colored by vtkFeatureEdges)
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)

# Mapper: map the full disk surface
disk_mapper = vtkPolyDataMapper()
disk_mapper.SetInputConnection(disk.GetOutputPort())
disk_mapper.ScalarVisibilityOff()

# Actor: the disk surface in light grey
disk_actor = vtkActor()
disk_actor.SetMapper(disk_mapper)
disk_actor.GetProperty().SetColor(light_gray_rgb)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(edge_actor)
renderer.AddActor(disk_actor)
renderer.SetBackground(slate_gray_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("BoundaryEdges")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
