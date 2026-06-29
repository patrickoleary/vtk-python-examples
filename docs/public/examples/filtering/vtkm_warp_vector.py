#!/usr/bin/env python
# Demonstrate vtkmWarpVector with two modes: custom vector field and data normals.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmWarpVector
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

# --- Viewport 0: Custom vector field warp ---
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
xy_source.SetZMag(10)
xy_source.SetSubsampleRate(1)
xy_source.Update()

# Create a vector array pointing in Z direction.
xy_vector = vtkFloatArray()
xy_vector.SetNumberOfComponents(3)
xy_vector.SetName("scalarVector")
xy_vector.SetNumberOfTuples(xy_source.GetOutput().GetNumberOfPoints())
for i in range(xy_source.GetOutput().GetNumberOfPoints()):
    xy_vector.SetTuple3(i, 0.0, 0.0, 1.0)
xy_source.GetOutput().GetPointData().AddArray(xy_vector)

xy_warp_vector = vtkmWarpVector()
xy_warp_vector.SetScaleFactor(2)
xy_warp_vector.SetInputConnection(xy_source.GetOutputPort())
xy_warp_vector.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "scalarVector"
)
xy_warp_vector.Update()

xy_mapper = vtkDataSetMapper()
xy_mapper.SetInputConnection(xy_warp_vector.GetOutputPort())

xy_actor = vtkActor()
xy_actor.SetMapper(xy_mapper)

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.SetBackground(brown_rgb)
renderer_0.AddActor(xy_actor)

# --- Viewport 1: Data normal warp ---
data_normal_source = vtkSphereSource()
data_normal_source.SetRadius(100)
data_normal_source.SetThetaResolution(20)
data_normal_source.SetPhiResolution(20)
data_normal_source.Update()
data_normal_output = data_normal_source.GetOutput()

data_normal_warp_vector = vtkmWarpVector()
data_normal_warp_vector.SetScaleFactor(5)
data_normal_warp_vector.SetInputData(data_normal_source.GetOutput())
data_normal_warp_vector.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.POINT,
    data_normal_output.GetPointData().GetNormals().GetName(),
)

data_normal_mapper = vtkDataSetMapper()
data_normal_mapper.SetInputConnection(data_normal_warp_vector.GetOutputPort())

data_normal_actor = vtkActor()
data_normal_actor.SetMapper(data_normal_mapper)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.SetBackground(green_rgb)
renderer_1.AddActor(data_normal_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("vtkm warp vector")
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
