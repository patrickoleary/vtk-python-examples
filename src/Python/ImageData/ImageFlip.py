#!/usr/bin/env python

# Mirror a 3D medical volume (FullHead.mhd) along the X axis using
# vtkImageFlip and display the original and flipped slices side by side.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageFlip,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
left_background_rgb = (0.2, 0.2, 0.3)
right_background_rgb = (0.3, 0.2, 0.2)

# Data directory: defaults to the folder containing this script
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))

# Reader: load the 3D medical volume
reader = vtkMetaImageReader()
reader.SetFileName(str(data_dir / "FullHead.mhd"))
reader.Update()

# Extract the middle axial slice from the original volume
extent = reader.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Cast: convert original to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Filter: flip the volume along the X axis (left-right mirror)
flip = vtkImageFlip()
flip.SetInputConnection(reader.GetOutputPort())
flip.SetFilteredAxis(0)

# Cast: convert flipped to unsigned char for display
cast_flipped = vtkImageCast()
cast_flipped.SetInputConnection(flip.GetOutputPort())
cast_flipped.SetOutputScalarTypeToUnsignedChar()
cast_flipped.ClampOverflowOn()

# Actor: display the original slice
original_actor = vtkImageActor()
original_actor.GetMapper().SetInputConnection(cast_original.GetOutputPort())
original_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Actor: display the flipped slice
flipped_actor = vtkImageActor()
flipped_actor.GetMapper().SetInputConnection(cast_flipped.GetOutputPort())
flipped_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Renderer 1: left viewport — original
renderer1 = vtkRenderer()
renderer1.AddActor(original_actor)
renderer1.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer1.SetBackground(left_background_rgb)
renderer1.ResetCamera()

# Renderer 2: right viewport — flipped
renderer2 = vtkRenderer()
renderer2.AddActor(flipped_actor)
renderer2.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer2.SetBackground(right_background_rgb)
renderer2.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer1)
render_window.AddRenderer(renderer2)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageFlip")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
