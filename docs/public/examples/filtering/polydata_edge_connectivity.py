#!/usr/bin/env python

# Segment a tessellated mesh into regions using
# vtkPolyDataEdgeConnectivityFilter with barrier edges and region growing.

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

# Bounding plane to improve tessellation
plane = vtkPlaneSource()
plane.SetResolution(10, 10)
plane.SetOrigin(-2, -2, 0)
plane.SetPoint1(2, -2, 0)
plane.SetPoint2(-2, 2, 0)

# Extract boundary edges from the plane
boundary_edges = vtkFeatureEdges()
boundary_edges.SetInputConnection(plane.GetOutputPort())
boundary_edges.ExtractAllEdgeTypesOff()
boundary_edges.BoundaryEdgesOn()
boundary_edges.Update()

# Concentric ring disk
disk = vtkDiskSource()
disk.SetInnerRadius(0.5)
disk.SetOuterRadius(1.0)
disk.SetRadialResolution(1)
disk.SetCircumferentialResolution(32)
disk.Update()

# Append boundary and disk points
append = vtkAppendPolyData()
append.AddInputData(boundary_edges.GetOutput())
append.AddInputData(disk.GetOutput())
append.Update()

# Delaunay tessellation
tessellation = vtkDelaunay2D()
tessellation.SetInputConnection(append.GetOutputPort())
tessellation.Update()

# Edge connectivity segmentation with barrier edges
connectivity = vtkPolyDataEdgeConnectivityFilter()
connectivity.SetInputConnection(tessellation.GetOutputPort())
connectivity.BarrierEdgesOn()
connectivity.SetBarrierEdgeLength(0.0, 0.20)
connectivity.GrowLargeRegionsOn()
connectivity.SetExtractionModeToLargeRegions()
connectivity.SetLargeRegionThreshold(0.04)
connectivity.ColorRegionsOn()
connectivity.Update()

print(f"Num cells: {connectivity.GetOutput().GetNumberOfCells()}")
print(f"Num regions: {connectivity.GetNumberOfExtractedRegions()}")

# Mapper colored by region
tess_mapper = vtkPolyDataMapper()
tess_mapper.SetInputConnection(connectivity.GetOutputPort())
tess_mapper.ScalarVisibilityOn()
tess_mapper.SetScalarModeToUseCellData()
tess_mapper.SetScalarRange(0, connectivity.GetNumberOfExtractedRegions() - 1)

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
render_window.SetWindowName("polydata edge connectivity")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
