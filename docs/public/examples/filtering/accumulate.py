#!/usr/bin/env python

# Accumulate a smoothed image histogram using vtkImageAccumulate.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkPNGReader
from vtkmodules.vtkImagingCore import (
    vtkImageAppendComponents,
    vtkImageClip,
    vtkImageShiftScale,
)
from vtkmodules.vtkImagingGeneral import vtkImageGaussianSmooth
from vtkmodules.vtkImagingStatistics import vtkImageAccumulate
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

# Smooth
smooth = vtkImageGaussianSmooth()
smooth.SetDimensionality(2)
smooth.SetStandardDeviations(1, 1)
smooth.SetInputConnection(reader.GetOutputPort())

# Append original and smoothed
image_append = vtkImageAppendComponents()
image_append.AddInputConnection(reader.GetOutputPort())
image_append.AddInputConnection(smooth.GetOutputPort())

# Clip
clip = vtkImageClip()
clip.SetInputConnection(image_append.GetOutputPort())
clip.SetOutputWholeExtent(0, 255, 0, 255, 20, 22)

# Accumulate histogram
accum = vtkImageAccumulate()
accum.SetInputConnection(clip.GetOutputPort())
accum.SetComponentExtent(0, 255, 0, 255, 0, 0)
accum.SetComponentSpacing(1, 1, 0.0)
accum.Update()

# Scale histogram values so they are visible
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(accum.GetOutputPort())
shift_scale.SetShift(0)
shift_scale.SetScale(20)
shift_scale.SetOutputScalarTypeToUnsignedChar()
shift_scale.ClampOverflowOn()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shift_scale.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("accumulate")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
