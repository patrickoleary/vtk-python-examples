#!/usr/bin/env python

# Compute the gradient magnitude of a 3D medical volume (FullHead.mhd)
# using vtkImageGradientMagnitude and display a middle axial slice
# showing tissue edges via the standard VTK rendering pipeline.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageGradientMagnitude
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

# Filter: compute gradient magnitude for edge detection
gradient_magnitude = vtkImageGradientMagnitude()
gradient_magnitude.SetInputConnection(reader.GetOutputPort())
gradient_magnitude.SetDimensionality(3)
gradient_magnitude.HandleBoundariesOn()

# Cast: convert output to unsigned char for display
cast = vtkImageCast()
cast.SetInputConnection(gradient_magnitude.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()
cast.Update()

# Choose the middle axial slice
extent = cast.GetOutput().GetExtent()
mid_z = (extent[4] + extent[5]) // 2

# Actor: display the gradient magnitude slice
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(cast.GetOutputPort())
actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], mid_z, mid_z)

# Renderer: assemble the scene with parallel projection for 2D viewing
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageGradientMagnitude")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
