#!/usr/bin/env python

# Render a hexagonal prism — a prism with two hexagonal faces and six
# rectangular sides, defined by 12 explicit point coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering,
# FreeType text rendering, and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkHexagonalPrism,
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

# Points: 12 vertices — top hexagonal face then bottom hexagonal face
points = vtkPoints()
points.InsertNextPoint(-0.35, -0.35, 0.35)
points.InsertNextPoint(0.35, -0.35, 0.35)
points.InsertNextPoint(0.7, 0.0, 0.35)
points.InsertNextPoint(0.35, 0.35, 0.35)
points.InsertNextPoint(-0.35, 0.35, 0.35)
points.InsertNextPoint(-0.7, 0.0, 0.35)
points.InsertNextPoint(-0.35, -0.35, -0.35)
points.InsertNextPoint(0.35, -0.35, -0.35)
points.InsertNextPoint(0.7, 0.0, -0.35)
points.InsertNextPoint(0.35, 0.35, -0.35)
points.InsertNextPoint(-0.35, 0.35, -0.35)
points.InsertNextPoint(-0.7, 0.0, -0.35)

# Cell: hexagonal prism with 12 point IDs
hexagonal_prism = vtkHexagonalPrism()
hexagonal_prism.GetPointIds().SetId(0, 0)
hexagonal_prism.GetPointIds().SetId(1, 1)
hexagonal_prism.GetPointIds().SetId(2, 2)
hexagonal_prism.GetPointIds().SetId(3, 3)
hexagonal_prism.GetPointIds().SetId(4, 4)
hexagonal_prism.GetPointIds().SetId(5, 5)
hexagonal_prism.GetPointIds().SetId(6, 6)
hexagonal_prism.GetPointIds().SetId(7, 7)
hexagonal_prism.GetPointIds().SetId(8, 8)
hexagonal_prism.GetPointIds().SetId(9, 9)
hexagonal_prism.GetPointIds().SetId(10, 10)
hexagonal_prism.GetPointIds().SetId(11, 11)

# Unstructured grid: holds the single cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(hexagonal_prism.GetCellType(), hexagonal_prism.GetPointIds())

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
render_window.SetWindowName("Cell3DHexagonalPrism")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
