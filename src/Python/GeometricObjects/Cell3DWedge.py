#!/usr/bin/env python

# Render a wedge — a 3D cell with two triangular ends joined by three
# rectangular faces, defined by 6 explicit point coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkUnstructuredGrid,
    vtkWedge,
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

# Points: 6 vertices — two triangular faces
points = vtkPoints()
points.InsertNextPoint(-0.5, 0.5, -0.5)
points.InsertNextPoint(-0.5, -0.5, -0.5)
points.InsertNextPoint(-0.5, 0.0, 0.5)
points.InsertNextPoint(0.5, 0.5, -0.5)
points.InsertNextPoint(0.5, -0.5, -0.5)
points.InsertNextPoint(0.5, 0.0, 0.5)

# Cell: wedge with 6 point IDs
wedge = vtkWedge()
wedge.GetPointIds().SetId(0, 0)
wedge.GetPointIds().SetId(1, 1)
wedge.GetPointIds().SetId(2, 2)
wedge.GetPointIds().SetId(3, 3)
wedge.GetPointIds().SetId(4, 4)
wedge.GetPointIds().SetId(5, 5)

# Unstructured grid: holds the single cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(wedge.GetCellType(), wedge.GetPointIds())

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
render_window.SetWindowName("Cell3DWedge")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
