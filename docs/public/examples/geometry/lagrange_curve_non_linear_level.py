#!/usr/bin/env python
# Demonstrate Lagrange curve with non-linear subdivision level rendering.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create an unstructured grid with a Lagrange curve cell.
dataset = vtkUnstructuredGrid()

points = vtkPoints()
points.SetNumberOfPoints(4)
points.SetPoint(0, 0, 1, 0)
points.SetPoint(1, 0.33, 0.8, 0)
points.SetPoint(2, 0.66, 0.5, 0)
points.SetPoint(3, 1, 0, 0)
dataset.SetPoints(points)

# VTK_LAGRANGE_CURVE = 68, connectivity: 0, 3, 1, 2 (order 3)
cells = vtkCellArray()
cells.InsertNextCell(4, [0, 3, 1, 2])
dataset.SetCells(68, cells)

# Extract surface with non-linear subdivision.
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputData(dataset)
surface_filter.SetNonlinearSubdivisionLevel(2)

# Mapper and actor.
mapper = vtkDataSetMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("lagrange curve non linear level")

renderer.ResetCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
