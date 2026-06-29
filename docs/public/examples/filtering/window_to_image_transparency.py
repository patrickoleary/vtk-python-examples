#!/usr/bin/env python

# Test vtkWindowToImageFilter with RGBA transparency.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkImageMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetAlphaBitPlanes(1)
render_window.SetWindowName("window to image transparency")
render_window.SetMultiSamples(0)
render_window.SetSize(256, 256)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Sphere
sphere = vtkSphereSource()

sph_mapper = vtkPolyDataMapper()
sph_mapper.SetInputConnection(sphere.GetOutputPort())

sph_actor = vtkActor()
sph_actor.SetMapper(sph_mapper)

renderer.AddActor(sph_actor)

# Render first image
render_window.Render()

# Create window to image filter, grabbing RGB and alpha
window_to_image = vtkWindowToImageFilter()
window_to_image.SetInput(render_window)
window_to_image.SetInputBufferTypeToRGBA()
window_to_image.Update()

# Copy the output
output_data = window_to_image.GetOutput().NewInstance()
output_data.DeepCopy(window_to_image.GetOutput())

# Set up mapper and actor to display the image
image_mapper = vtkImageMapper()
image_mapper.SetColorWindow(255)
image_mapper.SetColorLevel(127.5)
image_mapper.SetInputData(output_data)

image_actor = vtkActor2D()
image_actor.SetMapper(image_mapper)

# Change the image - scale sphere and change background to green
sph_actor.SetScale(2, 2, 2)
renderer.SetBackground(0, 1, 0)

# Add the image of the sphere
renderer.AddActor(image_actor)
renderer.SetViewport(0, 0, 1, 1)

interactor.Initialize()
interactor.Start()
