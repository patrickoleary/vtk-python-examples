#!/usr/bin/env python

# Test vtkCameraInterpolator with a DEM terrain flyover.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkCamera,
    vtkCameraInterpolator,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLOD import vtkLODActor

# Lookup table
lut = vtkLookupTable()
lut.SetHueRange(0.6, 0)
lut.SetSaturationRange(1.0, 0)
lut.SetValueRange(0.5, 1.0)

# Read DEM data
dem_reader = vtkDEMReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

lo = dem_reader.GetOutput().GetScalarRange()[0]
hi = dem_reader.GetOutput().GetScalarRange()[1]

# Surface pipeline
surface = vtkImageDataGeometryFilter()
surface.SetInputConnection(dem_reader.GetOutputPort())

warp = vtkWarpScalar()
warp.SetInputConnection(surface.GetOutputPort())
warp.SetScaleFactor(1)
warp.UseNormalOn()
warp.SetNormal(0, 0, 1)
warp.Update()

normals = vtkPolyDataNormals()
normals.SetInputData(warp.GetPolyDataOutput())
normals.SetFeatureAngle(60)
normals.SplittingOff()

dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(lut)

dem_actor = vtkLODActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("camera interpolator")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# Define camera keyframes
view_1 = vtkCamera()
view_1.SetClippingRange(30972.2, 35983.7)
view_1.SetFocalPoint(562835, 5.11498e+006, 2294.5)
view_1.SetPosition(562835, 5.11498e+006, 35449.9)
view_1.SetViewAngle(30)
view_1.SetViewUp(0, 1, 0)

view_2 = vtkCamera()
view_2.SetClippingRange(9013.43, 13470.4)
view_2.SetFocalPoint(562835, 5.11498e+006, 2294.5)
view_2.SetPosition(562835, 5.11498e+006, 13269.4)
view_2.SetViewAngle(30)
view_2.SetViewUp(0, 1, 0)

view_3 = vtkCamera()
view_3.SetClippingRange(4081.2, 13866.4)
view_3.SetFocalPoint(562853, 5.11586e+006, 2450.05)
view_3.SetPosition(562853, 5.1144e+006, 10726.6)
view_3.SetViewAngle(30)
view_3.SetViewUp(0, 0.984808, 0.173648)

view_4 = vtkCamera()
view_4.SetClippingRange(14.0481, 14048.1)
view_4.SetFocalPoint(562880, 5.11652e+006, 2733.15)
view_4.SetPosition(562974, 5.11462e+006, 6419.98)
view_4.SetViewAngle(30)
view_4.SetViewUp(0.0047047, 0.888364, 0.459116)

view_5 = vtkCamera()
view_5.SetClippingRange(14.411, 14411)
view_5.SetFocalPoint(562910, 5.11674e+006, 3027.15)
view_5.SetPosition(562414, 5.11568e+006, 3419.87)
view_5.SetViewAngle(30)
view_5.SetViewUp(-0.0301976, 0.359864, 0.932516)

# Camera interpolator
interpolator = vtkCameraInterpolator()
interpolator.SetInterpolationTypeToSpline()
interpolator.AddCamera(0, view_1)
interpolator.AddCamera(5, view_2)
interpolator.AddCamera(7.5, view_3)
interpolator.AddCamera(9.0, view_4)
interpolator.AddCamera(11.0, view_5)

camera = vtkCamera()
renderer.SetActiveCamera(camera)

# Interpolate to a specific time
interpolator.InterpolateCamera(8.2, camera)

interactor.Initialize()
interactor.Start()
