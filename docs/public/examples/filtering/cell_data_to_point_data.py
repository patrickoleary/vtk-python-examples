#!/usr/bin/env python

# Convert cell scalars to point scalars on a small structured grid.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkStructuredGrid
from vtkmodules.vtkFiltersCore import vtkCellDataToPointData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a 2x2 cell / 3x3 point structured grid
points = vtkPoints()
for pt in [(-1, 1, 0), (0, 1, 0), (1, 1, 0),
           (-1, 0, 0), (0, 0, 0), (1, 0, 0),
           (-1, -1, 0), (0, -1, 0), (1, -1, 0)]:
    points.InsertNextPoint(pt)

# Assign scalar values to each of the 4 cells
face_colors = vtkFloatArray()
for val in (0, 1, 1, 2):
    face_colors.InsertNextValue(val)

structured_grid = vtkStructuredGrid()
structured_grid.SetDimensions(3, 3, 1)
structured_grid.SetPoints(points)
structured_grid.GetCellData().SetScalars(face_colors)

# Filter: convert cell data to point data
cell_to_point = vtkCellDataToPointData()
cell_to_point.SetInputData(structured_grid)
cell_to_point.PassCellDataOn()

# Mapper: color by interpolated point scalars
mapper = vtkDataSetMapper()
mapper.SetInputConnection(cell_to_point.GetOutputPort())
mapper.SetScalarModeToUsePointData()
mapper.SetScalarRange(0, 2)

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("cell data to point data")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
