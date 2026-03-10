#!/usr/bin/env python

# Swap axes of a 3D medical volume (FullHead.mhd) using vtkImagePermute
# to convert an axial view to a coronal view.  The left viewport shows
# the original middle axial slice; the right shows the middle coronal
# slice after permuting axes.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImagePermute
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

# Filter: permute axes — swap Y and Z to convert axial to coronal view
permute = vtkImagePermute()
permute.SetInputConnection(reader.GetOutputPort())
permute.SetFilteredAxes(0, 2, 1)
permute.Update()

permuted_extent = permute.GetOutput().GetExtent()
permuted_mid_z = (permuted_extent[4] + permuted_extent[5]) // 2

# Cast original: convert to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Cast permuted: convert to unsigned char for display
cast_permuted = vtkImageCast()
cast_permuted.SetInputConnection(permute.GetOutputPort())
cast_permuted.SetOutputScalarTypeToUnsignedChar()
cast_permuted.ClampOverflowOn()

# Actor 1: original axial slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: coronal slice (from permuted volume) in the right viewport
actor_permuted = vtkImageActor()
actor_permuted.GetMapper().SetInputConnection(cast_permuted.GetOutputPort())
actor_permuted.SetDisplayExtent(permuted_extent[0], permuted_extent[1],
                                permuted_extent[2], permuted_extent[3],
                                permuted_mid_z, permuted_mid_z)

# Renderer 1: left viewport — original axial
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — permuted (coronal)
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_permuted)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImagePermute")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
