#!/usr/bin/env python

# Apply a Sobel 2D edge detector to a slice of a 3D medical volume
# (FullHead.mhd).  The left viewport shows the original middle axial
# slice; the right shows the Sobel edge-detected result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageExtractComponents
from vtkmodules.vtkImagingGeneral import vtkImageSobel2D
from vtkmodules.vtkImagingMath import vtkImageMagnitude
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

# Filter: Sobel 2D edge detection — produces a 2-component gradient output
sobel = vtkImageSobel2D()
sobel.SetInputConnection(reader.GetOutputPort())

# Magnitude: combine the two gradient components into a single scalar
magnitude = vtkImageMagnitude()
magnitude.SetInputConnection(sobel.GetOutputPort())

# Cast original: convert to unsigned char for display
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

# Cast edges: convert the magnitude to unsigned char for display
cast_edges = vtkImageCast()
cast_edges.SetInputConnection(magnitude.GetOutputPort())
cast_edges.SetOutputScalarTypeToUnsignedChar()
cast_edges.ClampOverflowOn()

# Actor 1: original slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: Sobel edge-detected slice in the right viewport
actor_edges = vtkImageActor()
actor_edges.GetMapper().SetInputConnection(cast_edges.GetOutputPort())
actor_edges.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — Sobel edges
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_edges)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageSobel")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
