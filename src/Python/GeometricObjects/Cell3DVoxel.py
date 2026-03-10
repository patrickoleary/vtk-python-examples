#!/usr/bin/env python

# Render a voxel — an axis-aligned hexahedron on a regular grid,
# defined by 8 explicit point coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
    vtkVoxel,
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

# Points: 8 vertices of a unit voxel centered at the origin
# Voxel point ordering: (i,j,k) with i varying fastest
points = vtkPoints()
points.InsertNextPoint(-0.5, -0.5, -0.5)
points.InsertNextPoint(0.5, -0.5, -0.5)
points.InsertNextPoint(-0.5, 0.5, -0.5)
points.InsertNextPoint(0.5, 0.5, -0.5)
points.InsertNextPoint(-0.5, -0.5, 0.5)
points.InsertNextPoint(0.5, -0.5, 0.5)
points.InsertNextPoint(-0.5, 0.5, 0.5)
points.InsertNextPoint(0.5, 0.5, 0.5)

# Cell: voxel with 8 point IDs
voxel = vtkVoxel()
voxel.GetPointIds().SetId(0, 0)
voxel.GetPointIds().SetId(1, 1)
voxel.GetPointIds().SetId(2, 2)
voxel.GetPointIds().SetId(3, 3)
voxel.GetPointIds().SetId(4, 4)
voxel.GetPointIds().SetId(5, 5)
voxel.GetPointIds().SetId(6, 6)
voxel.GetPointIds().SetId(7, 7)

# Unstructured grid: holds the single cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(voxel.GetCellType(), voxel.GetPointIds())

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
render_window.SetWindowName("Cell3DVoxel")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
