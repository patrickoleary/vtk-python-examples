#!/usr/bin/env python

# Read a DEM elevation model file and render with LOD actors at multiple resolutions.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import vtkCastToConcrete
from vtkmodules.vtkFiltersCore import (
    vtkElevationFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

scale = 5

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

# Read DEM file
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

elevation_lo = scale * dem_reader.GetElevationBounds()[0]
elevation_hi = scale * dem_reader.GetElevationBounds()[1]

# LOD 1 — shrink factor 4
lod1_shrink = vtkImageShrink3D()
lod1_shrink.SetShrinkFactors(4, 4, 1)
lod1_shrink.SetInputConnection(dem_reader.GetOutputPort())
lod1_shrink.AveragingOn()

lod1_geometry = vtkImageDataGeometryFilter()
lod1_geometry.SetInputConnection(lod1_shrink.GetOutputPort())
lod1_geometry.ReleaseDataFlagOn()

lod1_warp = vtkWarpScalar()
lod1_warp.SetInputConnection(lod1_geometry.GetOutputPort())
lod1_warp.SetNormal(0, 0, 1)
lod1_warp.UseNormalOn()
lod1_warp.SetScaleFactor(scale)
lod1_warp.ReleaseDataFlagOn()

lod1_elevation = vtkElevationFilter()
lod1_elevation.SetInputConnection(lod1_warp.GetOutputPort())
lod1_elevation.SetLowPoint(0, 0, elevation_lo)
lod1_elevation.SetHighPoint(0, 0, elevation_hi)
lod1_elevation.SetScalarRange(elevation_lo, elevation_hi)
lod1_elevation.ReleaseDataFlagOn()

lod1_cast = vtkCastToConcrete()
lod1_cast.SetInputConnection(lod1_elevation.GetOutputPort())

lod1_normals = vtkPolyDataNormals()
lod1_normals.SetInputConnection(lod1_cast.GetOutputPort())
lod1_normals.SetFeatureAngle(60)
lod1_normals.ConsistencyOff()
lod1_normals.SplittingOff()
lod1_normals.ReleaseDataFlagOn()

lod1_mapper = vtkPolyDataMapper()
lod1_mapper.SetInputConnection(lod1_normals.GetOutputPort())
lod1_mapper.SetScalarRange(elevation_lo, elevation_hi)
lod1_mapper.SetLookupTable(lookup_table)
lod1_mapper.Update()

# LOD 2 — shrink factor 8
lod2_shrink = vtkImageShrink3D()
lod2_shrink.SetShrinkFactors(8, 8, 1)
lod2_shrink.SetInputConnection(dem_reader.GetOutputPort())
lod2_shrink.AveragingOn()

lod2_geometry = vtkImageDataGeometryFilter()
lod2_geometry.SetInputConnection(lod2_shrink.GetOutputPort())
lod2_geometry.ReleaseDataFlagOn()

lod2_warp = vtkWarpScalar()
lod2_warp.SetInputConnection(lod2_geometry.GetOutputPort())
lod2_warp.SetNormal(0, 0, 1)
lod2_warp.UseNormalOn()
lod2_warp.SetScaleFactor(scale)
lod2_warp.ReleaseDataFlagOn()

lod2_elevation = vtkElevationFilter()
lod2_elevation.SetInputConnection(lod2_warp.GetOutputPort())
lod2_elevation.SetLowPoint(0, 0, elevation_lo)
lod2_elevation.SetHighPoint(0, 0, elevation_hi)
lod2_elevation.SetScalarRange(elevation_lo, elevation_hi)
lod2_elevation.ReleaseDataFlagOn()

lod2_cast = vtkCastToConcrete()
lod2_cast.SetInputConnection(lod2_elevation.GetOutputPort())

lod2_normals = vtkPolyDataNormals()
lod2_normals.SetInputConnection(lod2_cast.GetOutputPort())
lod2_normals.SetFeatureAngle(60)
lod2_normals.ConsistencyOff()
lod2_normals.SplittingOff()
lod2_normals.ReleaseDataFlagOn()

lod2_mapper = vtkPolyDataMapper()
lod2_mapper.SetInputConnection(lod2_normals.GetOutputPort())
lod2_mapper.SetScalarRange(elevation_lo, elevation_hi)
lod2_mapper.SetLookupTable(lookup_table)
lod2_mapper.Update()

# LOD 3 — shrink factor 16
lod3_shrink = vtkImageShrink3D()
lod3_shrink.SetShrinkFactors(16, 16, 1)
lod3_shrink.SetInputConnection(dem_reader.GetOutputPort())
lod3_shrink.AveragingOn()

lod3_geometry = vtkImageDataGeometryFilter()
lod3_geometry.SetInputConnection(lod3_shrink.GetOutputPort())
lod3_geometry.ReleaseDataFlagOn()

lod3_warp = vtkWarpScalar()
lod3_warp.SetInputConnection(lod3_geometry.GetOutputPort())
lod3_warp.SetNormal(0, 0, 1)
lod3_warp.UseNormalOn()
lod3_warp.SetScaleFactor(scale)
lod3_warp.ReleaseDataFlagOn()

lod3_elevation = vtkElevationFilter()
lod3_elevation.SetInputConnection(lod3_warp.GetOutputPort())
lod3_elevation.SetLowPoint(0, 0, elevation_lo)
lod3_elevation.SetHighPoint(0, 0, elevation_hi)
lod3_elevation.SetScalarRange(elevation_lo, elevation_hi)
lod3_elevation.ReleaseDataFlagOn()

lod3_cast = vtkCastToConcrete()
lod3_cast.SetInputConnection(lod3_elevation.GetOutputPort())

lod3_normals = vtkPolyDataNormals()
lod3_normals.SetInputConnection(lod3_cast.GetOutputPort())
lod3_normals.SetFeatureAngle(60)
lod3_normals.ConsistencyOff()
lod3_normals.SplittingOff()
lod3_normals.ReleaseDataFlagOn()

lod3_mapper = vtkPolyDataMapper()
lod3_mapper.SetInputConnection(lod3_normals.GetOutputPort())
lod3_mapper.SetScalarRange(elevation_lo, elevation_hi)
lod3_mapper.SetLookupTable(lookup_table)
lod3_mapper.Update()

# Actor
dem_actor = vtkLODActor()
dem_actor.AddLODMapper(lod1_mapper)
dem_actor.AddLODMapper(lod2_mapper)
dem_actor.AddLODMapper(lod3_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.4, 0.4, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dem")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetDesiredUpdateRate(1)

# Scene
camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetPosition(-99900, -21354, 131801)
camera.SetFocalPoint(41461, 41461, 2815)
renderer.ResetCamera()
camera.Dolly(1.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
