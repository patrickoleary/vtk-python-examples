#!/usr/bin/env python

# Demonstrate vtkTrimmedExtrusionFilter by reading a DEM height field,
# creating polygons at elevation, and extruding them down to the terrain
# surface along the z-axis.

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
from vtkmodules.vtkFiltersModeling import vtkTrimmedExtrusionFilter
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

scalar_low = dem_reader.GetOutput().GetScalarRange()[0]
scalar_high = dem_reader.GetOutput().GetScalarRange()[1]

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
warp.Update()

# Terrain actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(warp.GetOutputPort())
dem_mapper.SetScalarRange(scalar_low, scalar_high)
dem_mapper.SetLookupTable(lookup_table)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Create polygons to extrude at various elevations
polygons = vtkPolyData()
extrusion_points = vtkPoints()
extrusion_points.SetNumberOfPoints(14)
extrusion_points.SetPoint(0, 560000, 5110000, 2000)
extrusion_points.SetPoint(1, 560250, 5110000, 2000)
extrusion_points.SetPoint(2, 560250, 5110250, 2000)
extrusion_points.SetPoint(3, 560000, 5110250, 2000)
extrusion_points.SetPoint(4, 560500, 5110000, 2100)
extrusion_points.SetPoint(5, 560750, 5110000, 2100)
extrusion_points.SetPoint(6, 560750, 5110250, 2100)
extrusion_points.SetPoint(7, 560500, 5110250, 2100)
extrusion_points.SetPoint(8, 559800, 5110500, 1950)
extrusion_points.SetPoint(9, 560500, 5110500, 1950)
extrusion_points.SetPoint(10, 560500, 5110800, 1950)
extrusion_points.SetPoint(11, 560150, 5110800, 1950)
extrusion_points.SetPoint(12, 560150, 5111100, 1950)
extrusion_points.SetPoint(13, 559800, 5111100, 1950)

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

polygons.SetPoints(extrusion_points)
polygons.SetPolys(polys)

# Extrude polygons down to terrain surface
extrude = vtkTrimmedExtrusionFilter()
extrude.SetInputData(polygons)
extrude.SetTrimSurfaceConnection(warp.GetOutputPort())
extrude.SetExtrusionDirection(0, 0, 1)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(extrude.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)

# Show generating polygons (slightly offset to avoid z-fighting)
poly_mapper = vtkPolyDataMapper()
poly_mapper.SetInputData(polygons)
poly_mapper.ScalarVisibilityOff()

poly_actor = vtkActor()
poly_actor.SetMapper(poly_mapper)
poly_actor.GetProperty().SetColor(1, 0, 0)
poly_actor.AddPosition(0, 0, 10)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.AddActor(actor)
renderer.AddActor(poly_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("trimmed extrusion filter")

# Scene
renderer.GetActiveCamera().SetPosition(560752, 5110002, 2110)
renderer.GetActiveCamera().SetFocalPoint(560750, 5110000, 2100)
renderer.ResetCamera()
renderer.GetActiveCamera().SetClippingRange(269.775, 34560.4)
renderer.GetActiveCamera().SetFocalPoint(562026, 5.1135e+006, -400.794)
renderer.GetActiveCamera().SetPosition(556898, 5.10151e+006, 7906.19)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
