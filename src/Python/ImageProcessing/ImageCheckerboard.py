#!/usr/bin/env python

# Compare two images using a checkerboard pattern with vtkImageCheckerboard.
# The original FullHead slice and a Gaussian-smoothed version are interleaved
# in a checkerboard layout, making differences easy to spot.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageCheckerboard, vtkImageGaussianSmooth
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

# Filter: Gaussian smooth to create a visibly different image
smooth = vtkImageGaussianSmooth()
smooth.SetInputConnection(reader.GetOutputPort())
smooth.SetStandardDeviations(8.0, 8.0, 0.0)
smooth.SetRadiusFactors(5.0, 5.0, 0.0)

# Cast both to same type
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

cast_smooth = vtkImageCast()
cast_smooth.SetInputConnection(smooth.GetOutputPort())
cast_smooth.SetOutputScalarTypeToUnsignedChar()
cast_smooth.ClampOverflowOn()

# Checkerboard: interleave original and smoothed images
checkerboard = vtkImageCheckerboard()
checkerboard.SetInputConnection(0, cast_original.GetOutputPort())
checkerboard.SetInputConnection(1, cast_smooth.GetOutputPort())
checkerboard.SetNumberOfDivisions(4, 4, 1)

# Actor: display the checkerboard comparison
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(checkerboard.GetOutputPort())
actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                       mid_z, mid_z)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageCheckerboard")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
