#!/usr/bin/env python

# This MRI image illustrates attenuation that can occur due to sensor
# position.  The artifact is removed by multiplying by an attenuation
# profile determined manually using vtkSphere and vtkSampleFunction.
# The left viewport shows the original; the right shows the corrected result.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingCore import vtkImageCast, vtkImageShiftScale
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
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

# Reader: load the PGM image
reader = vtkPNMReader()
reader.SetFileName(str(data_dir / "AttenuationArtifact.pgm"))
reader.Update()

# Cast: convert to double for arithmetic operations
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToDouble()

# Smooth: reduce discrete scalar artifacts
smooth = vtkImageGaussianSmooth()
smooth.SetInputConnection(cast.GetOutputPort())
smooth.SetStandardDeviations(0.8, 0.8, 0)

# Attenuation profile: a spherical distance field scaled to model the
# sensor sensitivity fall-off
sphere = vtkSphere()
sphere.SetCenter(310, 130, 0)
sphere.SetRadius(0)

sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(0, 264, 0, 264, 0, 1)
sample.SetSampleDimensions(264, 264, 1)

scale = vtkImageShiftScale()
scale.SetInputConnection(sample.GetOutputPort())
scale.SetScale(0.000095)

# Multiply: correct the attenuation by multiplying the smoothed image
# with the scaled distance profile
multiply = vtkImageMathematics()
multiply.SetInputConnection(0, smooth.GetOutputPort())
multiply.SetInputConnection(1, scale.GetOutputPort())
multiply.SetOperationToMultiply()

# Actor 1: original image in the left viewport
color_window = 256.0
color_level = 127.5
actor_original = vtkImageActor()
actor_original.GetMapper().SetInputConnection(cast.GetOutputPort())
actor_original.GetProperty().SetColorWindow(color_window)
actor_original.GetProperty().SetColorLevel(color_level)

# Actor 2: corrected image in the right viewport
actor_corrected = vtkImageActor()
actor_corrected.GetMapper().SetInputConnection(multiply.GetOutputPort())

# Renderer 1: left viewport — original
renderer_left = vtkRenderer()
renderer_left.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_left.AddActor(actor_original)
renderer_left.ResetCamera()
renderer_left.SetBackground(black_rgb)

# Renderer 2: right viewport — corrected
renderer_right = vtkRenderer()
renderer_right.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_right.AddActor(actor_corrected)
renderer_right.ResetCamera()
renderer_right.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_left)
render_window.AddRenderer(renderer_right)
render_window.SetWindowName("Attenuation")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
