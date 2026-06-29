#!/usr/bin/env python

# Compute 2D gradient magnitude on a clipped subregion of a medical image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import (
    vtkImageChangeInformation,
    vtkImageClip,
)
from vtkmodules.vtkImagingGeneral import vtkImageGradientMagnitude
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

# Clip subregion
clip = vtkImageClip()
clip.SetInputConnection(reader.GetOutputPort())
clip.SetOutputWholeExtent(80, 230, 80, 230, 0, 0)
clip.ClipDataOff()

# Gradient magnitude
gradient = vtkImageGradientMagnitude()
gradient.SetDimensionality(2)
gradient.SetInputConnection(clip.GetOutputPort())
gradient.HandleBoundariesOff()

# Translate extent
slide = vtkImageChangeInformation()
slide.SetInputConnection(gradient.GetOutputPort())
slide.SetExtentTranslation(-100, -100, 0)
slide.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(slide.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(150, 150)
render_window.SetWindowName("gradient magnitude subregion")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
