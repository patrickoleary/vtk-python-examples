#!/usr/bin/env python

# Compute a Euclidean distance transform from a binary mask of a 3D
# medical volume (FullHead.mhd) using vtkImageEuclideanDistance.  The
# left viewport shows the binary threshold mask; the right shows the
# distance field mapped to a colormap.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageMapToColors, vtkImageThreshold
from vtkmodules.vtkImagingGeneral import vtkImageEuclideanDistance
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

# Threshold: create a binary mask (bone = foreground)
threshold = vtkImageThreshold()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByUpper(600)
threshold.SetInValue(0)
threshold.SetOutValue(1)
threshold.SetOutputScalarTypeToFloat()

# Distance: compute Euclidean distance from each non-zero voxel to the
# nearest zero voxel (foreground boundary)
distance = vtkImageEuclideanDistance()
distance.SetInputConnection(threshold.GetOutputPort())
distance.SetAlgorithmToSaito()
distance.InitializeOn()
distance.Update()

# Lookup table: map distance values to a cool-to-warm colormap
lut = vtkLookupTable()
lut.SetHueRange(0.667, 0.0)
lut.SetRange(0, 50)
lut.SetNumberOfColors(256)
lut.Build()

# Map: apply colormap to the distance field
map_to_colors = vtkImageMapToColors()
map_to_colors.SetInputConnection(distance.GetOutputPort())
map_to_colors.SetLookupTable(lut)
map_to_colors.SetOutputFormatToRGB()

# Cast: convert binary mask to unsigned char for display
cast_mask = vtkImageCast()
cast_mask.SetInputConnection(reader.GetOutputPort())
cast_mask.SetOutputScalarTypeToUnsignedChar()
cast_mask.ClampOverflowOn()

# Actor 1: original slice in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast_mask.GetOutputPort())
actor_original.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Actor 2: distance field in the right viewport
actor_distance = vtkImageActor()
actor_distance.GetMapper().SetInputConnection(map_to_colors.GetOutputPort())
actor_distance.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_original)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — distance field
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_distance)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageEuclideanDistance")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
