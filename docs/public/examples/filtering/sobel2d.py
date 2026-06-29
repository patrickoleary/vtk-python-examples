#!/usr/bin/env python

# Apply 2D Sobel edge detection to a DICOM medical image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkDICOMImageReader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageSobel2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkDICOMImageReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "mr.001"))

# Sobel 2D
sobel = vtkImageSobel2D()
sobel.SetInputConnection(reader.GetOutputPort())
sobel.ReleaseDataFlagOff()
sobel.Update()

# Scale Sobel output to visible range
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(sobel.GetOutputPort())
shift_scale.SetShift(0)
shift_scale.SetScale(5)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("sobel2d")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
