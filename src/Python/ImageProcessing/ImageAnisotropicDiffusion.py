#!/usr/bin/env python

# Edge-preserving smoothing of a 3D medical volume (FullHead.mhd) using
# vtkImageAnisotropicDiffusion2D.  The left viewport shows the original
# middle axial slice; the right shows the diffused result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageAnisotropicDiffusion2D
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

# Filter: anisotropic diffusion — smooths homogeneous regions while
# preserving edges by limiting diffusion across large gradients
diffusion = vtkImageAnisotropicDiffusion2D()
diffusion.SetInputConnection(reader.GetOutputPort())
diffusion.SetNumberOfIterations(10)
diffusion.SetDiffusionThreshold(20.0)
diffusion.SetDiffusionFactor(1.0)

# Cast original: convert to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Cast diffused: convert to unsigned char for display
cast_diffused = vtkImageCast()
cast_diffused.SetInputConnection(diffusion.GetOutputPort())
cast_diffused.SetOutputScalarTypeToUnsignedChar()
cast_diffused.ClampOverflowOn()

# Actor 1: original slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: diffused slice in the right viewport
actor_diffused = vtkImageActor()
actor_diffused.GetMapper().SetInputConnection(cast_diffused.GetOutputPort())
actor_diffused.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — diffused
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_diffused)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageAnisotropicDiffusion")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
