#!/usr/bin/env python

# Map Mandelbrot set to window/level colors using vtkImageMapToWindowLevelColors.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingColor import vtkImageMapToWindowLevelColors
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Constants
range_val = 150
xrad = 200
yrad = 200

# Mandelbrot source
mandelbrot1 = vtkImageMandelbrotSource()
mandelbrot1.SetMaximumNumberOfIterations(150)
mandelbrot1.SetWholeExtent(0, xrad - 1, 0, yrad - 1, 0, 0)
mandelbrot1.SetSampleCX(1.3 / xrad, 1.3 / xrad, 1.3 / xrad, 1.3 / xrad)
mandelbrot1.SetOriginCX(-0.72, 0.22, 0.0, 0.0)
mandelbrot1.SetProjectionAxes(0, 1, 2)

# Map to window/level colors
map_to_wl = vtkImageMapToWindowLevelColors()
map_to_wl.SetInputConnection(mandelbrot1.GetOutputPort())
map_to_wl.SetWindow(range_val)
map_to_wl.SetLevel(range_val / 3.0)
map_to_wl.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(map_to_wl.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("map to window level colors")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
