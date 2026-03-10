#!/usr/bin/env python

# Compare ideal and Butterworth high-pass filters in the frequency domain.
# The left viewport shows the ideal high-pass result (with ringing); the
# right shows the Butterworth result (gradual attenuation, less ringing).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingCore import vtkImageExtractComponents
from vtkmodules.vtkImagingFourier import (
    vtkImageButterworthHighPass,
    vtkImageFFT,
    vtkImageIdealHighPass,
    vtkImageRFFT,
)
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

# Reader: load the PNG image
reader = vtkPNGReader()
reader.SetFileName(str(data_dir / "fullhead15.png"))
reader.Update()

# FFT: transform to frequency domain
fft = vtkImageFFT()
fft.SetInputConnection(reader.GetOutputPort())

# Ideal high-pass: sharp cutoff in frequency domain
ideal_high_pass = vtkImageIdealHighPass()
ideal_high_pass.SetInputConnection(fft.GetOutputPort())
ideal_high_pass.SetXCutOff(0.1)
ideal_high_pass.SetYCutOff(0.1)

ideal_rfft = vtkImageRFFT()
ideal_rfft.SetInputConnection(ideal_high_pass.GetOutputPort())

ideal_real = vtkImageExtractComponents()
ideal_real.SetInputConnection(ideal_rfft.GetOutputPort())
ideal_real.SetComponents(0)

# Butterworth high-pass: gradual attenuation avoids ringing
butterworth_high_pass = vtkImageButterworthHighPass()
butterworth_high_pass.SetInputConnection(fft.GetOutputPort())
butterworth_high_pass.SetXCutOff(0.1)
butterworth_high_pass.SetYCutOff(0.1)

butterworth_rfft = vtkImageRFFT()
butterworth_rfft.SetInputConnection(butterworth_high_pass.GetOutputPort())

butterworth_real = vtkImageExtractComponents()
butterworth_real.SetInputConnection(butterworth_rfft.GetOutputPort())
butterworth_real.SetComponents(0)

# Actor 1: ideal high-pass result (left viewport)
ideal_color = vtkImageMapToWindowLevelColors()
ideal_color.SetWindow(500)
ideal_color.SetLevel(0)
ideal_color.SetInputConnection(ideal_real.GetOutputPort())

actor_ideal = vtkImageActor()
actor_ideal.GetMapper().SetInputConnection(ideal_color.GetOutputPort())
actor_ideal.GetProperty().SetInterpolationTypeToNearest()

# Actor 2: Butterworth high-pass result (right viewport)
butterworth_color = vtkImageMapToWindowLevelColors()
butterworth_color.SetWindow(500)
butterworth_color.SetLevel(0)
butterworth_color.SetInputConnection(butterworth_real.GetOutputPort())

actor_butterworth = vtkImageActor()
actor_butterworth.GetMapper().SetInputConnection(butterworth_color.GetOutputPort())
actor_butterworth.GetProperty().SetInterpolationTypeToNearest()

# Renderer 1: left viewport — ideal high-pass
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_ideal)
renderer_left.ResetCamera()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — Butterworth high-pass
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_butterworth)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("IdealHighPass")
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
