#!/usr/bin/env python

# Butterworth high-pass filter applied to an image in frequency domain.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingFourier import (
    vtkImageButterworthHighPass,
    vtkImageFFT,
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
fft.SetDimensionality(2)
fft.SetInputConnection(reader.GetOutputPort())

# Butterworth high-pass filter
high_pass = vtkImageButterworthHighPass()
high_pass.SetInputConnection(fft.GetOutputPort())
high_pass.SetOrder(2)
high_pass.SetXCutOff(0.2)
high_pass.SetYCutOff(0.1)
high_pass.ReleaseDataFlagOff()
high_pass.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(high_pass.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("butterworth high pass")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
