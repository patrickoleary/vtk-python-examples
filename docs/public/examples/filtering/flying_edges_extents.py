#!/usr/bin/env python

# Test vtkFlyingEdges3D with negative extents and vtkFlyingEdges2D on a
# resliced plane, displayed in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges2D,
    vtkFlyingEdges3D,
    vtkTubeFilter,
)
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import (
    vtkImageReslice,
    vtkRTAnalyticSource,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 100

# --- Left viewport: negative-extent wavelet iso-surface ---

# Source: wavelet with negative extents
source = vtkRTAnalyticSource()

iso = vtkFlyingEdges3D()
iso.SetInputConnection(source.GetOutputPort())
iso.SetValue(0, 150)

iso_mapper = vtkPolyDataMapper()
iso_mapper.SetInputConnection(iso.GetOutputPort())
iso_mapper.ScalarVisibilityOff()

iso_actor = vtkActor()
iso_actor.SetMapper(iso_mapper)
iso_actor.GetProperty().SetColor(1, 1, 1)
iso_actor.GetProperty().SetOpacity(1)

outline = vtkOutlineFilter()
outline.SetInputConnection(source.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# --- Right viewport: plane contour + 2D reslice contour ---

# Sample a plane function
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(0, 1, 0)

sample = vtkSampleFunction()
sample.SetImplicitFunction(plane)
sample.SetModelBounds(-10, 10, -10, 10, -10, 10)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.SetOutputScalarTypeToFloat()
sample.Update()

# 3D contour of the plane
iso_2 = vtkFlyingEdges3D()
iso_2.SetInputConnection(sample.GetOutputPort())
iso_2.SetValue(0, 0.0)

iso_2_mapper = vtkPolyDataMapper()
iso_2_mapper.SetInputConnection(iso_2.GetOutputPort())
iso_2_mapper.ScalarVisibilityOff()

iso_2_actor = vtkActor()
iso_2_actor.SetMapper(iso_2_mapper)
iso_2_actor.GetProperty().SetColor(1, 1, 1)
iso_2_actor.GetProperty().SetOpacity(1)

outline_2 = vtkOutlineFilter()
outline_2.SetInputConnection(sample.GetOutputPort())

outline_2_mapper = vtkPolyDataMapper()
outline_2_mapper.SetInputConnection(outline_2.GetOutputPort())

outline_2_actor = vtkActor()
outline_2_actor.SetMapper(outline_2_mapper)

# 2D reslice + contour with tube rendering
center = [0.0, 0.0, 0.0]
axial = vtkMatrix4x4()
axial.DeepCopy((1, 0, 0, center[0],
                0, 1, 0, center[1],
                0, 0, 1, center[2],
                0, 0, 0, 1))

reslice = vtkImageReslice()
reslice.SetInputConnection(sample.GetOutputPort())
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxes(axial)
reslice.SetInterpolationModeToLinear()

iso_3 = vtkFlyingEdges2D()
iso_3.SetInputConnection(reslice.GetOutputPort())
iso_3.SetValue(0, 0.0)

tube = vtkTubeFilter()
tube.SetInputConnection(iso_3.GetOutputPort())
tube.SetRadius(0.25)

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube.GetOutputPort())

tube_actor = vtkActor()
tube_actor.SetMapper(tube_mapper)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(outline_actor)
renderer_0.AddActor(iso_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(outline_2_actor)
renderer_1.AddActor(iso_2_actor)
renderer_1.AddActor(tube_actor)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(600, 300)
render_window.SetWindowName("flying edges extents")

# Scene
renderer_0.ResetCamera()
camera_1 = vtkCamera()
camera_1.SetPosition(0, 1, 0)
camera_1.SetFocalPoint(0, 0, 0)
camera_1.SetViewUp(0, 0, 1)
renderer_1.SetActiveCamera(camera_1)
renderer_1.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
