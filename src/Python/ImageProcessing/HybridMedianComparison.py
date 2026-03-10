#!/usr/bin/env python

# Compare median and hybrid-median filters for removing shot noise from
# a test pattern image.  Four viewports: original (top-left), noisy
# (top-right), hybrid median (bottom-left), standard median (bottom-right).

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageThreshold
from vtkmodules.vtkImagingGeneral import vtkImageHybridMedian2D, vtkImageMedian3D
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

# Reader: load the test pattern image
reader = vtkPNGReader()
reader.SetFileName(str(data_dir / "TestPattern.png"))
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

# Filter 1: standard median filter
median = vtkImageMedian3D()
median.SetInputData(noisy_data)
median.SetKernelSize(5, 5, 1)

# Filter 2: two-pass hybrid median filter (preserves corners/lines)
hybrid_median_1 = vtkImageHybridMedian2D()
hybrid_median_1.SetInputData(noisy_data)
hybrid_median = vtkImageHybridMedian2D()
hybrid_median.SetInputConnection(hybrid_median_1.GetOutputPort())

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

# Actor 3: hybrid median (bottom-left)
actor_hybrid = vtkImageActor()
actor_hybrid.GetMapper().SetInputConnection(hybrid_median.GetOutputPort())
actor_hybrid.GetProperty().SetColorWindow(color_window)
actor_hybrid.GetProperty().SetColorLevel(color_level)
actor_hybrid.GetProperty().SetInterpolationTypeToNearest()
actor_hybrid.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                              mid_z, mid_z)

# Actor 4: standard median (bottom-right)
actor_median = vtkImageActor()
actor_median.GetMapper().SetInputConnection(median.GetOutputPort())
actor_median.GetProperty().SetColorWindow(color_window)
actor_median.GetProperty().SetColorLevel(color_level)
actor_median.GetProperty().SetInterpolationTypeToNearest()

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

# Renderer 3: bottom-left — hybrid median
renderer_bl = vtkRenderer()
renderer_bl.AddActor(actor_hybrid)
renderer_bl.SetViewport(0.0, 0.0, 0.5, 0.5)
renderer_bl.SetBackground(black_rgb)
renderer_bl.SetActiveCamera(renderer_tl.GetActiveCamera())

# Renderer 4: bottom-right — standard median
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
render_window.SetWindowName("HybridMedianComparison")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
