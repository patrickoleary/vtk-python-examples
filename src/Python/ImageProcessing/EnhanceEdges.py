#!/usr/bin/env python

# Edge enhancement by subtracting the Laplacian from the original image.
# Three viewports show the original (left), the Laplacian (center), and
# the enhanced result (right) for a slice of the FullHead volume.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageLaplacian
from vtkmodules.vtkImagingMath import vtkImageMathematics
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

# Determine scalar range and a representative slice
scalar_range = reader.GetOutput().GetPointData().GetScalars().GetRange()
extent = reader.GetOutput().GetExtent()
mid_z = 22

# Cast: convert to double for arithmetic
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToDouble()

# Laplacian: second-derivative edge detection
laplacian = vtkImageLaplacian()
laplacian.SetInputConnection(cast.GetOutputPort())
laplacian.SetDimensionality(3)

# Enhance: subtract the Laplacian from the original to sharpen edges
enhance = vtkImageMathematics()
enhance.SetInputConnection(0, cast.GetOutputPort())
enhance.SetInputConnection(1, laplacian.GetOutputPort())
enhance.SetOperationToSubtract()

color_window = scalar_range[1] - scalar_range[0]
color_level = color_window / 2

# Actor 1: original slice (left viewport)
original_color = vtkImageMapToWindowLevelColors()
original_color.SetWindow(color_window)
original_color.SetLevel(color_level)
original_color.SetInputConnection(reader.GetOutputPort())

actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(original_color.GetOutputPort())
actor_original.GetProperty().SetInterpolationTypeToNearest()
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: Laplacian slice (center viewport)
laplacian_color = vtkImageMapToWindowLevelColors()
laplacian_color.SetWindow(1000)
laplacian_color.SetLevel(0)
laplacian_color.SetInputConnection(laplacian.GetOutputPort())

actor_laplacian = vtkImageActor()
actor_laplacian.GetMapper().SetInputConnection(laplacian_color.GetOutputPort())
actor_laplacian.GetProperty().SetInterpolationTypeToNearest()
actor_laplacian.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                 mid_z, mid_z)

# Actor 3: enhanced slice (right viewport)
enhanced_color = vtkImageMapToWindowLevelColors()
enhanced_color.SetWindow(color_window)
enhanced_color.SetLevel(color_level)
enhanced_color.SetInputConnection(enhance.GetOutputPort())

actor_enhanced = vtkImageActor()
actor_enhanced.GetMapper().SetInputConnection(enhanced_color.GetOutputPort())
actor_enhanced.GetProperty().SetInterpolationTypeToNearest()
actor_enhanced.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.333, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: center viewport — Laplacian
renderer_center = vtkRenderer()
renderer_center.AddActor(actor_laplacian)
renderer_center.SetViewport(0.333, 0.0, 0.667, 1.0)
renderer_center.SetBackground(black_rgb)
renderer_center.SetActiveCamera(renderer_left.GetActiveCamera())

# Renderer 3: right viewport — enhanced
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_enhanced)
renderer_right.SetViewport(0.667, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(1200, 400)
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_center)
render_window.AddRenderer(renderer_right)
render_window.SetWindowName("EnhanceEdges")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
