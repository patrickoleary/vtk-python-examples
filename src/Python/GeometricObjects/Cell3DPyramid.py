#!/usr/bin/env python

# Render a pyramid — a 3D cell with a square base tapering to an apex,
# defined by 5 explicit point coordinates.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkPyramid,
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

# Points: 4 base vertices and 1 apex
points = vtkPoints()
points.InsertNextPoint(0.5, 0.5, -0.5)
points.InsertNextPoint(-0.5, 0.5, -0.5)
points.InsertNextPoint(-0.5, -0.5, -0.5)
points.InsertNextPoint(0.5, -0.5, -0.5)
points.InsertNextPoint(0.0, 0.0, 0.5)

# Cell: pyramid with 5 point IDs
pyramid = vtkPyramid()
pyramid.GetPointIds().SetId(0, 0)
pyramid.GetPointIds().SetId(1, 1)
pyramid.GetPointIds().SetId(2, 2)
pyramid.GetPointIds().SetId(3, 3)
pyramid.GetPointIds().SetId(4, 4)

# Unstructured grid: holds the single cell
grid = vtkUnstructuredGrid()
grid.SetPoints(points)
grid.InsertNextCell(pyramid.GetCellType(), pyramid.GetPointIds())

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
render_window.SetWindowName("Cell3DPyramid")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
