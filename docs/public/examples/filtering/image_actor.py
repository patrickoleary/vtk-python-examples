#!/usr/bin/env python

# Test vtkImageActor with TIFF reader and luminance conversion.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Load TIFF image
tiff_reader = vtkTIFFReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

tiff_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader.SetOrientationType(4)

# Convert to luminance
luminance = vtkImageLuminance()
luminance.SetInputConnection(tiff_reader.GetOutputPort())

# Display as image actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(luminance.GetOutputPort())

renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("image actor")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# First render shows greyscale
render_window.Render()

# Switch from greyscale to RGB to test against an old bug
image_actor.GetMapper().SetInputConnection(tiff_reader.GetOutputPort())
camera = renderer.GetActiveCamera()
camera.Elevation(-30)
camera.Roll(-20)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
