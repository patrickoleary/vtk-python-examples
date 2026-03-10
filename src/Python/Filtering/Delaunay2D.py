#!/usr/bin/env python

# Create a terrain-like height field on a 10x10 grid and triangulate
# it with vtkDelaunay2D, displaying both the mesh and the input points.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
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
light_goldenrod_rgb = (0.980, 0.980, 0.824)
cornflower_blue_rgb = (0.392, 0.584, 0.929)
deep_pink_rgb = (1.0, 0.078, 0.576)
powder_blue_rgb = (0.690, 0.878, 0.902)

# Points: create a 10x10 grid with a terrain-like height field
points = vtkPoints()
grid_size = 10
for x in range(grid_size):
    for y in range(grid_size):
        points.InsertNextPoint(x, y, int((x + y) / (y + 1)))

polydata = vtkPolyData()
polydata.SetPoints(points)

# Filter: Delaunay 2D triangulation of the grid points
delaunay = vtkDelaunay2D()
delaunay.SetInputData(polydata)

# Mapper: map the triangulated mesh to graphics primitives
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(delaunay.GetOutputPort())

# Actor: assign the mesh with visible tube-style edges
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(light_goldenrod_rgb)
mesh_actor.GetProperty().EdgeVisibilityOn()
mesh_actor.GetProperty().SetEdgeColor(cornflower_blue_rgb)
mesh_actor.GetProperty().SetLineWidth(3)
mesh_actor.GetProperty().RenderLinesAsTubesOn()

# Filter: convert points to vertex glyphs for rendering
glyph_filter = vtkVertexGlyphFilter()
glyph_filter.SetInputData(polydata)

# Mapper: map vertex glyphs to graphics primitives
point_mapper = vtkPolyDataMapper()
point_mapper.SetInputConnection(glyph_filter.GetOutputPort())

# Actor: assign the point glyphs as spheres
point_actor = vtkActor()
point_actor.SetMapper(point_mapper)
point_actor.GetProperty().SetColor(deep_pink_rgb)
point_actor.GetProperty().SetPointSize(10)
point_actor.GetProperty().RenderPointsAsSpheresOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(mesh_actor)
renderer.AddActor(point_actor)
renderer.SetBackground(powder_blue_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Delaunay2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
