#!/usr/bin/env python
# Demonstrate vtkImagePlaneWidget with oriented image data using a rotation matrix.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math
import os

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersModeling import vtkImageDataOutlineFilter
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkInteractionWidgets import vtkImagePlaneWidget
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCellPicker,
    vtkImageActor,
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
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.SetDataMask(0x7FFF)
volume_reader.Update()

straight_data = volume_reader.GetOutput()

# Create oriented data by rotating original data by pi/5
oriented_data = vtkImageData()
oriented_data.DeepCopy(straight_data)
angle = math.pi / 5
cos_a = math.cos(angle)
sin_a = math.sin(angle)
oriented_data.SetDirectionMatrix(cos_a, -sin_a, 0, sin_a, cos_a, 0, 0, 0, 1)


# Helper: add image outline to a renderer
def add_image_outline(image, target_renderer, color):
    outline_filter = vtkImageDataOutlineFilter()
    outline_filter.SetInputData(image)
    outline_mapper = vtkPolyDataMapper()
    outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
    outline_actor = vtkActor()
    outline_actor.SetMapper(outline_mapper)
    outline_actor.GetProperty().SetColor(color)
    target_renderer.AddActor(outline_actor)


# Helper: set up a plane widget
def setup_plane_widget(plane_widget, iren, volume_input):
    plane_picker = vtkCellPicker()
    plane_picker.SetTolerance(0.005)
    plane_widget.SetInteractor(iren)
    plane_widget.SetPicker(plane_picker)
    plane_widget.SetInputData(volume_input)
    plane_widget.SetPlaneOrientationToXAxes()
    plane_widget.SetSliceIndex(42)
    plane_widget.On()


# Helper: add reslice output to a renderer
def add_reslice_output(plane_widget, target_renderer):
    color_map = vtkImageMapToColors()
    color_map.PassAlphaToOutputOff()
    color_map.SetActiveComponent(0)
    color_map.SetOutputFormatToLuminance()
    color_map.SetInputData(plane_widget.GetResliceOutput())
    color_map.SetLookupTable(plane_widget.GetLookupTable())
    reslice_actor = vtkImageActor()
    reslice_actor.PickableOff()
    reslice_actor.GetMapper().SetInputConnection(color_map.GetOutputPort())
    target_renderer.AddActor(reslice_actor)


# Renderers
scene_renderer = vtkRenderer()
scene_renderer.SetViewport(0, 0, 0.5, 1)
scene_renderer.SetBackground(0.4, 0.4, 0.8)

straight_slice_renderer = vtkRenderer()
straight_slice_renderer.SetViewport(0.5, 0, 1, 0.5)
straight_slice_renderer.SetBackground(0.8, 0.4, 0.8)

oriented_slice_renderer = vtkRenderer()
oriented_slice_renderer.SetViewport(0.5, 0.5, 1, 1)
oriented_slice_renderer.SetBackground(0.4, 0.8, 0.8)

# Add outlines to the 3D scene renderer
add_image_outline(straight_data, scene_renderer, (0.5, 0.5, 0.5))
add_image_outline(oriented_data, scene_renderer, (1.0, 1.0, 0.0))

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(scene_renderer)
render_window.AddRenderer(straight_slice_renderer)
render_window.AddRenderer(oriented_slice_renderer)
render_window.SetWindowName("image plane widget oriented")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 350)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widgets: plane widgets for oriented and straight data
oriented_plane_widget = vtkImagePlaneWidget()
setup_plane_widget(oriented_plane_widget, interactor, oriented_data)
add_reslice_output(oriented_plane_widget, oriented_slice_renderer)

straight_plane_widget = vtkImagePlaneWidget()
setup_plane_widget(straight_plane_widget, interactor, straight_data)
add_reslice_output(straight_plane_widget, straight_slice_renderer)

# Scene
scene_renderer.ResetCamera()
scene_renderer.GetActiveCamera().Elevation(110)
scene_renderer.GetActiveCamera().SetViewUp(0, 0, -1)
scene_renderer.GetActiveCamera().Azimuth(45)
scene_renderer.GetActiveCamera().Dolly(1.15)
scene_renderer.ResetCameraClippingRange()
oriented_slice_renderer.ResetCamera()
straight_slice_renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
