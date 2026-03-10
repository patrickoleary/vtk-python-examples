#!/usr/bin/env python

# Extract the edges of a sphere as wireframe lines using
# vtkExtractEdges and display them as tubes alongside the solid mesh.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import (
    vtkExtractEdges,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_coral_rgb = (0.941, 0.502, 0.502)
white_rgb = (1.0, 1.0, 1.0)
background_rgb = (0.1, 0.1, 0.2)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(20)
sphere_source.SetPhiResolution(20)

# Filter: extract the edges from the sphere polygons
extract_edges = vtkExtractEdges()
extract_edges.SetInputConnection(sphere_source.GetOutputPort())

# Filter: wrap tubes around the extracted edges for visibility
tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(extract_edges.GetOutputPort())
tube_filter.SetRadius(0.005)
tube_filter.SetNumberOfSides(12)

# Mapper: map the tube edges to graphics primitives
edge_mapper = vtkPolyDataMapper()
edge_mapper.SetInputConnection(tube_filter.GetOutputPort())

# Actor: assign the edge tubes (white)
edge_actor = vtkActor()
edge_actor.SetMapper(edge_mapper)
edge_actor.GetProperty().SetColor(white_rgb)

# Mapper: map the original sphere surface
surface_mapper = vtkPolyDataMapper()
surface_mapper.SetInputConnection(sphere_source.GetOutputPort())

# Actor: assign the sphere surface (light coral, semi-transparent)
surface_actor = vtkActor()
surface_actor.SetMapper(surface_mapper)
surface_actor.GetProperty().SetColor(light_coral_rgb)
surface_actor.GetProperty().SetOpacity(0.4)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(surface_actor)
renderer.AddActor(edge_actor)
renderer.SetBackground(background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ExtractEdges")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
