#!/usr/bin/env python

# Demonstrate image flip operations along X and Y axes using vtkImageFlip.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersCore import vtkImageAppend
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageFlip,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkImageReader()
reader.GetExecutive().SetReleaseDataFlag(0, 0)
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Cast to float
image_float = vtkImageCast()
image_float.SetInputConnection(reader.GetOutputPort())
image_float.SetOutputScalarTypeToFloat()

# Flip along X axis
flip_x = vtkImageFlip()
flip_x.SetInputConnection(image_float.GetOutputPort())
flip_x.SetFilteredAxis(0)

# Flip along Y axis with origin flip
flip_y = vtkImageFlip()
flip_y.SetInputConnection(image_float.GetOutputPort())
flip_y.SetFilteredAxis(1)
flip_y.FlipAboutOriginOn()

# Append original, flipX, flipY side by side
image_append = vtkImageAppend()
image_append.AddInputConnection(image_float.GetOutputPort())
image_append.AddInputConnection(flip_x.GetOutputPort())
image_append.AddInputConnection(flip_y.GetOutputPort())
image_append.SetAppendAxis(0)
image_append.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(image_append.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 256)
render_window.SetWindowName("all flips")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
