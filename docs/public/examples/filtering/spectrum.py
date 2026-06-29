#!/usr/bin/env python

# Display a compressed spectrum of a medical image using FFT and log scale.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingFourier import (
    vtkImageFFT,
    vtkImageFourierCenter,
)
from vtkmodules.vtkImagingMath import (
    vtkImageLogarithmicScale,
    vtkImageMagnitude,
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
fft.ReleaseDataFlagOff()

# Magnitude
magnitude = vtkImageMagnitude()
magnitude.SetInputConnection(fft.GetOutputPort())
magnitude.ReleaseDataFlagOff()

# Center the spectrum
center = vtkImageFourierCenter()
center.SetInputConnection(magnitude.GetOutputPort())

# Log scale compression
compress = vtkImageLogarithmicScale()
compress.SetInputConnection(center.GetOutputPort())
compress.SetConstant(15)
compress.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(compress.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("spectrum")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
