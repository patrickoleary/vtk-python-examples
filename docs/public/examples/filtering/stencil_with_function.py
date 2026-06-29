#!/usr/bin/env python

# Use a spherical implicit function as a stencil to mask a medical image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkImplicitFunctionToImageStencil,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read image
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
reader.SetDataOrigin(0.0, 0.0, 0.0)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))
reader.Update()

# Spherical stencil
sphere = vtkSphere()
sphere.SetCenter(128, 128, 0)
sphere.SetRadius(80)

function_to_stencil = vtkImplicitFunctionToImageStencil()
function_to_stencil.SetInput(sphere)
function_to_stencil.SetInformationInput(reader.GetOutput())
function_to_stencil.Update()

# Copy the stencil (for coverage)
stencil_original = function_to_stencil.GetOutput()
stencil_copy = stencil_original.NewInstance()
stencil_copy.DeepCopy(function_to_stencil.GetOutput())

# Darkened background
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(reader.GetOutputPort())
shift_scale.SetScale(0.2)
shift_scale.Update()

# Apply stencil
stencil = vtkImageStencil()
stencil.SetInputConnection(reader.GetOutputPort())
stencil.SetBackgroundInputData(shift_scale.GetOutput())
stencil.SetStencilData(stencil_copy)
stencil.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(stencil.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("stencil with function")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
