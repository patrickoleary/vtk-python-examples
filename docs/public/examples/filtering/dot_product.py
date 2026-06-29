#!/usr/bin/env python

# Compute dot product between a gradient field and a color image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import (
    vtkBMPReader,
    vtkPNGReader,
)
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageShiftScale,
)
from vtkmodules.vtkImagingGeneral import vtkImageGradient
from vtkmodules.vtkImagingMath import vtkImageDotProduct
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

cast = vtkImageCast()
cast.SetInputConnection(reader.GetOutputPort())
cast.SetOutputScalarTypeToFloat()

shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(cast.GetOutputPort())
shift_scale.SetScale(0.05)

gradient = vtkImageGradient()
gradient.SetInputConnection(shift_scale.GetOutputPort())
gradient.SetDimensionality(3)
gradient.Update()

bmp_reader = vtkBMPReader()
bmp_reader.SetFileName(os.path.join(data_dir, "masonry.bmp"))

cast2 = vtkImageCast()
cast2.SetInputConnection(bmp_reader.GetOutputPort())
cast2.SetOutputScalarTypeToDouble()
cast2.Update()

# Dot product
magnitude = vtkImageDotProduct()
magnitude.SetInput1Data(cast2.GetOutput())
magnitude.SetInput2Data(gradient.GetOutput())
magnitude.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(magnitude.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("dot product")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
