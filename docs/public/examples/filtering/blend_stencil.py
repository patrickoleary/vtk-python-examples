#!/usr/bin/env python

# Alpha-blend two images with a spherical stencil using vtkImageBlend.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkIOImage import (
    vtkBMPReader,
    vtkPNMReader,
)
from vtkmodules.vtkImagingCore import (
    vtkImageBlend,
    vtkImageTranslateExtent,
)
from vtkmodules.vtkImagingStencil import vtkImplicitFunctionToImageStencil
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read two images
reader1 = vtkBMPReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader1.SetFileName(os.path.join(data_dir, "masonry.bmp"))

reader2 = vtkPNMReader()
reader2.SetFileName(os.path.join(data_dir, "B.pgm"))

# Translate second image
translate = vtkImageTranslateExtent()
translate.SetInputConnection(reader2.GetOutputPort())
translate.SetTranslation(60, 60, 0)

# Spherical stencil
sphere = vtkSphere()
sphere.SetCenter(121, 131, 0)
sphere.SetRadius(70)

function_to_stencil = vtkImplicitFunctionToImageStencil()
function_to_stencil.SetInput(sphere)

# Blend with stencil
blend = vtkImageBlend()
blend.SetInputConnection(reader1.GetOutputPort())
blend.AddInputConnection(translate.GetOutputPort())
blend.ReplaceNthInputConnection(1, reader1.GetOutputPort())
blend.ReplaceNthInputConnection(1, translate.GetOutputPort())
blend.SetOpacity(1, 0.8)
blend.SetStencilConnection(function_to_stencil.GetOutputPort())
blend.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(blend.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("blend stencil")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
