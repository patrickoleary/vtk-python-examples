#!/usr/bin/env python

# Segment a plane mesh using vtkPolyDataEdgeConnectivityFilter with
# scalar connectivity, barrier edges from explicit source, and cell region areas.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import (
    vtkPointDataToCellData,
    vtkPolyDataEdgeConnectivityFilter,
    vtkSimpleElevationFilter,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: regular plane
plane = vtkPlaneSource()
plane.SetResolution(10, 10)
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(10, 0, 0)
plane.SetPoint2(0, 10, 0)

# Color by elevation
elevation = vtkSimpleElevationFilter()
elevation.SetInputConnection(plane.GetOutputPort())
elevation.SetVector(1, 0, 0)

# Convert to cell scalars
cell_scalars = vtkPointDataToCellData()
cell_scalars.SetInputConnection(elevation.GetOutputPort())
cell_scalars.Update()

# Create barrier edges from specific point ids
edges = vtkCellArray()
edges.InsertNextCell(2, [68, 69])
edges.InsertNextCell(2, [69, 70])

barrier_edges = vtkPolyData()
barrier_edges.SetPoints(cell_scalars.GetOutput().GetPoints())
barrier_edges.SetLines(edges)

# Edge connectivity with scalar range and barrier edges
connectivity = vtkPolyDataEdgeConnectivityFilter()
connectivity.SetInputConnection(cell_scalars.GetOutputPort())
connectivity.SetSourceData(barrier_edges)
connectivity.ScalarConnectivityOn()
connectivity.SetScalarRange(2, 4)
connectivity.BarrierEdgesOn()
connectivity.GrowLargeRegionsOff()
connectivity.SetExtractionModeToAllRegions()
connectivity.ColorRegionsOn()
connectivity.CellRegionAreasOn()
connectivity.Update()

print(f"Num cells: {connectivity.GetOutput().GetNumberOfCells()}")
print(f"Num regions: {connectivity.GetNumberOfExtractedRegions()}")
print(f"Total area: {connectivity.GetTotalArea()}")

# Mapper colored by region
tess_mapper = vtkPolyDataMapper()
tess_mapper.SetInputConnection(connectivity.GetOutputPort())
tess_mapper.ScalarVisibilityOn()
tess_mapper.SetScalarModeToUseCellData()
tess_mapper.SetScalarRange(0, 2)

tess_actor = vtkActor()
tess_actor.SetMapper(tess_mapper)
tess_actor.GetProperty().SetColor(1, 1, 1)
tess_actor.GetProperty().EdgeVisibilityOn()
tess_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(tess_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("edge connectivity scalar barrier")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
