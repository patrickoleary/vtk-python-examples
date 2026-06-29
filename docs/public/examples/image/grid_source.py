#!/usr/bin/env python

# Generate and display a grid pattern image using vtkImageGridSource.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkImagingSources import vtkImageGridSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
black_rgb = (0.0, 0.0, 0.0)

# Source: generate a grid pattern image
source = vtkImageGridSource()
source.SetGridSpacing(16, 16, 0)
source.SetGridOrigin(0, 0, 0)
source.SetDataScalarTypeToUnsignedChar()
source.SetDataExtent(0, 255, 0, 255, 0, 0)
source.SetLineValue(255)
source.SetFillValue(0)
source.Update()

# Actor: display the grid image
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(source.GetOutputPort())

# Renderer: assemble the scene with parallel projection for 2D viewing
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(black_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("grid source")
render_window.SetMultiSamples(0)
render_window.SetSize(512, 512)

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
interactor_style_image = vtkInteractorStyleImage()
render_window_interactor.SetInteractorStyle(interactor_style_image)
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure parallel projection for 2D image viewing
renderer.ResetCamera()
renderer.GetActiveCamera().ParallelProjectionOn()

render_window_interactor.Initialize()
render_window_interactor.Start()
