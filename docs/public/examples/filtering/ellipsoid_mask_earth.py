#!/usr/bin/env python

# Apply multiple ellipsoid masks to an earth image using vtkImageMask.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNMReader
from vtkmodules.vtkImagingCore import vtkImageMask
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read earth image
reader = vtkPNMReader()
reader.ReleaseDataFlagOff()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFileName(os.path.join(data_dir, "earth.ppm"))
reader.Update()

# First ellipsoid mask
sphere = vtkImageEllipsoidSource()
sphere.SetWholeExtent(0, 511, 0, 255, 0, 0)
sphere.SetCenter(128, 128, 0)
sphere.SetRadius(80, 80, 1)
sphere.Update()

mask = vtkImageMask()
mask.SetImageInputData(reader.GetOutput())
mask.SetMaskInputData(sphere.GetOutput())
mask.SetMaskedOutputValue(100, 128, 200)
mask.NotMaskOn()
mask.ReleaseDataFlagOff()
mask.Update()

# Second ellipsoid mask
sphere2 = vtkImageEllipsoidSource()
sphere2.SetWholeExtent(0, 511, 0, 255, 0, 0)
sphere2.SetCenter(328, 128, 0)
sphere2.SetRadius(80, 50, 1)
sphere2.Update()

mask2 = vtkImageMask()
mask2.SetImageInputData(mask.GetOutput())
mask2.SetMaskInputData(sphere2.GetOutput())
mask2.SetMaskedOutputValue(100)
mask2.NotMaskOn()
mask2.ReleaseDataFlagOff()
mask2.Update()

# Third ellipsoid mask with alpha
sphere3 = vtkImageEllipsoidSource()
sphere3.SetWholeExtent(0, 511, 0, 255, 0, 0)
sphere3.SetCenter(228, 155, 0)
sphere3.SetRadius(80, 80, 1)
sphere3.Update()

mask3 = vtkImageMask()
mask3.SetImageInputData(mask2.GetOutput())
mask3.SetMaskInputData(sphere3.GetOutput())
mask3.SetMaskedOutputValue(255)
mask3.NotMaskOn()
mask3.SetMaskAlpha(0.5)
mask3.ReleaseDataFlagOff()
mask3.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(mask3.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 256)
render_window.SetWindowName("ellipsoid mask earth")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
