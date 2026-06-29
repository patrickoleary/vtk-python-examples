#!/usr/bin/env python

# Apply 2D anisotropic diffusion to a medical image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingGeneral import vtkImageAnisotropicDiffusion2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkPNGReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Anisotropic diffusion
diffusion = vtkImageAnisotropicDiffusion2D()
diffusion.SetInputConnection(reader.GetOutputPort())
diffusion.SetDiffusionFactor(1.0)
diffusion.SetDiffusionThreshold(200.0)
diffusion.SetNumberOfIterations(5)
diffusion.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(diffusion.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("anisotropic diffusion2d")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
