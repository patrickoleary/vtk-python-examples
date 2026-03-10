#!/usr/bin/env python

# Perform 2D skeletonization on a thresholded slice of a 3D medical
# volume (FullHead.mhd) using vtkImageSkeleton2D.  The left viewport
# shows the binary threshold mask; the right shows the skeleton.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageThreshold
from vtkmodules.vtkImagingMorphological import vtkImageSkeleton2D
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

# Threshold: create a binary mask of bone-like intensities
threshold = vtkImageThreshold()
threshold.SetInputConnection(reader.GetOutputPort())
threshold.ThresholdByUpper(600)
threshold.SetInValue(255)
threshold.SetOutValue(0)
threshold.SetOutputScalarTypeToUnsignedChar()

# Skeleton: thin the binary mask to a 1-pixel-wide skeleton
skeleton = vtkImageSkeleton2D()
skeleton.SetInputConnection(threshold.GetOutputPort())
skeleton.SetNumberOfIterations(20)
skeleton.SetPrune(1)

# Actor 1: binary mask in the left viewport
actor_mask = vtkImageActor()
actor_mask.GetMapper().SetInputConnection(threshold.GetOutputPort())
actor_mask.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                            mid_z, mid_z)

# Actor 2: skeleton in the right viewport
actor_skeleton = vtkImageActor()
actor_skeleton.GetMapper().SetInputConnection(skeleton.GetOutputPort())
actor_skeleton.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3],
                                mid_z, mid_z)

# Renderer 1: left viewport — binary mask
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_mask)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — skeleton
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_skeleton)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageSkeleton")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
