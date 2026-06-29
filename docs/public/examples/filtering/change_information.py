#!/usr/bin/env python

# Center an image before rotation using vtkImageChangeInformation.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import (
    vtkImageChangeInformation,
    vtkImageReslice,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Center the image at (0,0,0)
information = vtkImageChangeInformation()
information.SetInputConnection(reader.GetOutputPort())
information.CenterImageOn()

# Reslice with rotated axes
reslice = vtkImageReslice()
reslice.SetInputConnection(information.GetOutputPort())
reslice.SetResliceAxesDirectionCosines([0.866025, -0.5, 0, 0.5, 0.866025, 0, 0, 0, 1])
reslice.SetInterpolationModeToCubic()

# Reset information back to original
reader.Update()
information2 = vtkImageChangeInformation()
information2.SetInputConnection(reslice.GetOutputPort())
information2.SetInformationInputData(reader.GetOutput())
information2.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(information2.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("change information")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
