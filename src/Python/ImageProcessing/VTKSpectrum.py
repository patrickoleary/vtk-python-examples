#!/usr/bin/env python

# Compute and display the power spectrum of an image using the discrete
# Fourier transform.  The left viewport shows the original image; the
# right shows the log-scaled, centered magnitude spectrum.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingCore import vtkImageMapToColors
from vtkmodules.vtkImagingFourier import vtkImageFFT, vtkImageFourierCenter
from vtkmodules.vtkImagingMath import vtkImageLogarithmicScale, vtkImageMagnitude
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowLevelLookupTable,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the PGM image
reader = vtkPNMReader()
reader.SetFileName(str(data_dir / "vtks.pgm"))
reader.Update()

# FFT: transform to frequency domain
fft = vtkImageFFT()
fft.SetInputConnection(reader.GetOutputPort())

# Magnitude: compute the magnitude of the complex FFT output
mag = vtkImageMagnitude()
mag.SetInputConnection(fft.GetOutputPort())

# Center: shift the zero-frequency component to the center of the spectrum
center = vtkImageFourierCenter()
center.SetInputConnection(mag.GetOutputPort())

# Compress: apply logarithmic scaling to compress the dynamic range
compress = vtkImageLogarithmicScale()
compress.SetInputConnection(center.GetOutputPort())
compress.SetConstant(15)
compress.Update()

# Actor 1: original image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())
actor_original.GetProperty().SetInterpolationTypeToNearest()

# Actor 2: spectrum image (right viewport) — apply window/level LUT (inlined)
wlut = vtkWindowLevelLookupTable()
wlut.SetWindow(160)
wlut.SetLevel(120)
wlut.Build()

spectrum_color = vtkImageMapToColors()
spectrum_color.SetLookupTable(wlut)
spectrum_color.SetInputConnection(compress.GetOutputPort())

actor_spectrum = vtkImageActor()
actor_spectrum.GetMapper().SetInputConnection(spectrum_color.GetOutputPort())
actor_spectrum.GetProperty().SetInterpolationTypeToNearest()

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.ResetCamera()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — spectrum
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_spectrum)
renderer_right.ResetCamera()
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("VTKSpectrum")
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
