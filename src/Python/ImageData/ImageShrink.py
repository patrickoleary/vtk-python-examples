#!/usr/bin/env python

# Downsample a 3D medical volume (FullHead.mhd) by an integer factor
# using vtkImageShrink3D.  The left viewport shows the original middle
# axial slice; the right shows the downsampled version.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShrink3D
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

# Filter: shrink by a factor of 4 in X and Y, keep Z unchanged
shrink = vtkImageShrink3D()
shrink.SetInputConnection(reader.GetOutputPort())
shrink.SetShrinkFactors(4, 4, 1)
shrink.AveragingOn()
shrink.Update()

shrunk_extent = shrink.GetOutput().GetExtent()
shrunk_mid_z = (shrunk_extent[4] + shrunk_extent[5]) // 2

# Cast original: convert to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Cast shrunk: convert to unsigned char for display
cast_shrunk = vtkImageCast()
cast_shrunk.SetInputConnection(shrink.GetOutputPort())
cast_shrunk.SetOutputScalarTypeToUnsignedChar()
cast_shrunk.ClampOverflowOn()

# Actor 1: original slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: downsampled slice in the right viewport
actor_shrunk = vtkImageActor()
actor_shrunk.GetMapper().SetInputConnection(cast_shrunk.GetOutputPort())
actor_shrunk.SetDisplayExtent(shrunk_extent[0], shrunk_extent[1],
                              shrunk_extent[2], shrunk_extent[3],
                              shrunk_mid_z, shrunk_mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — downsampled
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_shrunk)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageShrink")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
