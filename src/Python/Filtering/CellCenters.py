#!/usr/bin/env python

# Demonstrate vtkCellCenters to generate points at cell centers of a mesh,
# then display small sphere glyphs at those locations.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkCellCenters
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkGlyph3DMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (0.980, 0.502, 0.447)
steel_blue_rgb = (0.275, 0.510, 0.706)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: low-resolution sphere so cell centers are visible
sphere = vtkSphereSource()
sphere.SetPhiResolution(12)
sphere.SetThetaResolution(12)

# Filter: compute cell centers
centers = vtkCellCenters()
centers.SetInputConnection(sphere.GetOutputPort())

# Source: small sphere glyph shape
glyph_source = vtkSphereSource()
glyph_source.SetRadius(0.03)
glyph_source.SetPhiResolution(8)
glyph_source.SetThetaResolution(8)

# Mapper: place sphere glyphs at each cell center
glyph_mapper = vtkGlyph3DMapper()
glyph_mapper.SetInputConnection(centers.GetOutputPort())
glyph_mapper.SetSourceConnection(glyph_source.GetOutputPort())
glyph_mapper.ScalingOff()

# Actor: assign the glyph geometry
glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetColor(tomato_rgb)

# Mapper: map the wireframe mesh to graphics primitives
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: wireframe mesh for context
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetRepresentationToWireframe()
mesh_actor.GetProperty().SetColor(steel_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(mesh_actor)
renderer.AddActor(glyph_actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CellCenters")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
