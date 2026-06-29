#!/usr/bin/env python

# Test that vtkMapper does not corrupt shared LookupTable alpha with ImagePlaneWidget.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkLookupTable,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
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

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Load volume data
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

x_min, x_max, y_min, y_max, z_min, z_max = v16.GetExecutive().GetWholeExtent(v16.GetOutputInformation(0))
img_data = v16.GetOutput()
spacing = img_data.GetSpacing()
sx, sy, sz = spacing
origin = img_data.GetOrigin()
ox, oy, oz = origin

# Outline
outline = vtkOutlineFilter()
outline.SetInputData(img_data)

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)

# Shared picker
picker = vtkCellPicker()
picker.SetTolerance(0.005)

# Image plane widgets
plane_widget_x = vtkImagePlaneWidget()
plane_widget_x.DisplayTextOn()
plane_widget_x.SetInputData(img_data)
plane_widget_x.SetPlaneOrientationToXAxes()
plane_widget_x.SetSliceIndex(32)
plane_widget_x.SetPicker(picker)
plane_widget_x.SetKeyPressActivationValue("x")
prop_1 = plane_widget_x.GetPlaneProperty()
prop_1.SetColor(1, 0, 0)

plane_widget_y = vtkImagePlaneWidget()
plane_widget_y.DisplayTextOn()
plane_widget_y.SetInputData(img_data)
plane_widget_y.SetPlaneOrientationToYAxes()
plane_widget_y.SetSliceIndex(32)
plane_widget_y.SetPicker(picker)
plane_widget_y.SetKeyPressActivationValue("y")
prop_2 = plane_widget_y.GetPlaneProperty()
prop_2.SetColor(1, 1, 0)
plane_widget_y.SetLookupTable(plane_widget_x.GetLookupTable())

plane_widget_z = vtkImagePlaneWidget()
plane_widget_z.DisplayTextOn()
plane_widget_z.SetInputData(img_data)
plane_widget_z.SetPlaneOrientationToZAxes()
plane_widget_z.SetSliceIndex(46)
plane_widget_z.SetPicker(picker)
plane_widget_z.SetKeyPressActivationValue("z")
prop_3 = plane_widget_z.GetPlaneProperty()
prop_3.SetColor(0, 0, 1)
plane_widget_z.SetLookupTable(plane_widget_x.GetLookupTable())

# Dummy actor sharing widget LUT with different opacity
dummy_pd = vtkPolyData()
dummy_pts = vtkPoints()
dummy_pts.InsertNextPoint((0, 0, 0))
dummy_scalars = vtkFloatArray()
dummy_scalars.InsertNextValue(1.0)
dummy_pd.SetPoints(dummy_pts)
dummy_pd.GetPointData().SetScalars(dummy_scalars)

dummy_mapper = vtkPolyDataMapper()
dummy_mapper.SetInputData(dummy_pd)
dummy_mapper.SetLookupTable(plane_widget_x.GetLookupTable())
dummy_mapper.UseLookupTableScalarRangeOn()

dummy_actor = vtkActor()
dummy_actor.SetMapper(dummy_mapper)
dummy_actor.GetProperty().SetOpacity(0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(dummy_actor)
renderer.AddActor(outline_actor)
renderer.SetBackground(0.1, 0.1, 0.2)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("mapper lut")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

plane_widget_x.SetInteractor(interactor)
plane_widget_x.On()
plane_widget_y.SetInteractor(interactor)
plane_widget_y.On()
plane_widget_z.SetInteractor(interactor)
plane_widget_z.On()

# Scene
renderer.ResetCamera()
cam_1 = renderer.GetActiveCamera()
cam_1.Elevation(110)
cam_1.SetViewUp(0, 0, -1)
cam_1.Azimuth(45)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
