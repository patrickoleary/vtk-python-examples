#!/usr/bin/env python

# Alpha-blend two images using vtkImageBlend.  The original FullHead
# slice is blended with a Sobel edge-detected version to create a
# composite that highlights edges over the anatomy.  Three viewports
# show the original, the edges, and the blended result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageBlend, vtkImageCast
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

# Filter: Sobel edge detection for the overlay
sobel = vtkImageSobel2D()
sobel.SetInputConnection(reader.GetOutputPort())

magnitude = vtkImageMagnitude()
magnitude.SetInputConnection(sobel.GetOutputPort())

# Cast both inputs to the same type before blending
cast_original = vtkImageCast()
cast_original.SetInputConnection(reader.GetOutputPort())
cast_original.SetOutputScalarTypeToUnsignedChar()
cast_original.ClampOverflowOn()

cast_edges = vtkImageCast()
cast_edges.SetInputConnection(magnitude.GetOutputPort())
cast_edges.SetOutputScalarTypeToUnsignedChar()
cast_edges.ClampOverflowOn()

# Blend: combine original (60%) with edges (40%)
blend = vtkImageBlend()
blend.AddInputConnection(0, cast_original.GetOutputPort())
blend.AddInputConnection(0, cast_edges.GetOutputPort())
blend.SetOpacity(0, 0.6)
blend.SetOpacity(1, 0.4)

# Actor 1: original
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_original.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: edges
actor_edges = vtkImageActor()
actor_edges.GetMapper().SetInputConnection(cast_edges.GetOutputPort())
actor_edges.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Actor 3: blended
actor_blend = vtkImageActor()
actor_blend.GetMapper().SetInputConnection(blend.GetOutputPort())
actor_blend.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                             mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: center viewport — edges
renderer_center = vtkRenderer()
renderer_center.AddActor(actor_edges)
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.SetBackground(black_rgb)
renderer_center.ResetCamera()

# Renderer 3: right viewport — blended
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_blend)
renderer_right.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_center)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1500, 500)
render_window.SetWindowName("ImageBlend")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
