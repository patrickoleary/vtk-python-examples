#!/usr/bin/env python

# Demonstrate vtkMergeCells by creating two adjacent hexahedra with
# slightly perturbed shared vertices, merging them with different
# tolerances, and rendering the merged result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkIdTypeArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonCore import VTK_DOUBLE
from vtkmodules.vtkCommonDataModel import (
    VTK_HEXAHEDRON,
    vtkUnstructuredGrid,
)
from vtkmodules.vtkFiltersGeneral import vtkMergeCells
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Perturbation amplitude
amplitude = 1.0e-13
vtkMath.RandomSeed(8775070)

# Build hexahedron 0 at origin
length = 1.0
pts_0 = vtkPoints()
pts_0.SetDataType(VTK_DOUBLE)
pts_0.InsertNextPoint(0, 0, 0)
pts_0.InsertNextPoint(length, 0, 0)
pts_0.InsertNextPoint(length, length, 0)
pts_0.InsertNextPoint(0, length, 0)
pts_0.InsertNextPoint(0, 0, length)
pts_0.InsertNextPoint(length, 0, length)
pts_0.InsertNextPoint(length, length, length)
pts_0.InsertNextPoint(0, length, length)

mesh_0 = vtkUnstructuredGrid()
mesh_0.SetPoints(pts_0)
mesh_0.Allocate(1)
mesh_0.InsertNextCell(VTK_HEXAHEDRON, 8, list(range(8)))

ids_0 = vtkIdTypeArray()
ids_0.SetName("GlobalCellIds")
ids_0.SetNumberOfValues(1)
ids_0.SetValue(0, 0)
mesh_0.GetCellData().SetGlobalIds(ids_0)

# Build hexahedron 1 offset in y with perturbed points
pts_1 = vtkPoints()
pts_1.SetDataType(VTK_DOUBLE)
origin_1 = [0.0, length, 0.0]
base_pts = [
    (origin_1[0], origin_1[1], origin_1[2]),
    (origin_1[0] + length, origin_1[1], origin_1[2]),
    (origin_1[0] + length, origin_1[1] + length, origin_1[2]),
    (origin_1[0], origin_1[1] + length, origin_1[2]),
    (origin_1[0], origin_1[1], origin_1[2] + length),
    (origin_1[0] + length, origin_1[1], origin_1[2] + length),
    (origin_1[0] + length, origin_1[1] + length, origin_1[2] + length),
    (origin_1[0], origin_1[1] + length, origin_1[2] + length),
]

for px, py, pz in base_pts:
    rx = (1 if vtkMath.Random(-1, 1) >= 0 else -1) * vtkMath.Random(0.5, 0.7) * amplitude
    ry = (1 if vtkMath.Random(-1, 1) >= 0 else -1) * vtkMath.Random(0.5, 0.7) * amplitude
    rz = (1 if vtkMath.Random(-1, 1) >= 0 else -1) * vtkMath.Random(0.5, 0.7) * amplitude
    pts_1.InsertNextPoint(px + rx, py + ry, pz + rz)

mesh_1 = vtkUnstructuredGrid()
mesh_1.SetPoints(pts_1)
mesh_1.Allocate(1)
mesh_1.InsertNextCell(VTK_HEXAHEDRON, 8, list(range(8)))

ids_1 = vtkIdTypeArray()
ids_1.SetName("GlobalCellIds")
ids_1.SetNumberOfValues(1)
ids_1.SetValue(0, 1)
mesh_1.GetCellData().SetGlobalIds(ids_1)

# Merge with tolerance larger than perturbation (4 points should merge)
tolerance = amplitude * 10
merge_cells = vtkMergeCells()
merge_cells.SetTotalNumberOfPoints(16)
merge_cells.SetTotalNumberOfCells(2)
merge_cells.SetTotalNumberOfDataSets(2)
merge_cells.SetPointMergeTolerance(tolerance)
merge_cells.SetUseGlobalCellIds(1)
merge_cells.SetUseGlobalIds(0)

merged_grid = vtkUnstructuredGrid()
merge_cells.SetUnstructuredGrid(merged_grid)
merge_cells.MergeDataSet(mesh_0)
merge_cells.MergeDataSet(mesh_1)
merge_cells.Finish()

# Extract surface for rendering
surface = vtkDataSetSurfaceFilter()
surface.SetInputData(merge_cells.GetUnstructuredGrid())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetEdgeVisibility(True)
actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("merge cells")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Azimuth(30)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
