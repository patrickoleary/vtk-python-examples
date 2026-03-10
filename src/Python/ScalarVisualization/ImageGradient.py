#!/usr/bin/env python

# Visualize gradient information of a CT head slice as an HSV color image.

import os
from pathlib import Path

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkIOImage import vtkMetaImageReader
from vtkmodules.vtkImagingColor import vtkImageHSVToRGB
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageConstantPad,
    vtkImageExtractComponents,
    vtkImageMagnify,
)
from vtkmodules.vtkImagingGeneral import (
    vtkImageEuclideanToPolar,
    vtkImageGaussianSmooth,
    vtkImageGradient,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
silver = (0.753, 0.753, 0.753)

# Data file
data_dir = Path(os.environ.get("VPE_DATA_DIR", Path(__file__).parent))
file_name = str(data_dir / "FullHead.mhd")

# Reader: load the CT head volume
reader = vtkMetaImageReader()
reader.SetFileName(file_name)
reader.Update()

# Filter: cast to float for gradient computation
cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToFloat()

# Filter: magnify the image 2x
magnify = vtkImageMagnify()
magnify.SetInputConnection(cast.GetOutputPort())
magnify.SetMagnificationFactors(2, 2, 1)
magnify.InterpolateOn()

# Filter: smooth to remove high-frequency interpolation artifacts
smooth = vtkImageGaussianSmooth()
smooth.SetInputConnection(magnify.GetOutputPort())
smooth.SetDimensionality(2)
smooth.SetStandardDeviations(1.5, 1.5, 0.0)
smooth.SetRadiusFactors(2.01, 2.01, 0.0)

# Filter: compute the 2D gradient
gradient = vtkImageGradient()
gradient.SetInputConnection(smooth.GetOutputPort())
gradient.SetDimensionality(2)

# Filter: convert gradient to polar coordinates (magnitude → saturation, direction → hue)
polar = vtkImageEuclideanToPolar()
polar.SetInputConnection(gradient.GetOutputPort())
polar.SetThetaMaximum(255.0)

# Filter: pad to three components for HSV representation
pad = vtkImageConstantPad()
pad.SetInputConnection(polar.GetOutputPort())
pad.SetOutputNumberOfScalarComponents(3)
pad.SetConstant(200.0)

# Filter: permute components into HSV order
permute = vtkImageExtractComponents()
permute.SetInputConnection(pad.GetOutputPort())
permute.SetComponents(0, 2, 1)

# Filter: convert HSV to RGB
rgb = vtkImageHSVToRGB()
rgb.SetInputConnection(permute.GetOutputPort())
rgb.SetMaximum(255.0)

# Filter: cast back to unsigned char for display
display_cast = vtkImageCast()
display_cast.SetInputConnection(rgb.GetOutputPort())
display_cast.SetOutputScalarTypeToUnsignedChar()
display_cast.ClampOverflowOn()

# Actor: display the RGB image slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(display_cast.GetOutputPort())
image_actor.SetDisplayExtent(0, 511, 0, 511, 22, 22)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(silver)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("ImageGradient")
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
