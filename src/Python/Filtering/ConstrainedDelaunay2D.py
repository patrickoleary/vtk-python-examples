#!/usr/bin/env python

# Generate a jittered 10x10 grid, define a polygonal hole boundary,
# and triangulate with vtkDelaunay2D constrained by that boundary.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import (
    vtkMinimalStandardRandomSequence,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolygon,
)
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peacock_rgb = (0.2, 0.631, 0.788)
raspberry_rgb = (0.529, 0.149, 0.341)
red_rgb = (1.0, 0.0, 0.0)
mint_rgb = (0.741, 0.988, 0.788)

# Points: generate a 10x10 grid with random jitter
points = vtkPoints()
grid_size = 10
random_sequence = vtkMinimalStandardRandomSequence()
random_sequence.Initialize(0)
for x in range(grid_size):
    for y in range(grid_size):
        d1 = random_sequence.GetValue() / 2.0 - 0.25
        random_sequence.Next()
        d2 = random_sequence.GetValue() / 2.0 - 0.25
        random_sequence.Next()
        points.InsertNextPoint(x + d1, y + d2, 0)

point_polydata = vtkPolyData()
point_polydata.SetPoints(points)

# Boundary: define a polygonal hole constraint (clockwise winding)
polygon = vtkPolygon()
for pid in [22, 23, 24, 25, 35, 45, 44, 43, 42, 32]:
    polygon.GetPointIds().InsertNextId(pid)

cell_array = vtkCellArray()
cell_array.InsertNextCell(polygon)

boundary = vtkPolyData()
boundary.SetPoints(point_polydata.GetPoints())
boundary.SetPolys(cell_array)

# Filter: constrained Delaunay 2D triangulation with the boundary hole
delaunay = vtkDelaunay2D()
delaunay.SetInputData(point_polydata)
delaunay.SetSourceData(boundary)

# Mapper: map the triangulated mesh to graphics primitives
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(delaunay.GetOutputPort())

# Actor: assign the mesh with visible edges
mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().EdgeVisibilityOn()
mesh_actor.GetProperty().SetEdgeColor(peacock_rgb)
mesh_actor.GetProperty().SetInterpolationToFlat()

# Mapper: map the boundary polygon as wireframe
boundary_mapper = vtkPolyDataMapper()
boundary_mapper.SetInputData(boundary)

# Actor: assign the boundary wireframe
boundary_actor = vtkActor()
boundary_actor.SetMapper(boundary_mapper)
boundary_actor.GetProperty().SetColor(raspberry_rgb)
boundary_actor.GetProperty().SetLineWidth(3)
boundary_actor.GetProperty().EdgeVisibilityOn()
boundary_actor.GetProperty().SetEdgeColor(red_rgb)
boundary_actor.GetProperty().SetRepresentationToWireframe()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(mesh_actor)
renderer.AddActor(boundary_actor)
renderer.SetBackground(mint_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ConstrainedDelaunay2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
