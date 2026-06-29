#!/usr/bin/env python

# Convert a 2D gradient to polar coordinates using vtkImageEuclideanToPolar.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingGeneral import (
    vtkImageEuclideanToPolar,
    vtkImageGradient,
)
from vtkmodules.vtkImagingSources import vtkImageGaussianSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Gaussian source
gauss = vtkImageGaussianSource()
gauss.SetWholeExtent(0, 255, 0, 255, 0, 44)
gauss.SetCenter(127, 127, 22)
gauss.SetStandardDeviation(50.0)
gauss.SetMaximum(10000.0)

# Gradient
gradient = vtkImageGradient()
gradient.SetInputConnection(gauss.GetOutputPort())
gradient.SetDimensionality(2)

# Euclidean to polar
polar = vtkImageEuclideanToPolar()
polar.SetInputConnection(gradient.GetOutputPort())
polar.SetThetaMaximum(255)
polar.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(polar.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("euclidean to polar")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
