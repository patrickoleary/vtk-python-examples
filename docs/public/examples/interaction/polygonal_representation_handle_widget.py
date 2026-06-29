#!/usr/bin/env python
# Demonstrate a polygonal handle representation constrained to a terrain surface.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals, vtkTriangleFilter
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkImageResample
from vtkmodules.vtkInteractionWidgets import (
    vtkHandleWidget,
    vtkPolygonalHandleRepresentation3D,
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

lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

poly_normals = vtkPolyDataNormals()
poly_normals.SetInputConnection(warp.GetOutputPort())
poly_normals.SetFeatureAngle(60)
poly_normals.SplittingOff()
poly_normals.ComputeCellNormalsOn()
poly_normals.Update()

normals_output = poly_normals.GetOutput()

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputData(normals_output)
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
render_window.SetWindowName("polygonal representation handle widget")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
sphere = vtkSphereSource()
sphere.SetThetaResolution(10)
sphere.SetPhiResolution(10)
sphere.SetRadius(300.0)
sphere.Update()

handle_rep = vtkPolygonalHandleRepresentation3D()
handle_rep.SetHandle(sphere.GetOutput())

point_placer = vtkPolygonalSurfacePointPlacer()
point_placer.AddProp(dem_actor)
point_placer.GetPolys().AddItem(normals_output)
handle_rep.SetPointPlacer(point_placer)

handle_rep.SetWorldPosition((562532, 5.11396e+06, 2618.62))
handle_rep.GetProperty().SetColor(1.0, 0.0, 0.0)
handle_rep.GetProperty().SetLineWidth(1.0)
handle_rep.GetSelectedProperty().SetColor(0.2, 0.0, 1.0)

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(handle_rep)
handle_widget.EnableAxisConstraintOff()
handle_widget.EnabledOn()

# Scene
renderer.ResetCamera()
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
