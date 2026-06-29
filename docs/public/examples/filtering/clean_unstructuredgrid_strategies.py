#!/usr/bin/env python

# Demonstrate vtkCleanUnstructuredGrid with different point data weighing
# strategies (first point, averaging, spatial density) on two tetrahedra
# sharing a coincident point, and visualize the cleaned results.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkDoubleArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    VTK_TETRA,
    vtkCellArray,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkCleanUnstructuredGrid
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Two tetrahedra sharing one coincident point (point 3 == point 4)
tetra_coords = [
    0.0, 0.0, 0.0,
    1.0, 0.0, 0.0,
    0.0, 1.0, 0.0,
    0.0, 0.0, 1.0,
    0.0, 0.0, 1.0,
    2.0, 0.0, 1.0,
    0.0, 1.0, 1.0,
    0.0, 0.0, 2.0,
]

# Build unstructured grid
point_array = vtkDoubleArray()
point_array.SetNumberOfComponents(3)
point_array.SetNumberOfTuples(8)
for i in range(8):
    point_array.SetTuple3(i, tetra_coords[i * 3], tetra_coords[i * 3 + 1], tetra_coords[i * 3 + 2])

pts = vtkPoints()
pts.SetData(point_array)

cells = vtkCellArray()
cells.InsertNextCell(4, [0, 1, 2, 3])
cells.InsertNextCell(4, [4, 5, 6, 7])

# Scalar data: iota 0..7
scalars = vtkDoubleArray()
scalars.SetName("IotaScalar")
scalars.SetNumberOfTuples(8)
for i in range(8):
    scalars.SetValue(i, float(i))

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(pts)
ugrid.SetCells(VTK_TETRA, cells)
ugrid.GetPointData().AddArray(scalars)

# --- Col 0: FirstPoint strategy ---
cleaner_0 = vtkCleanUnstructuredGrid()
cleaner_0.SetPointDataWeighingStrategy(0)
cleaner_0.SetInputData(ugrid)
cleaner_0.Update()

surface_0 = vtkDataSetSurfaceFilter()
surface_0.SetInputConnection(cleaner_0.GetOutputPort())

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(surface_0.GetOutputPort())
mapper_0.SetScalarModeToUsePointFieldData()
mapper_0.SelectColorArray("IotaScalar")
mapper_0.SetScalarRange(0, 7)

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0.1, 0.2, 0.4)
renderer_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 1.0)

# --- Col 1: Averaging strategy ---
cleaner_1 = vtkCleanUnstructuredGrid()
cleaner_1.SetPointDataWeighingStrategy(1)
cleaner_1.SetInputData(ugrid)
cleaner_1.Update()

surface_1 = vtkDataSetSurfaceFilter()
surface_1.SetInputConnection(cleaner_1.GetOutputPort())

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(surface_1.GetOutputPort())
mapper_1.SetScalarModeToUsePointFieldData()
mapper_1.SelectColorArray("IotaScalar")
mapper_1.SetScalarRange(0, 7)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0.1, 0.2, 0.4)
renderer_1.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 1.0)

# --- Col 2: SpatialDensity strategy ---
cleaner_2 = vtkCleanUnstructuredGrid()
cleaner_2.SetPointDataWeighingStrategy(2)
cleaner_2.SetInputData(ugrid)
cleaner_2.Update()

surface_2 = vtkDataSetSurfaceFilter()
surface_2.SetInputConnection(cleaner_2.GetOutputPort())

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(surface_2.GetOutputPort())
mapper_2.SetScalarModeToUsePointFieldData()
mapper_2.SelectColorArray("IotaScalar")
mapper_2.SetScalarRange(0, 7)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(0.1, 0.2, 0.4)
renderer_2.SetViewport(2.0 / 3.0, 0.0, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("clean unstructuredgrid strategies")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

interactor.Initialize()
interactor.Start()
