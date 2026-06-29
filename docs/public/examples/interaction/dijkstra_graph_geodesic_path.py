#!/usr/bin/env python
# Demonstrate vtkContourWidget with Dijkstra geodesic path on a terrain surface.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkInteractionWidgets import (
    vtkContourWidget,
    vtkOrientedGlyphContourRepresentation,
    vtkPolygonalSurfaceContourLineInterpolator,
    vtkPolygonalSurfacePointPlacer,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

# Filters
resample = vtkImageResample()
resample.SetInputConnection(dem_reader.GetOutputPort())
resample.SetDimensionality(2)
resample.SetAxisMagnificationFactor(0, 1.0)
resample.SetAxisMagnificationFactor(1, 1.0)

surface = vtkImageDataGeometryFilter()
surface.SetInputConnection(resample.GetOutputPort())

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(surface.GetOutputPort())
triangle_filter.Update()

warp = vtkWarpScalar()
warp.SetInputConnection(triangle_filter.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)
warp.Update()

warp_output = warp.GetPolyDataOutput()

# Mapper + Actor
scalar_lo = dem_reader.GetOutput().GetScalarRange()[0]
scalar_hi = dem_reader.GetOutput().GetScalarRange()[1]

lut = vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)

dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputData(warp_output)
dem_mapper.SetScalarRange(scalar_lo, scalar_hi)
dem_mapper.SetLookupTable(lut)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dijkstra graph geodesic path")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
contour_widget = vtkContourWidget()
contour_widget.SetInteractor(interactor)

contour_rep = vtkOrientedGlyphContourRepresentation.SafeDownCast(
    contour_widget.GetRepresentation()
)
contour_rep.GetLinesProperty().SetColor(1, 0.2, 0)
contour_rep.GetLinesProperty().SetLineWidth(3.0)

point_placer = vtkPolygonalSurfacePointPlacer()
point_placer.AddProp(dem_actor)
point_placer.GetPolys().AddItem(warp_output)
point_placer.SnapToClosestPointOn()
contour_rep.SetPointPlacer(point_placer)

interpolator = vtkPolygonalSurfaceContourLineInterpolator()
interpolator.GetPolys().AddItem(warp_output)
contour_rep.SetLineInterpolator(interpolator)

contour_widget.EnabledOn()

# Scene
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().SetPosition(-99900, -21354, 131801)
renderer.GetActiveCamera().SetFocalPoint(41461, 41461, 2815)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(4.2)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
