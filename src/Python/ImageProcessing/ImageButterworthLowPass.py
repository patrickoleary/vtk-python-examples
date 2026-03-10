#!/usr/bin/env python

# Apply a Butterworth low-pass filter in the frequency domain to smooth
# a 3D medical volume (FullHead.mhd).  The pipeline converts to the
# frequency domain with vtkImageFFT, applies the Butterworth filter,
# then converts back with vtkImageRFFT.  The left viewport shows the
# original; the right shows the smoothed result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageExtractComponents, vtkImageShiftScale
from vtkmodules.vtkImagingFourier import (
    vtkImageButterworthLowPass,
    vtkImageFFT,
    vtkImageRFFT,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Determine the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# FFT: transform to the frequency domain
fft = vtkImageFFT()
fft.SetInputConnection(reader.GetOutputPort())
fft.SetDimensionality(2)

# Butterworth low-pass: attenuate high frequencies for smoothing
butterworth = vtkImageButterworthLowPass()
butterworth.SetInputConnection(fft.GetOutputPort())
butterworth.SetCutOff(0.2, 0.2, 0.2)
butterworth.SetOrder(2)

# Inverse FFT: transform back to the spatial domain
rfft = vtkImageRFFT()
rfft.SetInputConnection(butterworth.GetOutputPort())
rfft.SetDimensionality(2)

# Extract: take the real component from the complex output
extract = vtkImageExtractComponents()
extract.SetInputConnection(rfft.GetOutputPort())
extract.SetComponents(0)

# Cast original: convert to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# ShiftScale: map the filtered output range to [0, 255] for display
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(extract.GetOutputPort())
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Actor 1: original slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: smoothed slice in the right viewport
actor_smoothed = vtkImageActor()
actor_smoothed.GetMapper().SetInputConnection(shift_scale.GetOutputPort())
actor_smoothed.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — Butterworth smoothed
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_smoothed)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageButterworthLowPass")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
