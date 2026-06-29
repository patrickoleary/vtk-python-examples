#!/usr/bin/env python

# Demonstrate a 3D cursor in a volume rendering with axes and outline.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingVolumeOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkFiltersGeneral import vtkAxes
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkImagingCore import vtkImageMagnify
from vtkmodules.vtkImagingHybrid import vtkImageCursor3D
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkFixedPointVolumeRayCastMapper

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Global cursor and magnification values
CURSOR_X = 20
CURSOR_Y = 20
CURSOR_Z = 20
IMAGE_MAG_X = 4
IMAGE_MAG_Y = 4
IMAGE_MAG_Z = 1

# Read SLC volume data
reader = vtkSLCReader()
reader.SetFileName(os.path.join(data_dir, "neghip.slc"))

# Magnify and add 3D cursor overlay
magnify = vtkImageMagnify()
magnify.SetInputConnection(reader.GetOutputPort())
magnify.SetMagnificationFactors(IMAGE_MAG_X, IMAGE_MAG_Y, IMAGE_MAG_Z)

image_cursor = vtkImageCursor3D()
image_cursor.SetInputConnection(magnify.GetOutputPort())
image_cursor.SetCursorPosition(
    CURSOR_X * IMAGE_MAG_X, CURSOR_Y * IMAGE_MAG_Y, CURSOR_Z * IMAGE_MAG_Z
)
image_cursor.SetCursorValue(255)
image_cursor.SetCursorRadius(50 * IMAGE_MAG_X)

# Axes at cursor position
axes = vtkAxes()
axes.SymmetricOn()
axes.SetOrigin(CURSOR_X, CURSOR_Y, CURSOR_Z)
axes.SetScaleFactor(50.0)

axes_mapper = vtkPolyDataMapper()
axes_mapper.SetInputConnection(axes.GetOutputPort())

axes_actor = vtkActor()
axes_actor.SetMapper(axes_mapper)
axes_actor.GetProperty().SetAmbient(0.5)

# Image slice display using vtkImageActor (not vtkImageViewer)
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_cursor.GetOutputPort())
image_actor.SetDisplayExtent(0, 0, 0, 0, CURSOR_Z * IMAGE_MAG_Z, CURSOR_Z * IMAGE_MAG_Z)

# Opacity and color transfer functions for volume
opacity_transfer_function = vtkPiecewiseFunction()
opacity_transfer_function.AddPoint(20, 0.0)
opacity_transfer_function.AddPoint(255, 0.2)

color_transfer_function = vtkColorTransferFunction()
color_transfer_function.AddRGBPoint(0, 0, 0, 0)
color_transfer_function.AddRGBPoint(64, 1, 0, 0)
color_transfer_function.AddRGBPoint(128, 0, 0, 1)
color_transfer_function.AddRGBPoint(192, 0, 1, 0)
color_transfer_function.AddRGBPoint(255, 0, 0.2, 0)

# Volume property
volume_property = vtkVolumeProperty()
volume_property.SetColor(color_transfer_function)
volume_property.SetScalarOpacity(opacity_transfer_function)

# Volume mapper and volume
volume_mapper = vtkFixedPointVolumeRayCastMapper()
volume_mapper.SetInputConnection(reader.GetOutputPort())

volume = vtkVolume()
volume.SetMapper(volume_mapper)
volume.SetProperty(volume_property)

# Outline
outline = vtkOutlineFilter()
outline.SetInputConnection(reader.GetOutputPort())

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(1, 1, 1)

# Image renderer
image_renderer = vtkRenderer()
image_renderer.AddActor(image_actor)
image_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)

# 3D renderer
renderer = vtkRenderer()
renderer.AddActor(axes_actor)
renderer.AddVolume(volume)
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.SetViewport(0.5, 0.0, 1.0, 1.0)

render_window = vtkRenderWindow()
render_window.SetSize(512, 256)
render_window.AddRenderer(image_renderer)
render_window.AddRenderer(renderer)
render_window.SetWindowName("cursor3d")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
image_renderer.GetActiveCamera().ParallelProjectionOn()
image_renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
