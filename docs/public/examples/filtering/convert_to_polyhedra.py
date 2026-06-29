#!/usr/bin/env python

# Convert hex and quad cells to polyhedra using vtkConvertToPolyhedra,
# displaying results with all cells and only convertible cells side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkConvertToPolyhedra
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build an unstructured grid with a hex and a quad
grid = vtkUnstructuredGrid()

grid_points = vtkPoints()
grid_points.SetNumberOfPoints(12)

# Hex points
grid_points.SetPoint(0, 0, 0, 0)
grid_points.SetPoint(1, 1, 0, 0)
grid_points.SetPoint(2, 1, 1, 0)
grid_points.SetPoint(3, 0, 1, 0)
grid_points.SetPoint(4, 0, 0, 1)
grid_points.SetPoint(5, 1, 0, 1)
grid_points.SetPoint(6, 1, 1, 1)
grid_points.SetPoint(7, 0, 1, 1)

# Quad points
grid_points.SetPoint(8, 4, 0, 0.5)
grid_points.SetPoint(9, 5, 0, 0.5)
grid_points.SetPoint(10, 5, 1, 0.5)
grid_points.SetPoint(11, 4, 1, 0.5)

grid.SetPoints(grid_points)

# Insert hex cell (type 12)
cell_pts = [0, 1, 2, 3, 4, 5, 6, 7]
grid.InsertNextCell(12, 8, cell_pts)

# Insert quad cell (type 9)
cell_pts = [8, 9, 10, 11]
grid.InsertNextCell(9, 4, cell_pts)

# Cell scalars
cell_scalars = vtkFloatArray()
cell_scalars.SetNumberOfTuples(2)
cell_scalars.SetTuple1(0, 0)
cell_scalars.SetTuple1(1, 2)
grid.GetCellData().SetScalars(cell_scalars)

# Convert to polyhedra (all cells)
convert_all = vtkConvertToPolyhedra()
convert_all.SetInputData(grid)
convert_all.OutputAllCellsOn()
convert_all.Update()

# Convert again (handles already-polyhedra input)
convert_2 = vtkConvertToPolyhedra()
convert_2.SetInputConnection(convert_all.GetOutputPort())
convert_2.OutputAllCellsOn()
convert_2.Update()

# Convert only convertible types (excludes quad)
convert_3d_only = vtkConvertToPolyhedra()
convert_3d_only.SetInputConnection(convert_all.GetOutputPort())
convert_3d_only.OutputAllCellsOff()
convert_3d_only.Update()

# Mapper for all cells
mapper_all = vtkDataSetMapper()
mapper_all.SetInputConnection(convert_2.GetOutputPort())
mapper_all.SetScalarRange(0, 2)

actor_all = vtkActor()
actor_all.SetMapper(mapper_all)
actor_all.GetProperty().SetInterpolationToFlat()

# Mapper for 3D-only cells
mapper_3d = vtkDataSetMapper()
mapper_3d.SetInputConnection(convert_3d_only.GetOutputPort())
mapper_3d.SetScalarRange(0, 2)

actor_3d = vtkActor()
actor_3d.SetMapper(mapper_3d)
actor_3d.GetProperty().SetInterpolationToFlat()
actor_3d.AddPosition(2, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_all)
renderer.AddActor(actor_3d)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 100)
render_window.SetWindowName("convert to polyhedra")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(2.5, 0.5, 6)
camera.SetFocalPoint(2.5, 0.5, 0)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
