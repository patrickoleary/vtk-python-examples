#!/usr/bin/env python

# Visualize skin isosurfaces from CT head data with six different slice
# orderings (ap, pa, si, is, lr, rl), each rendered with a distinct color.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Data directory
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Slice order transforms (inlined from SliceOrder module)
si_transform = vtkTransform()
si_transform.SetMatrix([1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1])

iss_transform = vtkTransform()
iss_transform.SetMatrix([1, 0, 0, 0, 0, 0, -1, 0, 0, -1, 0, 0, 0, 0, 0, 1])

ap_transform = vtkTransform()
ap_transform.Scale(1, -1, 1)

pa_transform = vtkTransform()
pa_transform.Scale(1, -1, -1)

lr_transform = vtkTransform()
lr_transform.SetMatrix([0, 0, -1, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1])

rl_transform = vtkTransform()
rl_transform.SetMatrix([0, 0, 1, 0, 0, -1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1])

# Parameters
RESOLUTION = 64
START_SLICE = 50
END_SLICE = 60
PIXEL_SIZE = 3.2
origin = (RESOLUTION / 2.0) * PIXEL_SIZE * -1.0

# AP reader/contour/mapper/actor
ap_reader = vtkVolume16Reader()
ap_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
ap_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
ap_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
ap_reader.SetDataOrigin(origin, origin, 1.5)
ap_reader.SetImageRange(START_SLICE, END_SLICE)
ap_reader.SetTransform(ap_transform)
ap_reader.SetHeaderSize(0)
ap_reader.SetDataMask(0x7fff)
ap_reader.SetDataByteOrderToLittleEndian()
ap_reader.GetExecutive().SetReleaseDataFlag(0, 1)

ap_contour = vtkContourFilter()
ap_contour.SetInputConnection(ap_reader.GetOutputPort())
ap_contour.SetValue(0, 550.5)
ap_contour.ComputeScalarsOff()
ap_contour.ReleaseDataFlagOn()

ap_mapper = vtkPolyDataMapper()
ap_mapper.SetInputConnection(ap_contour.GetOutputPort())

ap_actor = vtkActor()
ap_actor.SetMapper(ap_mapper)
ap_actor.GetProperty().SetDiffuseColor(0.875950, 0.598302, 0.656878)

# PA reader/contour/mapper/actor
pa_reader = vtkVolume16Reader()
pa_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
pa_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
pa_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
pa_reader.SetDataOrigin(origin, origin, 1.5)
pa_reader.SetImageRange(START_SLICE, END_SLICE)
pa_reader.SetTransform(pa_transform)
pa_reader.SetHeaderSize(0)
pa_reader.SetDataMask(0x7fff)
pa_reader.SetDataByteOrderToLittleEndian()
pa_reader.GetExecutive().SetReleaseDataFlag(0, 1)

pa_contour = vtkContourFilter()
pa_contour.SetInputConnection(pa_reader.GetOutputPort())
pa_contour.SetValue(0, 550.5)
pa_contour.ComputeScalarsOff()
pa_contour.ReleaseDataFlagOn()

pa_mapper = vtkPolyDataMapper()
pa_mapper.SetInputConnection(pa_contour.GetOutputPort())

pa_actor = vtkActor()
pa_actor.SetMapper(pa_mapper)
pa_actor.GetProperty().SetDiffuseColor(0.641134, 0.536594, 0.537889)

# SI reader/contour/mapper/actor
si_reader = vtkVolume16Reader()
si_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
si_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
si_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
si_reader.SetDataOrigin(origin, origin, 1.5)
si_reader.SetImageRange(START_SLICE, END_SLICE)
si_reader.SetTransform(si_transform)
si_reader.SetHeaderSize(0)
si_reader.SetDataMask(0x7fff)
si_reader.SetDataByteOrderToLittleEndian()
si_reader.GetExecutive().SetReleaseDataFlag(0, 1)

si_contour = vtkContourFilter()
si_contour.SetInputConnection(si_reader.GetOutputPort())
si_contour.SetValue(0, 550.5)
si_contour.ComputeScalarsOff()
si_contour.ReleaseDataFlagOn()

si_mapper = vtkPolyDataMapper()
si_mapper.SetInputConnection(si_contour.GetOutputPort())

si_actor = vtkActor()
si_actor.SetMapper(si_mapper)
si_actor.GetProperty().SetDiffuseColor(0.804079, 0.650506, 0.558249)

# ISS reader/contour/mapper/actor
iss_reader = vtkVolume16Reader()
iss_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
iss_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
iss_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
iss_reader.SetDataOrigin(origin, origin, 1.5)
iss_reader.SetImageRange(START_SLICE, END_SLICE)
iss_reader.SetTransform(iss_transform)
iss_reader.SetHeaderSize(0)
iss_reader.SetDataMask(0x7fff)
iss_reader.SetDataByteOrderToLittleEndian()
iss_reader.GetExecutive().SetReleaseDataFlag(0, 1)

iss_contour = vtkContourFilter()
iss_contour.SetInputConnection(iss_reader.GetOutputPort())
iss_contour.SetValue(0, 550.5)
iss_contour.ComputeScalarsOff()
iss_contour.ReleaseDataFlagOn()

iss_mapper = vtkPolyDataMapper()
iss_mapper.SetInputConnection(iss_contour.GetOutputPort())

iss_actor = vtkActor()
iss_actor.SetMapper(iss_mapper)
iss_actor.GetProperty().SetDiffuseColor(0.992896, 0.603716, 0.660385)

# LR reader/contour/mapper/actor
lr_reader = vtkVolume16Reader()
lr_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
lr_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
lr_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
lr_reader.SetDataOrigin(origin, origin, 1.5)
lr_reader.SetImageRange(START_SLICE, END_SLICE)
lr_reader.SetTransform(lr_transform)
lr_reader.SetHeaderSize(0)
lr_reader.SetDataMask(0x7fff)
lr_reader.SetDataByteOrderToLittleEndian()
lr_reader.GetExecutive().SetReleaseDataFlag(0, 1)

lr_contour = vtkContourFilter()
lr_contour.SetInputConnection(lr_reader.GetOutputPort())
lr_contour.SetValue(0, 550.5)
lr_contour.ComputeScalarsOff()
lr_contour.ReleaseDataFlagOn()

lr_mapper = vtkPolyDataMapper()
lr_mapper.SetInputConnection(lr_contour.GetOutputPort())

lr_actor = vtkActor()
lr_actor.SetMapper(lr_mapper)
lr_actor.GetProperty().SetDiffuseColor(0.589101, 0.513448, 0.523095)

# RL reader/contour/mapper/actor
rl_reader = vtkVolume16Reader()
rl_reader.SetDataDimensions(RESOLUTION, RESOLUTION)
rl_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
rl_reader.SetDataSpacing(PIXEL_SIZE, PIXEL_SIZE, 1.5)
rl_reader.SetDataOrigin(origin, origin, 1.5)
rl_reader.SetImageRange(START_SLICE, END_SLICE)
rl_reader.SetTransform(rl_transform)
rl_reader.SetHeaderSize(0)
rl_reader.SetDataMask(0x7fff)
rl_reader.SetDataByteOrderToLittleEndian()
rl_reader.GetExecutive().SetReleaseDataFlag(0, 1)

rl_contour = vtkContourFilter()
rl_contour.SetInputConnection(rl_reader.GetOutputPort())
rl_contour.SetValue(0, 550.5)
rl_contour.ComputeScalarsOff()
rl_contour.ReleaseDataFlagOn()

rl_mapper = vtkPolyDataMapper()
rl_mapper.SetInputConnection(rl_contour.GetOutputPort())

rl_actor = vtkActor()
rl_actor.SetMapper(rl_mapper)
rl_actor.GetProperty().SetDiffuseColor(0.650247, 0.700527, 0.752458)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ap_actor)
renderer.AddActor(pa_actor)
renderer.AddActor(si_actor)
renderer.AddActor(iss_actor)
renderer.AddActor(lr_actor)
renderer.AddActor(rl_actor)
renderer.SetBackground(0.8, 0.8, 0.8)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("skin order")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(210)
renderer.GetActiveCamera().Elevation(30)
renderer.GetActiveCamera().Dolly(1.2)
renderer.ResetCameraClippingRange()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
