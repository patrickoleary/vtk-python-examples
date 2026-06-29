#!/usr/bin/env python
# Demonstrate vtkHandleWidget with vtkSphereHandleRepresentation on DEM terrain.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkInteractionWidgets import vtkHandleWidget, vtkSphereHandleRepresentation
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))

# Filters
resample = vtkImageResample()
resample.SetInputConnection(dem_reader.GetOutputPort())
resample.SetDimensionality(2)
resample.SetAxisMagnificationFactor(0, 1)
resample.SetAxisMagnificationFactor(1, 1)

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

# Lookup table
lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

elevation_lut = vtkLookupTable()
elevation_lut.SetHueRange(0.6, 0)
elevation_lut.SetSaturationRange(1.0, 0)
elevation_lut.SetValueRange(0.5, 1.0)

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(warp.GetOutputPort())
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
render_window.SetWindowName("sphere handle widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
handle_rep = vtkSphereHandleRepresentation()
handle_rep.SetWorldPosition([562532, 5.11396e+06, 2618.62])
handle_rep.GetProperty().SetColor(1.0, 0.0, 0.0)
handle_rep.GetProperty().SetLineWidth(1.0)
handle_rep.GetSelectedProperty().SetColor(0.2, 0.0, 1.0)

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(handle_rep)
handle_widget.EnableAxisConstraintOff()
handle_widget.EnabledOn()

# Scene
renderer.GetActiveCamera().SetViewUp(0, 0, 1)
renderer.GetActiveCamera().SetPosition(-99900, -21354, 131801)
renderer.GetActiveCamera().SetFocalPoint(41461, 41461, 2815)
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
