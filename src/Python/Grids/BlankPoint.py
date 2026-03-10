#!/usr/bin/env python

# Create a structured grid and blank a point to hide it and its surrounding faces.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkStructuredGridGeometryFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
blue_rgb = (0.0, 0.0, 1.0)
forest_green_rgb = (0.133, 0.545, 0.133)

# Source: create an 8x8 structured grid with one elevated and blanked point
grid_size = 8
points = vtkPoints()
blank_idx = 0
for j in range(grid_size):
    for i in range(grid_size):
        if i == 3 and j == 3:
            points.InsertNextPoint(i, j, 2)
            blank_idx = j * grid_size + i
        else:
            points.InsertNextPoint(i, j, 0)

structured_grid = vtkStructuredGrid()
structured_grid.SetDimensions(grid_size, grid_size, 1)
structured_grid.SetPoints(points)
structured_grid.BlankPoint(blank_idx)

# GeometryFilter: extract surface geometry (blanked point and faces are removed)
geometry_filter = vtkStructuredGridGeometryFilter()
geometry_filter.SetInputData(structured_grid)

# Mapper: map the geometry to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputConnection(geometry_filter.GetOutputPort())

# Actor: assign the mapped geometry with visible edges
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().EdgeVisibilityOn()
actor.GetProperty().SetEdgeColor(blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(forest_green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("BlankPoint")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
