#!/usr/bin/env python

# Use one image to stencil another using vtkImageToImageStencil.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import (
    vtkBMPReader,
    vtkPNMReader,
)
from vtkmodules.vtkImagingCore import vtkImageTranslateExtent
from vtkmodules.vtkImagingStencil import (
    vtkImageStencil,
    vtkImageToImageStencil,
)
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

# Convert image to stencil
image_to_stencil = vtkImageToImageStencil()
image_to_stencil.SetInputConnection(translate.GetOutputPort())
image_to_stencil.ThresholdBetween(0, 127)
image_to_stencil.SetUpperThreshold(image_to_stencil.GetUpperThreshold())
image_to_stencil.SetLowerThreshold(image_to_stencil.GetLowerThreshold())

# Apply stencil
stencil = vtkImageStencil()
stencil.SetInputConnection(reader1.GetOutputPort())
stencil.SetBackgroundValue(0)
stencil.ReverseStencilOn()
stencil.SetStencilConnection(image_to_stencil.GetOutputPort())
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
render_window.SetWindowName("stencil with image")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
