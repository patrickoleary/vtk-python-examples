#!/usr/bin/env python

# Clean an unstructured grid using vtkStaticCleanUnstructuredGrid
# with zero and non-zero tolerances, including shrunk data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkGenericCell,
    vtkSphere,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersCore import (
    vtkPointDataToCellData,
    vtkStaticCleanUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 25

# Source: sample a sphere implicit function
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(0.25)

sample_func = vtkSampleFunction()
sample_func.SetImplicitFunction(sphere)
sample_func.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample_func.SetSampleDimensions(resolution, resolution, resolution)

# Convert point data to cell data
point_to_cell = vtkPointDataToCellData()
point_to_cell.SetInputConnection(sample_func.GetOutputPort())
point_to_cell.PassPointDataOn()
point_to_cell.SetProcessAllArrays(False)
point_to_cell.AddPointDataArray("scalars")
point_to_cell.Update()

sample = point_to_cell.GetOutput()

# Build an unstructured grid from the second half of cells
points = vtkPoints()
cells = vtkCellArray()
grid = vtkUnstructuredGrid()
grid.SetPoints(points)

num_pts = sample.GetNumberOfPoints()
points.SetNumberOfPoints(num_pts)
grid.GetPointData().ShallowCopy(sample.GetPointData())
for p_id in range(num_pts):
    points.SetPoint(p_id, sample.GetPoint(p_id))

num_cells = sample.GetNumberOfCells()
gen_cell = vtkGenericCell()
grid.GetCellData().CopyAllocate(sample.GetCellData())
for c_id in range(int(num_cells / 2), num_cells):
    sample.GetCell(c_id, gen_cell)
    new_id = grid.InsertNextCell(gen_cell.GetCellType(), gen_cell.GetPointIds())
    grid.GetCellData().CopyData(sample.GetCellData(), c_id, new_id)

# Clean with zero tolerance
clean_0 = vtkStaticCleanUnstructuredGrid()
clean_0.SetInputData(grid)
clean_0.ToleranceIsAbsoluteOn()
clean_0.SetTolerance(0.0)
clean_0.RemoveUnusedPointsOff()
clean_0.Update()

print(f"Grid: {grid.GetNumberOfPoints()} points, {grid.GetNumberOfCells()} cells")
print(f"Zero tolerance: {clean_0.GetOutput().GetNumberOfPoints()} points, {clean_0.GetOutput().GetNumberOfCells()} cells")

# Shrink then clean with non-zero tolerance
shrink = vtkShrinkFilter()
shrink.SetInputData(sample)
shrink.SetShrinkFactor(0.999)
shrink.Update()

clean_1 = vtkStaticCleanUnstructuredGrid()
clean_1.SetInputConnection(shrink.GetOutputPort())
clean_1.ToleranceIsAbsoluteOn()
clean_1.SetAbsoluteTolerance(0.01)
clean_1.ProduceMergeMapOn()
clean_1.AveragePointDataOn()
clean_1.Update()

print(f"Shrunk: {shrink.GetOutput().GetNumberOfPoints()} points, {shrink.GetOutput().GetNumberOfCells()} cells")
print(f"Non-zero tolerance: {clean_1.GetOutput().GetNumberOfPoints()} points, {clean_1.GetOutput().GetNumberOfCells()} cells")

# Mapper
mapper = vtkDataSetMapper()
mapper.SetInputConnection(clean_1.GetOutputPort())
mapper.SetScalarRange(sample.GetPointData().GetScalars().GetRange())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToFlat()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("clean unstructuredgrid")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1, 1, 1)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
