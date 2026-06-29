#!/usr/bin/env python
# Demonstrate vtkInteractorStyleTerrain on DEM elevation data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter, vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTerrain
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
scale = 5

lut = vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)

# Read DEM data
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

elevation_low = scale * dem_reader.GetElevationBounds()[0]
elevation_high = scale * dem_reader.GetElevationBounds()[1]

# Shrink for faster rendering
shrink = vtkImageShrink3D()
shrink.SetShrinkFactors(16, 16, 1)
shrink.SetInputConnection(dem_reader.GetOutputPort())
shrink.AveragingOn()

# Convert image data to geometry
geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(shrink.GetOutputPort())
geometry_filter.ReleaseDataFlagOn()

# Warp by elevation
warp = vtkWarpScalar()
warp.SetInputConnection(geometry_filter.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.UseNormalOn()
warp.SetScaleFactor(scale)
warp.ReleaseDataFlagOn()

# Color by elevation
elevation = vtkElevationFilter()
elevation.SetInputConnection(warp.GetOutputPort())
elevation.SetLowPoint(0, 0, elevation_low)
elevation.SetHighPoint(0, 0, elevation_high)
elevation.SetScalarRange(elevation_low, elevation_high)
elevation.ReleaseDataFlagOn()

# Compute normals
normals = vtkPolyDataNormals()
normals.SetInputConnection(elevation.GetOutputPort())
normals.SetFeatureAngle(60)
normals.ConsistencyOff()
normals.SplittingOff()
normals.ReleaseDataFlagOn()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(normals.GetOutputPort())
mapper.SetScalarRange(elevation_low, elevation_high)
mapper.SetLookupTable(lut)
mapper.Update()

actor = vtkActor()
actor.SetMapper(mapper)

# Rendering with terrain interaction style
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.4, 0.4, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("interactor style terrain")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

style = vtkInteractorStyleTerrain()
interactor.SetInteractorStyle(style)
interactor.SetDesiredUpdateRate(1)

# Camera setup
camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetPosition(-99900, -21354, 131801)
camera.SetFocalPoint(41461, 41461, 2815)
renderer.ResetCamera()
camera.Dolly(1.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
