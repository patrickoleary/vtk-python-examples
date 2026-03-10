#!/usr/bin/env python

# Generate random terrain points on an XY grid, triangulate with
# vtkDelaunay2D, and display both the points and the triangulated mesh.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
red_rgb = (1.0, 0.0, 0.0)
green_rgb = (0.0, 0.5, 0.0)

# Points: create a 10x10 grid with random Z heights
points = vtkPoints()
grid_size = 10
random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.Initialize(0)
for x in range(grid_size):
    for y in range(grid_size):
        d = random_sequence.GetValue()
        random_sequence.Next()
        points.InsertNextPoint(x, y, d * 3)

polydata = vtkPolyData()
polydata.SetPoints(points)

# Filter: convert points to vertex glyphs for rendering
glyph_filter = vtkVertexGlyphFilter()
glyph_filter.SetInputData(polydata)

# Mapper: map vertex glyphs to graphics primitives
points_mapper = vtkPolyDataMapper()
points_mapper.SetInputConnection(glyph_filter.GetOutputPort())

# Actor: assign the point glyphs (red)
points_actor = vtkActor()
points_actor.SetMapper(points_mapper)
points_actor.GetProperty().SetPointSize(3)
points_actor.GetProperty().SetColor(red_rgb)

# Filter: Delaunay 2D triangulation of the grid points
delaunay = vtkDelaunay2D()
delaunay.SetInputData(polydata)

# Mapper: map the triangulated mesh to graphics primitives
triangulated_mapper = vtkPolyDataMapper()
triangulated_mapper.SetInputConnection(delaunay.GetOutputPort())

# Actor: assign the triangulated mesh
triangulated_actor = vtkActor()
triangulated_actor.SetMapper(triangulated_mapper)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(points_actor)
renderer.AddActor(triangulated_actor)
renderer.SetBackground(green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TriangulateTerrainMap")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
