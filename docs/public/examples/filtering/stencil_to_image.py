#!/usr/bin/env python

# Convert a spherical stencil to a binary image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkImagingStencil import (
    vtkImageStencilToImage,
    vtkImplicitFunctionToImageStencil,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere
sphere = vtkSphere()
sphere.SetCenter(128, 128, 0)
sphere.SetRadius(80)

# Convert to stencil
function_to_stencil = vtkImplicitFunctionToImageStencil()
function_to_stencil.SetInput(sphere)
function_to_stencil.SetOutputOrigin(0, 0, 0)
function_to_stencil.SetOutputSpacing(1, 1, 1)
function_to_stencil.SetOutputWholeExtent(0, 255, 0, 255, 0, 0)

# Stencil to binary image
stencil_to_image = vtkImageStencilToImage()
stencil_to_image.SetInputConnection(function_to_stencil.GetOutputPort())
stencil_to_image.SetOutsideValue(0)
stencil_to_image.SetInsideValue(255)
stencil_to_image.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(stencil_to_image.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("stencil to image")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
