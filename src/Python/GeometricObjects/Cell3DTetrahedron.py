#!/usr/bin/env python

# Render a tetrahedron — a 3D cell with four triangular faces,
# defined by 4 explicit point coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
    vtkCellArray,
    vtkTetra,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_blue_background_rgb = (0.2, 0.302, 0.4)

# Points: 4 vertices of a tetrahedron centered near the origin
points = vtkPoints()
points.InsertNextPoint(-0.5, -0.5, -0.5)
points.InsertNextPoint(0.5, -0.5, -0.5)
points.InsertNextPoint(0.5, 0.5, -0.5)
points.InsertNextPoint(-0.5, 0.5, 0.5)

# Cell: tetrahedron with 4 point IDs
tetrahedron = vtkTetra()
tetrahedron.GetPointIds().SetId(0, 0)
tetrahedron.GetPointIds().SetId(1, 1)
tetrahedron.GetPointIds().SetId(2, 2)
tetrahedron.GetPointIds().SetId(3, 3)

cells = vtkCellArray()
cells.InsertNextCell(tetrahedron)

# Unstructured grid: holds the single cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.SetCells(VTK_TETRA, cells)

# Mapper: map the grid to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(grid)

# Actor: position, orient, and color the cell
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.RotateX(20.0)
actor.RotateY(-20.0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_blue_background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Cell3DTetrahedron")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
