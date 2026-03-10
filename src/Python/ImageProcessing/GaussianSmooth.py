#!/usr/bin/env python

# Low-pass filtering with a Gaussian kernel applied to a color image
# (Gourds.png).  The left viewport shows the original; the right shows
# the smoothed result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
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

# Reader: load the color PNG image
reader = vtkPNGReader()
reader.SetFileName(str(data_dir / "Gourds.png"))
reader.Update()

# Cast: convert to float for the Gaussian filter
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToFloat()

# Filter: Gaussian smoothing (low-pass filter)
smooth = vtkImageGaussianSmooth()
smooth.SetDimensionality(2)
smooth.SetInputConnection(cast.GetOutputPort())
smooth.SetStandardDeviations(4.0, 4.0)
smooth.SetRadiusFactors(2.0, 2.0)

# Actor 1: original image in the left viewport
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: smoothed image in the right viewport
actor_smoothed = vtkImageActor()
actor_smoothed.GetMapper().SetInputConnection(smooth.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.ResetCamera()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — smoothed
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_smoothed)
renderer_right.ResetCamera()
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetWindowName("GaussianSmooth")
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
