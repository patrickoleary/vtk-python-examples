#!/usr/bin/env python
# Demonstrate a distance widget constrained to lie on a polygonal terrain surface.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkInteractionWidgets import (
    vtkDistanceRepresentation2D,
    vtkDistanceWidget,
    vtkPointHandleRepresentation3D,
    vtkPolygonalSurfacePointPlacer,
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

lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

warp_output = warp.GetPolyDataOutput()

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputData(warp_output)
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(lookup_table)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polygonal surface constrained distance widget")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
distance_rep = vtkDistanceRepresentation2D()
distance_rep.GetAxis().GetProperty().SetColor(0.0, 0.0, 1.0)

handle_rep_3d = vtkPointHandleRepresentation3D()
handle_rep_3d.GetProperty().SetLineWidth(4.0)
handle_rep_3d.GetProperty().SetColor(0.0, 0.0, 0.5)
distance_rep.SetHandleRepresentation(handle_rep_3d)

point_placer = vtkPolygonalSurfacePointPlacer()
point_placer.AddProp(dem_actor)
point_placer.GetPolys().AddItem(warp_output)

distance_rep.InstantiateHandleRepresentation()
distance_rep.GetPoint1Representation().SetPointPlacer(point_placer)
distance_rep.GetPoint2Representation().SetPointPlacer(point_placer)

distance_widget = vtkDistanceWidget()
distance_widget.SetInteractor(interactor)
distance_widget.SetRepresentation(distance_rep)
distance_widget.EnabledOn()

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
