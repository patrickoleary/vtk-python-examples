#!/usr/bin/env python
# Demonstrate vtkImageOrthoPlanes with three vtkImagePlaneWidgets on medical volume data.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkInteractionWidgets import vtkImageOrthoPlanes, vtkImagePlaneWidget
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: volume data
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
file_prefix = os.path.join(data_dir, "headsq", "quarter")

volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetFilePrefix(file_prefix)
volume_reader.SetDataMask(0x7FFF)
volume_reader.Update()

# Filter
outline = vtkOutlineFilter()
outline.SetInputConnection(volume_reader.GetOutputPort())

# Mapper + Actor
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer (two viewports)
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.58333, 1)
renderer_0.AddActor(outline_actor)
renderer_0.SetBackground(0.1, 0.1, 0.2)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.58333, 0, 1, 1)
renderer_1.SetBackground(0.2, 0.1, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_0)
render_window.SetWindowName("ortho planes")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 350)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Cell picker for the image plane widgets
picker = vtkCellPicker()
picker.SetTolerance(0.005)

ipw_prop = vtkProperty()


# Callback to synchronize window/level across planes.
def window_level_callback(caller, event):
    window_level = caller.GetWindowLevel()
    if caller is plane_widget_x:
        plane_widget_y.SetWindowLevel(window_level[0], window_level[1], 1)
        plane_widget_z.SetWindowLevel(window_level[0], window_level[1], 1)
    elif caller is plane_widget_y:
        plane_widget_x.SetWindowLevel(window_level[0], window_level[1], 1)
        plane_widget_z.SetWindowLevel(window_level[0], window_level[1], 1)
    elif caller is plane_widget_z:
        plane_widget_x.SetWindowLevel(window_level[0], window_level[1], 1)
        plane_widget_y.SetWindowLevel(window_level[0], window_level[1], 1)


# Widget: three image plane widgets (X, Y, Z)
plane_widget_x = vtkImagePlaneWidget()
plane_widget_x.SetInteractor(interactor)
plane_widget_x.SetKeyPressActivationValue("x")
plane_widget_x.SetPicker(picker)
plane_widget_x.RestrictPlaneToVolumeOn()
plane_widget_x.GetPlaneProperty().SetColor(1, 0, 0)
plane_widget_x.SetTexturePlaneProperty(ipw_prop)
plane_widget_x.TextureInterpolateOff()
plane_widget_x.SetResliceInterpolateToNearestNeighbour()
plane_widget_x.SetInputConnection(volume_reader.GetOutputPort())
plane_widget_x.SetPlaneOrientationToXAxes()
plane_widget_x.SetSliceIndex(32)
plane_widget_x.DisplayTextOn()
plane_widget_x.On()
plane_widget_x.InteractionOff()
plane_widget_x.InteractionOn()
plane_widget_x.AddObserver(vtkCommand.EndWindowLevelEvent, window_level_callback)

plane_widget_y = vtkImagePlaneWidget()
plane_widget_y.SetInteractor(interactor)
plane_widget_y.SetKeyPressActivationValue("y")
plane_widget_y.SetPicker(picker)
plane_widget_y.GetPlaneProperty().SetColor(1, 1, 0)
plane_widget_y.SetTexturePlaneProperty(ipw_prop)
plane_widget_y.TextureInterpolateOn()
plane_widget_y.SetResliceInterpolateToLinear()
plane_widget_y.SetInputConnection(volume_reader.GetOutputPort())
plane_widget_y.SetPlaneOrientationToYAxes()
plane_widget_y.SetSlicePosition(102.4)
plane_widget_y.SetLookupTable(plane_widget_x.GetLookupTable())
plane_widget_y.DisplayTextOff()
plane_widget_y.UpdatePlacement()
plane_widget_y.On()
plane_widget_y.AddObserver(vtkCommand.EndWindowLevelEvent, window_level_callback)

plane_widget_z = vtkImagePlaneWidget()
plane_widget_z.SetInteractor(interactor)
plane_widget_z.SetKeyPressActivationValue("z")
plane_widget_z.SetPicker(picker)
plane_widget_z.GetPlaneProperty().SetColor(0, 0, 1)
plane_widget_z.SetTexturePlaneProperty(ipw_prop)
plane_widget_z.TextureInterpolateOn()
plane_widget_z.SetResliceInterpolateToCubic()
plane_widget_z.SetInputConnection(volume_reader.GetOutputPort())
plane_widget_z.SetPlaneOrientationToZAxes()
plane_widget_z.SetSliceIndex(25)
plane_widget_z.SetLookupTable(plane_widget_x.GetLookupTable())
plane_widget_z.DisplayTextOn()
plane_widget_z.On()
plane_widget_z.AddObserver(vtkCommand.EndWindowLevelEvent, window_level_callback)

# Set up orthogonal planes
ortho_planes = vtkImageOrthoPlanes()
ortho_planes.SetPlane(0, plane_widget_x)
ortho_planes.SetPlane(1, plane_widget_y)
ortho_planes.SetPlane(2, plane_widget_z)
ortho_planes.ResetPlanes()

# 2D image from the Z reslice output
color_map = vtkImageMapToColors()
color_map.PassAlphaToOutputOff()
color_map.SetActiveComponent(0)
color_map.SetOutputFormatToLuminance()
color_map.SetInputData(plane_widget_z.GetResliceOutput())
color_map.SetLookupTable(plane_widget_x.GetLookupTable())

image_actor = vtkImageActor()
image_actor.PickableOff()
image_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
renderer_1.AddActor(image_actor)

# Scene
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Elevation(110)
renderer_0.GetActiveCamera().SetViewUp(0, 0, -1)
renderer_0.GetActiveCamera().Azimuth(45)
renderer_0.GetActiveCamera().Dolly(1.15)
renderer_0.ResetCameraClippingRange()

renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
