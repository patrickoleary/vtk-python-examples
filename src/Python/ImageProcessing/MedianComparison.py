#!/usr/bin/env python

# Compare Gaussian and median smoothing for reducing low-probability
# high-amplitude (shot) noise on a slice of FullHead.mhd.  Four
# viewports: original (top-left), noisy (top-right), Gaussian smoothed
# (bottom-left), median filtered (bottom-right).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageThreshold
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth, vtkImageMedian3D
from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import vtkImageNoiseSource
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

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

scalar_range = reader.GetOutput().GetPointData().GetScalars().GetRange()
extent = reader.GetOutput().GetExtent()
mid_z = (extent[5] - extent[4]) // 2

# Cast: convert to double for arithmetic
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToDouble()
cast.Update()

original_data = vtkImageData()
original_data.DeepCopy(cast.GetOutput())

# Generate shot noise and add it to the original image (inlined)
noise_amplitude = 2000.0
noise_fraction = 0.1

noise_source = vtkImageNoiseSource()
noise_source.SetWholeExtent(extent)
noise_source.SetMinimum(0.0)
noise_source.SetMaximum(1.0)

noise_thresh_high = vtkImageThreshold()
noise_thresh_high.SetInputConnection(noise_source.GetOutputPort())
noise_thresh_high.ThresholdByLower(1.0 - noise_fraction)
noise_thresh_high.SetInValue(0)
noise_thresh_high.SetOutValue(noise_amplitude)

noise_thresh_low = vtkImageThreshold()
noise_thresh_low.SetInputConnection(noise_source.GetOutputPort())
noise_thresh_low.ThresholdByLower(noise_fraction)
noise_thresh_low.SetInValue(1.0 - noise_amplitude)
noise_thresh_low.SetOutValue(0.0)

shot_noise = vtkImageMathematics()
shot_noise.SetInputConnection(0, noise_thresh_high.GetOutputPort())
shot_noise.SetInputConnection(1, noise_thresh_low.GetOutputPort())
shot_noise.SetOperationToAdd()

add_noise = vtkImageMathematics()
add_noise.SetInputData(0, original_data)
add_noise.SetInputConnection(1, shot_noise.GetOutputPort())
add_noise.SetOperationToAdd()
add_noise.Update()

noisy_data = vtkImageData()
noisy_data.DeepCopy(add_noise.GetOutput())

# Filter 1: median filter
median = vtkImageMedian3D()
median.SetInputData(noisy_data)
median.SetKernelSize(5, 5, 1)

# Filter 2: Gaussian smoothing
gaussian = vtkImageGaussianSmooth()
gaussian.SetDimensionality(2)
gaussian.SetInputData(noisy_data)
gaussian.SetStandardDeviations(2.0, 2.0)
gaussian.SetRadiusFactors(2.0, 2.0)

color_window = (scalar_range[1] - scalar_range[0]) * 0.8
color_level = color_window / 2

# Actor 1: original (top-left)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputData(original_data)
actor_original.GetProperty().SetColorWindow(color_window)
actor_original.GetProperty().SetColorLevel(color_level)
actor_original.GetProperty().SetInterpolationTypeToNearest()
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: noisy (top-right)
actor_noisy = vtkImageActor()
actor_noisy.GetMapper().SetInputData(noisy_data)
actor_noisy.GetProperty().SetColorWindow(color_window)
actor_noisy.GetProperty().SetColorLevel(color_level)
actor_noisy.GetProperty().SetInterpolationTypeToNearest()
actor_noisy.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Actor 3: Gaussian smoothed (bottom-left)
actor_gaussian = vtkImageActor()
actor_gaussian.GetMapper().SetInputConnection(gaussian.GetOutputPort())
actor_gaussian.GetProperty().SetColorWindow(color_window)
actor_gaussian.GetProperty().SetColorLevel(color_level)
actor_gaussian.GetProperty().SetInterpolationTypeToNearest()
actor_gaussian.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 4: median filtered (bottom-right)
actor_median = vtkImageActor()
actor_median.GetMapper().SetInputConnection(median.GetOutputPort())
actor_median.GetProperty().SetColorWindow(color_window)
actor_median.GetProperty().SetColorLevel(color_level)
actor_median.GetProperty().SetInterpolationTypeToNearest()
actor_median.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                              mid_z, mid_z)

# Renderer 1: top-left — original
renderer_tl = vtkRenderer()
renderer_tl.AddActor(actor_original)
renderer_tl.SetViewport(0.0, 0.5, 0.5, 1.0)
renderer_tl.SetBackground(black_rgb)
renderer_tl.ResetCamera()

# Renderer 2: top-right — noisy
renderer_tr = vtkRenderer()
renderer_tr.AddActor(actor_noisy)
renderer_tr.SetViewport(0.5, 0.5, 1.0, 1.0)
renderer_tr.SetBackground(black_rgb)
renderer_tr.SetActiveCamera(renderer_tl.GetActiveCamera())

# Renderer 3: bottom-left — Gaussian
renderer_bl = vtkRenderer()
renderer_bl.AddActor(actor_gaussian)
renderer_bl.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_bl.SetBackground(black_rgb)
renderer_bl.SetActiveCamera(renderer_tl.GetActiveCamera())

# Renderer 4: bottom-right — median
renderer_br = vtkRenderer()
renderer_br.AddActor(actor_median)
renderer_br.SetViewport(0.5, 0.0, 1.0, 0.5)
renderer_br.SetBackground(black_rgb)
renderer_br.SetActiveCamera(renderer_tl.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(800, 800)
render_window.AddRenderer(renderer_tl)
render_window.AddRenderer(renderer_tr)
render_window.AddRenderer(renderer_bl)
render_window.AddRenderer(renderer_br)
render_window.SetWindowName("MedianComparison")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
