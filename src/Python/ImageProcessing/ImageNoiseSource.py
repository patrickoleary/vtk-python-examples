#!/usr/bin/env python

# Generate and display a random noise image using vtkImageNoiseSource.
# The noise image is displayed as a 2D slice with values mapped to
# grayscale.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageNoiseSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: generate a 256x256 random noise image with values in [0, 255]
noise = vtkImageNoiseSource()
noise.SetWholeExtent(0, 255, 0, 255, 0, 0)
noise.SetMinimum(0.0)
noise.SetMaximum(255.0)
noise.Update()

# Cast: convert to unsigned char for display
cast = vtkImageCast()
cast.SetInputConnection(noise.GetOutputPort())
cast.SetOutputScalarTypeToUnsignedChar()
cast.ClampOverflowOn()

# Actor: display the noise image
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(cast.GetOutputPort())

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 640)
render_window.SetWindowName("ImageNoiseSource")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
