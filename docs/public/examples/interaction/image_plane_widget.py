#!/usr/bin/env python
# Demonstrate vtkImagePlaneWidget with three orthogonal planes on volume data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkInteractionWidgets import vtkImagePlaneWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.Update()

x_min, x_max, y_min, y_max, z_min, z_max = volume_reader.GetExecutive().GetWholeExtent(
    volume_reader.GetOutputInformation(0)
)
img_data = volume_reader.GetOutput()

# Create a copy of the image data to demonstrate that
# vtkImagePlaneWidget works correctly with user-created vtkImageData
my_img_data = vtkImageData()
my_img_data.SetDimensions(img_data.GetDimensions())
my_img_data.SetExtent(img_data.GetExtent())
my_img_data.SetSpacing(img_data.GetSpacing())
my_img_data.SetOrigin(img_data.GetOrigin())
my_img_data.SetScalarType(img_data.GetScalarType(), my_img_data.GetInformation())
my_img_data.GetPointData().SetScalars(img_data.GetPointData().GetScalars())
img_data = my_img_data

# Filter + Mapper + Actor: outline
outline = vtkOutlineFilter()
outline.SetInputData(img_data)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.1, 0.2)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("image plane widget")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Shared picker for the three plane widgets
picker = vtkCellPicker()
picker.SetTolerance(0.005)

# Widget: X-axis image plane (red)
plane_widget_x = vtkImagePlaneWidget()
plane_widget_x.DisplayTextOn()
plane_widget_x.SetInputData(img_data)
plane_widget_x.SetPlaneOrientationToXAxes()
plane_widget_x.SetSliceIndex(32)
plane_widget_x.SetPicker(picker)
plane_widget_x.SetKeyPressActivationValue("x")
plane_widget_x.GetPlaneProperty().SetColor(1, 0, 0)
plane_widget_x.SetInteractor(interactor)
plane_widget_x.On()

# Widget: Y-axis image plane (yellow)
plane_widget_y = vtkImagePlaneWidget()
plane_widget_y.DisplayTextOn()
plane_widget_y.SetInputData(img_data)
plane_widget_y.SetPlaneOrientationToYAxes()
plane_widget_y.SetSliceIndex(32)
plane_widget_y.SetPicker(picker)
plane_widget_y.SetKeyPressActivationValue("y")
plane_widget_y.GetPlaneProperty().SetColor(1, 1, 0)
plane_widget_y.SetLookupTable(plane_widget_x.GetLookupTable())
plane_widget_y.SetInteractor(interactor)
plane_widget_y.On()

# Widget: Z-axis image plane (blue)
plane_widget_z = vtkImagePlaneWidget()
plane_widget_z.DisplayTextOn()
plane_widget_z.SetInputData(img_data)
plane_widget_z.SetPlaneOrientationToZAxes()
plane_widget_z.SetSliceIndex(46)
plane_widget_z.SetPicker(picker)
plane_widget_z.SetKeyPressActivationValue("z")
plane_widget_z.GetPlaneProperty().SetColor(0, 0, 1)
plane_widget_z.SetLookupTable(plane_widget_x.GetLookupTable())
plane_widget_z.SetInteractor(interactor)
plane_widget_z.On()

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Elevation(110)
camera.SetViewUp(0, 0, -1)
camera.Azimuth(45)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
