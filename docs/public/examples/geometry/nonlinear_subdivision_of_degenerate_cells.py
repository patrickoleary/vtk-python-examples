#!/usr/bin/env python
# Demonstrate nonlinear subdivision of degenerate Lagrange hexahedron cells.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create an unstructured grid with degenerate Lagrange hexahedra.
grid = vtkUnstructuredGrid()
points = vtkPoints()
points.SetNumberOfPoints(5)
points.SetPoint(0, 0, 0, 0)
points.SetPoint(1, 1, 0, 0)
points.SetPoint(2, 0, 1, 0)
points.SetPoint(3, 1, 1, 0)
points.SetPoint(4, 0.5, 0.5, 0.5)
grid.SetPoints(points)

# VTK_LAGRANGE_HEXAHEDRON = 72
connectivity_1 = [4, 1, 3, 4, 0, 0, 0, 0]
connectivity_2 = [0, 0, 0, 0, 3, 4, 4, 2]
cells = vtkCellArray()
cells.InsertNextCell(8, connectivity_1)
cells.InsertNextCell(8, connectivity_2)
grid.SetCells(72, cells)

# Extract surface with nonlinear subdivision.
surface_filter = vtkDataSetSurfaceFilter()
surface_filter.SetInputData(grid)
surface_filter.SetNonlinearSubdivisionLevel(3)
surface_filter.PassThroughCellIdsOff()
surface_filter.PassThroughPointIdsOff()
surface_filter.FastModeOn()
surface_filter.Update()

# Mapper and actor.
mapper = vtkDataSetMapper()
mapper.SetInputConnection(surface_filter.GetOutputPort())

prop = vtkProperty()
prop.LightingOff()
prop.SetRepresentationToSurface()
prop.EdgeVisibilityOff()
prop.SetOpacity(0.5)

actor = vtkActor()
actor.SetMapper(mapper)
actor.SetProperty(prop)

renderer = vtkRenderer()
renderer.AddActor(actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.AddRenderer(renderer)
render_window.SetWindowName("nonlinear subdivision of degenerate cells")

renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(10)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
