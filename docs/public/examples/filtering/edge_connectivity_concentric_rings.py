#!/usr/bin/env python

# Segment a tessellated mesh with two concentric disk rings using
# vtkPolyDataEdgeConnectivityFilter with barrier edges and sorted regions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkAppendPolyData,
    vtkDelaunay2D,
    vtkFeatureEdges,
    vtkPolyDataEdgeConnectivityFilter,
)
from vtkmodules.vtkFiltersSources import (
    vtkDiskSource,
    vtkPlaneSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Bounding plane
plane = vtkPlaneSource()
plane.SetResolution(10, 10)
plane.SetOrigin(-5, -5, 0)
plane.SetPoint1(5, -5, 0)
plane.SetPoint2(-5, 5, 0)

# Extract boundary edges
boundary_edges = vtkFeatureEdges()
boundary_edges.SetInputConnection(plane.GetOutputPort())
boundary_edges.ExtractAllEdgeTypesOff()
boundary_edges.BoundaryEdgesOn()
boundary_edges.Update()

# Inner disk ring
disk = vtkDiskSource()
disk.SetInnerRadius(0.5)
disk.SetOuterRadius(1.0)
disk.SetRadialResolution(1)
disk.SetCircumferentialResolution(32)
disk.Update()

# Outer disk ring
disk_2 = vtkDiskSource()
disk_2.SetInnerRadius(2.0)
disk_2.SetOuterRadius(3.5)
disk_2.SetRadialResolution(1)
disk_2.SetCircumferentialResolution(64)
disk_2.Update()

# Append and tessellate
append = vtkAppendPolyData()
append.AddInputData(boundary_edges.GetOutput())
append.AddInputData(disk.GetOutput())
append.AddInputData(disk_2.GetOutput())
append.Update()

tessellation = vtkDelaunay2D()
tessellation.SetInputConnection(append.GetOutputPort())
tessellation.Update()

# Edge connectivity with barrier edges and sorted regions
connectivity = vtkPolyDataEdgeConnectivityFilter()
connectivity.SetInputConnection(tessellation.GetOutputPort())
connectivity.BarrierEdgesOn()
connectivity.GrowSmallRegionsOn()
connectivity.SetBarrierEdgeLength(0.0, 0.35)
connectivity.SetExtractionModeToAllRegions()
connectivity.SetLargeRegionThreshold(0.25)
connectivity.ColorRegionsOn()
connectivity.CellRegionAreasOn()
connectivity.Update()

print(f"Num cells: {connectivity.GetOutput().GetNumberOfCells()}")
print(f"Num regions: {connectivity.GetNumberOfExtractedRegions()}")

# Mapper colored by region
tess_mapper = vtkPolyDataMapper()
tess_mapper.SetInputConnection(connectivity.GetOutputPort())
tess_mapper.ScalarVisibilityOn()
tess_mapper.SetScalarModeToUseCellData()
tess_mapper.SetScalarRange(0, 2)

tess_actor = vtkActor()
tess_actor.SetMapper(tess_mapper)
tess_actor.GetProperty().SetColor(1, 1, 1)
tess_actor.GetProperty().SetEdgeColor(0, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0, 0, 0)
renderer.AddActor(tess_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("edge connectivity concentric rings")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
