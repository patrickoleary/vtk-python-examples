#!/usr/bin/env python

# Test combined update extent handling when multiple algorithms
# request different extents from the same source.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import (
    vtkImageBlend,
    vtkImageClip,
    vtkImageShiftScale,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read an image that has an extent of 0 255 0 255 0 0
reader = vtkPNGReader()
reader.SetDataSpacing(0.8, 0.8, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "fullhead15.png"))

# Clip the image down to 0 127 0 127 0 0
clip = vtkImageClip()
clip.SetInputConnection(reader.GetOutputPort())
clip.SetOutputWholeExtent(0, 127, 0, 127, 0, 0)

# Darken the background
darken = vtkImageShiftScale()
darken.SetInputConnection(reader.GetOutputPort())
darken.SetScale(0.2)

# Blend clipped and darkened images
blend = vtkImageBlend()
blend.SetInputConnection(darken.GetOutputPort())
blend.AddInputConnection(clip.GetOutputPort())
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
render_window.SetWindowName("multiple update extents")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
