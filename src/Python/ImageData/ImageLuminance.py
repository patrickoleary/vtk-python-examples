#!/usr/bin/env python

# Convert an RGB color image (Gourds.png) to grayscale using
# vtkImageLuminance.  The left viewport shows the original color image;
# the right shows the grayscale luminance result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingColor import vtkImageLuminance
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

# Filter: convert RGB to grayscale luminance
luminance = vtkImageLuminance()
luminance.SetInputConnection(reader.GetOutputPort())

# Actor 1: original color image in the left viewport
actor_color = vtkImageActor()
actor_color.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: grayscale luminance in the right viewport
actor_gray = vtkImageActor()
actor_gray.GetMapper().SetInputConnection(luminance.GetOutputPort())

# Renderer 1: left viewport — original color
renderer_left = vtkRenderer()
renderer_left.AddActor(actor_color)
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()

# Renderer 2: right viewport — grayscale
renderer_right = vtkRenderer()
renderer_right.AddActor(actor_gray)
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.SetBackground(black_rgb)
renderer_right.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(1200, 500)
render_window.SetWindowName("ImageLuminance")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
