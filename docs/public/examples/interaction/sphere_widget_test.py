#!/usr/bin/env python
# Demonstrate vtkSphereWidget2 controlling a light position on terrain data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import (
    vtkElevationFilter,
    vtkPolyDataNormals,
)
from vtkmodules.vtkFiltersGeneral import vtkWarpScalar
from vtkmodules.vtkFiltersGeometry import vtkImageDataGeometryFilter
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkInteractionWidgets import (
    vtkSphereRepresentation,
    vtkSphereWidget2,
)
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Source
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

scale = 2
elevation_lut = vtkLookupTable()
elevation_lut.SetHueRange(0.6, 0)
elevation_lut.SetSaturationRange(1.0, 0)
elevation_lut.SetValueRange(0.5, 1.0)
lo = scale * dem_reader.GetElevationBounds()[0]
hi = scale * dem_reader.GetElevationBounds()[1]

# Filters
shrink_filter = vtkImageShrink3D()
shrink_filter.SetShrinkFactors(4, 4, 1)
shrink_filter.SetInputConnection(dem_reader.GetOutputPort())
shrink_filter.AveragingOn()

geometry_filter = vtkImageDataGeometryFilter()
geometry_filter.SetInputConnection(shrink_filter.GetOutputPort())
geometry_filter.ReleaseDataFlagOn()

warp = vtkWarpScalar()
warp.SetInputConnection(geometry_filter.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.UseNormalOn()
warp.SetScaleFactor(scale)
warp.ReleaseDataFlagOn()

elevation = vtkElevationFilter()
elevation.SetInputConnection(warp.GetOutputPort())
elevation.SetLowPoint(0, 0, lo)
elevation.SetHighPoint(0, 0, hi)
elevation.SetScalarRange(lo, hi)
elevation.ReleaseDataFlagOn()

normals = vtkPolyDataNormals()
normals.SetInputConnection(elevation.GetOutputPort())
normals.SetFeatureAngle(60)
normals.ConsistencyOff()
normals.SplittingOff()
normals.ReleaseDataFlagOn()
normals.Update()

# Mapper + Actor
dem_mapper = vtkPolyDataMapper()
dem_mapper.SetInputConnection(normals.GetOutputPort())
dem_mapper.SetScalarRange(lo, hi)
dem_mapper.SetLookupTable(elevation_lut)

dem_actor = vtkActor()
dem_actor.SetMapper(dem_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dem_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("sphere widget test")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.LightFollowCameraOff()


# Callback to move light to sphere handle position
def move_light(widget, event_string):
    light.SetPosition(sphere_rep.GetHandlePosition())


# Widget
sphere_rep = vtkSphereRepresentation()
sphere_rep.SetPlaceFactor(4)
sphere_rep.PlaceWidget(normals.GetOutput().GetBounds())
sphere_rep.HandleVisibilityOn()
sphere_rep.SetRepresentationToWireframe()

sphere_widget = vtkSphereWidget2()
sphere_widget.SetInteractor(interactor)
sphere_widget.SetRepresentation(sphere_rep)
sphere_widget.AddObserver("InteractionEvent", move_light)

# Scene
camera = renderer.GetActiveCamera()
camera.SetViewUp(0, 0, 1)
camera.SetFocalPoint(dem_reader.GetOutput().GetCenter())
camera.SetPosition(1, 0, 0)
renderer.ResetCamera()
camera.Elevation(25)
camera.Azimuth(125)
camera.Zoom(1.25)
renderer.ResetCameraClippingRange()

# Add a light controlled by the sphere widget
light = vtkLight()
light.SetFocalPoint(sphere_rep.GetCenter())
light.SetPosition(sphere_rep.GetHandlePosition())
renderer.AddLight(light)

interactor.Initialize()
interactor.Start()
