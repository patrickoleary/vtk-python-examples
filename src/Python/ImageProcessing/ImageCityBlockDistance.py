#!/usr/bin/env python

# Compute the city-block (Manhattan) distance transform of a binary
# image using vtkImageCityBlockDistance and display original vs
# distance map side by side.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageCityBlockDistance
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

# Reader: load a binary PGM image
reader = vtkPNMReader()
reader.SetFileName(str(data_dir / "binary.pgm"))

# Cast to short: vtkImageCityBlockDistance requires short scalar input
cast_to_short = vtkImageCast()
cast_to_short.SetInputConnection(reader.GetOutputPort())
cast_to_short.SetOutputScalarTypeToShort()

# Distance: compute city-block distance from each pixel to the
# nearest zero-valued pixel
distance = vtkImageCityBlockDistance()
distance.SetInputConnection(cast_to_short.GetOutputPort())
distance.SetDimensionality(2)
distance.Update()

# ShiftScale: normalize distance values to [0, 255] for display
scalar_range = distance.GetOutput().GetScalarRange()
scale_factor = 255.0 / max(scalar_range[1], 1.0)
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(distance.GetOutputPort())
shift_scale.SetScale(scale_factor)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Actor 1: original binary image (left viewport)
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(reader.GetOutputPort())

# Actor 2: distance map (right viewport)
actor_distance = vtkImageActor()
actor_distance.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.SetBackground(black_rgb)
renderer_left.ResetCamera()
renderer_left.GetActiveCamera().ParallelProjectionOn()

# Renderer 2: right viewport — distance map
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_distance)
renderer_right.SetBackground(black_rgb)
renderer_right.SetActiveCamera(renderer_left.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetSize(800, 400)
render_window.SetWindowName("ImageCityBlockDistance")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
