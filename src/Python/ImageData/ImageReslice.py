#!/usr/bin/env python

# Reslice a 3D medical volume (FullHead.mhd) along an oblique plane
# using vtkImageReslice and display the result as a 2D image.

import math
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
    vtkImageReslice,
)
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

# Filter: reslice along an oblique plane tilted 25 degrees around Y
cos_angle = math.cos(math.radians(25))
sin_angle = math.sin(math.radians(25))

reslice = vtkImageReslice()
reslice.SetInputConnection(reader.GetOutputPort())
reslice.SetOutputDimensionality(2)
reslice.SetResliceAxesDirectionCosines(
    cos_angle, 0, sin_angle,
    0, 1, 0,
    -sin_angle, 0, cos_angle,
)
reslice.SetResliceAxesOrigin(128, 128, 47)
reslice.SetInterpolationModeToLinear()

# Cast: convert to unsigned char for display
cast = vtkImageCast()
cast.SetInputConnection(reslice.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Actor: display the resliced image as a 2D actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(cast.GetOutputPort())

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("ImageReslice")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
