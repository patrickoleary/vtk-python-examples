#!/usr/bin/env python

# Render a sphere offscreen, capture pixel data to an image, and display it.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkImageActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere_source = vtkSphereSource()
sphere_source.SetCenter(0.0, 0.0, 0.0)
sphere_source.SetRadius(5.0)
sphere_source.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere_source.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()

render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Pipeline exception: render needed for offscreen capture workflow
render_window.Render()

# Render offscreen
render_window.SetShowWindow(False)
render_window.SetUseOffScreenBuffers(True)
render_window.Render()

# Capture empty framebuffer
size = render_window.GetSize()
image = vtkImageData()
image.SetDimensions(size[0], size[1], 1)
image.AllocateScalars(VTK_UNSIGNED_CHAR, 3)

render_window.SetShowWindow(True)
render_window.SetUseOffScreenBuffers(False)

# Now add the actor and render
renderer.AddActor(actor)
renderer.ResetCamera()
render_window.Render()

# Render offscreen again with actor
render_window.SetShowWindow(False)
render_window.SetUseOffScreenBuffers(True)
render_window.Render()

# Capture framebuffer with sphere
render_window.GetPixelData(
    0, 0, size[0] - 1, size[1] - 1, 0,
    image.GetPointData().GetScalars(), 0)

render_window.SetShowWindow(True)
render_window.SetUseOffScreenBuffers(False)

# Display captured image
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputData(image)
renderer.RemoveActor(actor)
renderer.AddActor(image_actor)
renderer.SetBackground(1, 1, 1)

render_window.SetWindowName("to image")
render_window.Render()
renderer.ResetCamera()

render_window.Render()
interactor.Initialize()
interactor.Start()
