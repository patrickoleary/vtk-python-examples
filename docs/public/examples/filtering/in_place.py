#!/usr/bin/env python

# Demonstrate in-place filtering with vtkImageCursor3D on magnified SLC data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkImageAppend
from vtkmodules.vtkIOImage import vtkSLCReader
from vtkmodules.vtkImagingCore import vtkImageMagnify
from vtkmodules.vtkImagingHybrid import vtkImageCursor3D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Constants
cursor_x = 20
cursor_y = 20
cursor_z = 20
image_mag_x = 2
image_mag_y = 2
image_mag_z = 1

# Pipeline
reader = vtkSLCReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "nut.slc"))

# Magnify
magnify1 = vtkImageMagnify()
magnify1.SetInputConnection(reader.GetOutputPort())
magnify1.SetMagnificationFactors(image_mag_x, image_mag_y, image_mag_z)
magnify1.ReleaseDataFlagOn()

magnify2 = vtkImageMagnify()
magnify2.SetInputConnection(reader.GetOutputPort())
magnify2.SetMagnificationFactors(image_mag_x, image_mag_y, image_mag_z)
magnify2.ReleaseDataFlagOn()

# In-place cursor filter
cursor = vtkImageCursor3D()
cursor.SetInputConnection(magnify1.GetOutputPort())
cursor.SetCursorPosition(cursor_x * image_mag_x,
                          cursor_y * image_mag_y,
                          cursor_z * image_mag_z)
cursor.SetCursorValue(255)
cursor.SetCursorRadius(50 * image_mag_x)

# Append side by side
image_append = vtkImageAppend()
image_append.SetAppendAxis(0)
image_append.AddInputConnection(magnify2.GetOutputPort())
image_append.AddInputConnection(cursor.GetOutputPort())
image_append.Update()

# Display with vtkImageActor - show the slice at cursor_z
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_append.GetOutputPort())
ext = image_append.GetOutput().GetExtent()
z_slice = cursor_z * image_mag_z
image_actor.SetDisplayExtent(ext[0], ext[1], ext[2], ext[3], z_slice, z_slice)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 256)
render_window.SetWindowName("in place")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
