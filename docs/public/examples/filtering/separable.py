#!/usr/bin/env python

# Apply separable convolution with gradient in X and Gaussian smoothing in Y.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math
import os

from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingGeneral import vtkImageSeparableConvolution
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Gradient kernel in X
kernel = vtkFloatArray()
kernel.SetNumberOfTuples(3)
kernel.InsertValue(0, -1)
kernel.InsertValue(1, 0)
kernel.InsertValue(2, 1)

# Gaussian kernel in Y
sigma = 1.5
sigma2 = sigma * sigma
gaussian = vtkFloatArray()
gaussian.SetNumberOfTuples(31)
for i in range(31):
    x = i - 15
    g = math.exp(-(x * x) / (2.0 * sigma2)) / (math.sqrt(2.0 * 3.1415) * sigma)
    gaussian.InsertValue(i, g)

# Separable convolution
convolve = vtkImageSeparableConvolution()
convolve.SetInputConnection(reader.GetOutputPort())
convolve.SetDimensionality(2)
convolve.SetXKernel(kernel)
convolve.SetYKernel(gaussian)
convolve.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(convolve.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("separable")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
