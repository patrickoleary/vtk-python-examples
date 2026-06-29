#!/usr/bin/env python
# Demonstrate editing a contour widget on terrain data with terrain interpolation.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkInteractionWidgets import (
    vtkContourWidget,
    vtkOrientedGlyphContourRepresentation,
    vtkTerrainContourLineInterpolator,
    vtkTerrainDataPointPlacer,
)
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))

# Filters
geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(dem_reader.GetOutputPort())

warp_scalar = vtkWarpScalar()
warp_scalar.SetInputConnection(geometry_filter.GetOutputPort())
warp_scalar.SetScaleFactor(1)
warp_scalar.UseNormalOn()
warp_scalar.SetNormal(0, 0, 1)
warp_scalar.Update()

normals_filter = vtkPolyDataNormals()
normals_filter.SetInputConnection(warp_scalar.GetOutputPort())
normals_filter.SetFeatureAngle(60)
normals_filter.SplittingOff()
normals_filter.Update()

# LUT for height field
lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

elevation_lut = vtkLookupTable()
elevation_lut.SetHueRange(0.6, 0)
elevation_lut.SetSaturationRange(1.0, 0)
elevation_lut.SetValueRange(0.5, 1.0)

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals_filter.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(elevation_lut)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("terrain polyline editor")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
contour_widget = vtkContourWidget()
contour_rep = vtkOrientedGlyphContourRepresentation.SafeDownCast(
    contour_widget.GetRepresentation()
)
contour_rep.GetLinesProperty().SetColor(1.0, 0.0, 0.0)
contour_widget.SetInteractor(interactor)

point_placer = vtkTerrainDataPointPlacer()
point_placer.AddProp(dem_actor)
contour_rep.SetPointPlacer(point_placer)

interpolator = vtkTerrainContourLineInterpolator()
contour_rep.SetLineInterpolator(interpolator)
interpolator.SetImageData(dem_reader.GetOutput())

contour_widget.EnabledOn()

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
