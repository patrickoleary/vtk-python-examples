#!/usr/bin/env python

# Demonstrate vtkFitToHeightMapFilter by reading a DEM height field,
# creating polygons, and fitting them to the terrain using both point
# projection and cell average height strategies in side-by-side renderers.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkFitToHeightMapFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Lookup table for terrain coloring
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

# Read DEM height field
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

elevation_low = dem_reader.GetOutput().GetScalarRange()[0]
elevation_high = dem_reader.GetOutput().GetScalarRange()[1]

# Create warped terrain surface
surface = vtkImageDataGeometryFilter()
surface.SetInputConnection(dem_reader.GetOutputPort())

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(surface.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(triangle_filter.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)

# Terrain actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(warp.GetOutputPort())
dem_mapper.SetScalarRange(elevation_low, elevation_high)
dem_mapper.SetLookupTable(lookup_table)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Create polygons to fit onto the terrain
polygons = vtkPolyData()
points = vtkPoints()
points.SetNumberOfPoints(14)
points.SetPoint(0, 560000, 5110000, 0)
points.SetPoint(1, 560250, 5110000, 0)
points.SetPoint(2, 560250, 5110250, 0)
points.SetPoint(3, 560000, 5110250, 0)
points.SetPoint(4, 560500, 5110000, 0)
points.SetPoint(5, 560750, 5110000, 0)
points.SetPoint(6, 560750, 5110250, 0)
points.SetPoint(7, 560500, 5110250, 0)
points.SetPoint(8, 559800, 5110500, 0)
points.SetPoint(9, 560500, 5110500, 0)
points.SetPoint(10, 560500, 5110800, 0)
points.SetPoint(11, 560150, 5110800, 0)
points.SetPoint(12, 560150, 5111100, 0)
points.SetPoint(13, 559800, 5111100, 0)

polys = vtkCellArray()
polys.InsertNextCell(4)
polys.InsertCellPoint(0)
polys.InsertCellPoint(1)
polys.InsertCellPoint(2)
polys.InsertCellPoint(3)
polys.InsertNextCell(4)
polys.InsertCellPoint(4)
polys.InsertCellPoint(5)
polys.InsertCellPoint(6)
polys.InsertCellPoint(7)
polys.InsertNextCell(6)
polys.InsertCellPoint(8)
polys.InsertCellPoint(9)
polys.InsertCellPoint(10)
polys.InsertCellPoint(11)
polys.InsertCellPoint(12)
polys.InsertCellPoint(13)

polygons.SetPoints(points)
polygons.SetPolys(polys)

# Fit polygons using point projection strategy
fit = vtkFitToHeightMapFilter()
fit.SetInputData(polygons)
fit.SetHeightMapConnection(dem_reader.GetOutputPort())
fit.SetFittingStrategyToPointProjection()
fit.UseHeightMapOffsetOn()
fit.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(fit.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

# Fit polygons using cell average height strategy
fit_2 = vtkFitToHeightMapFilter()
fit_2.SetInputData(polygons)
fit_2.SetHeightMapConnection(dem_reader.GetOutputPort())
fit_2.SetFittingStrategyToCellAverageHeight()
fit_2.UseHeightMapOffsetOn()
fit_2.Update()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(fit_2.GetOutputPort())
mapper_2.ScalarVisibilityOff()

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(1, 0, 0)

# Two renderers side by side
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(dem_actor)
renderer_0.AddActor(actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.AddActor(dem_actor)
renderer_1.AddActor(actor_2)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("fit to height map filter")

# Scene
renderer_0.GetActiveCamera().SetPosition(560752, 5110002, 2110)
renderer_0.GetActiveCamera().SetFocalPoint(560750, 5110000, 2100)
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetClippingRange(269.775, 34560.4)
renderer_0.GetActiveCamera().SetFocalPoint(562026, 5.1135e+006, -400.794)
renderer_0.GetActiveCamera().SetPosition(556898, 5.10151e+006, 7906.19)
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
