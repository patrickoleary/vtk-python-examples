#!/usr/bin/env python

# Generate and display a Mandelbrot fractal image using
# vtkImageMandelbrotSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingCore import vtkImageCast
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: generate a Mandelbrot fractal image
source = vtkImageMandelbrotSource()
source.SetWholeExtent(0, 511, 0, 511, 0, 0)
source.SetProjectionAxes(0, 1, 2)
source.SetOriginCX(-1.75, -1.25, 0.0, 0.0)
source.SetSizeCX(2.5, 2.5, 2.0, 1.5)
source.SetMaximumNumberOfIterations(200)
source.Update()

# Cast: convert from float to unsigned char for display
cast_filter = vtkImageCast()
cast_filter.SetInputConnection(source.GetOutputPort())
cast_filter.SetOutputScalarTypeToUnsignedChar()
cast_filter.ClampOverflowOn()

# Actor: display the fractal image
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
render_window.SetWindowName("ImageMandelbrotSource")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
