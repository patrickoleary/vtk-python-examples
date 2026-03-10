#!/usr/bin/env python

# Apply an ideal low-pass filter in the frequency domain to smooth a
# medical volume slice and display original vs filtered side by side.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingFourier import vtkImageFFT, vtkImageIdealLowPass, vtkImageRFFT
from vtkmodules.vtkImagingMath import vtkImageMagnitude
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
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

# Reader: load a single slice PNG image
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Choose the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# FFT: transform the image to the frequency domain
fft = vtkImageFFT()
fft.SetInputConnection(reader.GetOutputPort())
fft.SetDimensionality(2)

# IdealLowPass: zero all frequencies above the cutoff
low_pass = vtkImageIdealLowPass()
low_pass.SetInputConnection(fft.GetOutputPort())
low_pass.SetXCutOff(0.05)
low_pass.SetYCutOff(0.05)

# RFFT: transform back to the spatial domain
rfft = vtkImageRFFT()
rfft.SetInputConnection(low_pass.GetOutputPort())
rfft.SetDimensionality(2)

# Magnitude: extract real magnitude from complex output
magnitude = vtkImageMagnitude()
magnitude.SetInputConnection(rfft.GetOutputPort())

# Cast filtered to unsigned char for display
cast_filtered = vtkImageCast()
cast_filtered.SetInputConnection(magnitude.GetOutputPort())
cast_filtered.SetOutputScalarTypeToUnsignedChar()
cast_filtered.ClampOverflowOn()

# Cast original to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Actor 1: original slice (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Actor 2: low-pass filtered slice (right viewport)
actor_filtered = vtkImageActor()
actor_filtered.GetMapper().SetInputConnection(cast_filtered.GetOutputPort())
actor_filtered.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — low-pass filtered
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_filtered)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageIdealLowPass")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
