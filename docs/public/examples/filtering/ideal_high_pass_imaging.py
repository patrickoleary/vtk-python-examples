#!/usr/bin/env python

# Ideal high-pass filter applied to a medical image in the frequency domain.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageExtractComponents
from vtkmodules.vtkImagingFourier import (
    vtkImageFFT,
    vtkImageIdealHighPass,
    vtkImageRFFT,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Forward FFT
fft = vtkImageFFT()
fft.SetInputConnection(reader.GetOutputPort())

# High-pass filter
high_pass = vtkImageIdealHighPass()
high_pass.SetInputConnection(fft.GetOutputPort())
high_pass.SetXCutOff(0.1)
high_pass.SetYCutOff(0.1)
high_pass.ReleaseDataFlagOff()

# Inverse FFT
rfft = vtkImageRFFT()
rfft.SetInputConnection(high_pass.GetOutputPort())

# Extract real component
real = vtkImageExtractComponents()
real.SetInputConnection(rfft.GetOutputPort())
real.SetComponents(0)
real.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(real.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("ideal high pass imaging")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
