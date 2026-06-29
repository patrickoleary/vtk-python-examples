#!/usr/bin/env python
# Demonstrate vtkmWarpScalar with three modes: XY plane, data normal, and custom normal.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmWarpScalar
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB).
brown_rgb = (0.5, 0.4, 0.3)
green_rgb = (0.0, 0.7, 0.2)
purple_rgb = (0.3, 0.2, 0.5)

# --- Viewport 0: XY plane warp ---
xy_source = vtkRTAnalyticSource()
xy_source.SetWholeExtent(-100, 100, -100, 100, 1, 1)
xy_source.SetCenter(0, 0, 0)
xy_source.SetMaximum(255)
xy_source.SetStandardDeviation(0.5)
xy_source.SetXFreq(60)
xy_source.SetYFreq(30)
xy_source.SetZFreq(40)
xy_source.SetXMag(10)
xy_source.SetYMag(18)
xy_source.SetZMag(5)
xy_source.SetSubsampleRate(1)

xy_warp_scalar = vtkmWarpScalar()
xy_warp_scalar.SetScaleFactor(2)
xy_warp_scalar.XYPlaneOn()
xy_warp_scalar.SetNormal(1, 0, 0)  # should be ignored
xy_warp_scalar.SetInputConnection(xy_source.GetOutputPort())

xy_mapper = vtkDataSetMapper()
xy_mapper.SetInputConnection(xy_warp_scalar.GetOutputPort())

xy_actor = vtkActor()
xy_actor.SetMapper(xy_mapper)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.33, 1.0)
renderer_0.SetBackground(brown_rgb)
renderer_0.AddActor(xy_actor)

# --- Viewport 1: Data normal warp ---
data_normal_source = vtkSphereSource()
data_normal_source.SetRadius(100)
data_normal_source.SetThetaResolution(20)
data_normal_source.SetPhiResolution(20)
data_normal_source.Update()
data_normal_output = data_normal_source.GetOutput()

# Create scalar array.
scalar_array = vtkFloatArray()
scalar_array.SetName("scalarfactor")
scalar_array.SetNumberOfValues(data_normal_output.GetNumberOfPoints())
for i in range(data_normal_output.GetNumberOfPoints()):
    scalar_array.SetValue(i, 2)
data_normal_output.GetPointData().AddArray(scalar_array)

data_normal_warp_scalar = vtkmWarpScalar()
data_normal_warp_scalar.SetScaleFactor(2)
data_normal_warp_scalar.SetInputData(data_normal_source.GetOutput())
data_normal_warp_scalar.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "scalarfactor"
)

data_normal_mapper = vtkDataSetMapper()
data_normal_mapper.SetInputConnection(data_normal_warp_scalar.GetOutputPort())

data_normal_actor = vtkActor()
data_normal_actor.SetMapper(data_normal_mapper)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0.0, 0.66, 1.0)
renderer_1.SetBackground(green_rgb)
renderer_1.AddActor(data_normal_actor)

# --- Viewport 2: Custom normal warp ---
custom_normal_source = vtkRTAnalyticSource()
custom_normal_source.SetWholeExtent(-100, 100, -100, 100, 1, 1)
custom_normal_source.SetCenter(0, 0, 0)
custom_normal_source.SetMaximum(255)
custom_normal_source.SetStandardDeviation(0.5)
custom_normal_source.SetXFreq(60)
custom_normal_source.SetYFreq(30)
custom_normal_source.SetZFreq(40)
custom_normal_source.SetXMag(10)
custom_normal_source.SetYMag(18)
custom_normal_source.SetZMag(5)
custom_normal_source.SetSubsampleRate(1)

custom_normal_warp_scalar = vtkmWarpScalar()
custom_normal_warp_scalar.SetScaleFactor(2)
custom_normal_warp_scalar.SetNormal(0.333, 0.333, 0.333)
custom_normal_warp_scalar.SetInputConnection(custom_normal_source.GetOutputPort())

custom_normal_mapper = vtkDataSetMapper()
custom_normal_mapper.SetInputConnection(custom_normal_warp_scalar.GetOutputPort())

custom_normal_actor = vtkActor()
custom_normal_actor.SetMapper(custom_normal_mapper)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.66, 0.0, 1.0, 1.0)
renderer_2.SetBackground(purple_rgb)
renderer_2.AddActor(custom_normal_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(900, 300)
render_window.SetWindowName("vtkm warp scalar")
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()
renderer_2.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
