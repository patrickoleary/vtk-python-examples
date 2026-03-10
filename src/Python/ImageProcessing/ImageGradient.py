#!/usr/bin/env python

# Compute the full gradient vector of a medical volume slice using
# vtkImageGradient and display the gradient magnitude alongside
# the original.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageGradient
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

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Choose the middle axial slice
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Gradient: compute the 2D gradient vector (dx, dy) at each voxel
gradient = vtkImageGradient()
gradient.SetInputConnection(reader.GetOutputPort())
gradient.SetDimensionality(2)
gradient.HandleBoundariesOn()

# Magnitude: compute the magnitude of the gradient vector
magnitude = vtkImageMagnitude()
magnitude.SetInputConnection(gradient.GetOutputPort())
magnitude.Update()

# ShiftScale: normalize gradient magnitude to [0, 255] for display
mag_range = magnitude.GetOutput().GetScalarRange()
scale_factor = 255.0 / max(mag_range[1], 1.0)
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(magnitude.GetOutputPort())
shift_scale.SetScale(scale_factor)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Cast original for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Actor 1: original slice (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Actor 2: gradient magnitude slice (right viewport)
actor_gradient = vtkImageActor()
actor_gradient.GetMapper().SetInputConnection(shift_scale.GetOutputPort())
actor_gradient.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — gradient magnitude
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_gradient)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageGradient")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
