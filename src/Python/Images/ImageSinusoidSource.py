#!/usr/bin/env python

# Generate and display a sinusoidal pattern image using
# vtkImageSinusoidSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageSinusoidSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: generate a sinusoidal pattern image
source = vtkImageSinusoidSource()
source.SetWholeExtent(0, 255, 0, 255, 0, 0)
source.SetAmplitude(127)
source.SetDirection(1.0, 1.0, 0.0)
source.SetPeriod(64.0)
source.Update()

# Cast: convert from double to unsigned char for display
cast_filter = vtkImageCast()
cast_filter.SetInputConnection(source.GetOutputPort())
cast_filter.SetOutputScalarTypeToUnsignedChar()
cast_filter.ClampOverflowOn()

# Actor: display the sinusoidal image
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(cast_filter.GetOutputPort())

# Renderer: assemble the scene with parallel projection for 2D viewing
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("ImageSinusoidSource")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
