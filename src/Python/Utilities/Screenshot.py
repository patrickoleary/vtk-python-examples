#!/usr/bin/env python

# Capture a render window to a PNG image file.

import tempfile

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkWindowToImageFilter,
)

# Colors (normalized RGB)
indian_red_rgb = (0.804, 0.361, 0.361)
misty_rose_rgb = (1.0, 0.894, 0.882)

# Source: generate a sphere
sphere = vtkSphereSource()
sphere.SetRadius(5.0)
sphere.SetPhiResolution(30)
sphere.SetThetaResolution(30)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(indian_red_rgb)
actor.GetProperty().SetSpecular(0.6)
actor.GetProperty().SetSpecularPower(30)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(misty_rose_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Screenshot")
render_window.Render()

# Screenshot: capture the render window contents to a PNG file.
# vtkWindowToImageFilter reads the framebuffer and produces an image.
# vtkPNGWriter writes the image to disk.
window_to_image = vtkWindowToImageFilter()
window_to_image.SetInput(render_window)
window_to_image.SetInputBufferTypeToRGB()
window_to_image.ReadFrontBufferOff()
window_to_image.Update()

screenshot_path = tempfile.NamedTemporaryFile(
    suffix=".png", prefix="vtk_screenshot_", delete=False
).name

writer = vtkPNGWriter()
writer.SetFileName(screenshot_path)
writer.SetInputConnection(window_to_image.GetOutputPort())
writer.Write()

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
