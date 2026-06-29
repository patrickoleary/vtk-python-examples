#!/usr/bin/env python

# Compute a weighted sum of a magnified medical image and a thresholded version.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageMagnify,
    vtkImageThreshold,
)
from vtkmodules.vtkImagingMath import vtkImageWeightedSum
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Magnify
magnify = vtkImageMagnify()
magnify.SetInputConnection(reader.GetOutputPort())
magnify.SetMagnificationFactors(4, 4, 1)

# Threshold
threshold = vtkImageThreshold()
threshold.SetInputConnection(magnify.GetOutputPort())
threshold.SetReplaceIn(1)
threshold.SetReplaceOut(1)
threshold.ThresholdBetween(-1000, 1000)
threshold.SetOutValue(0)
threshold.SetInValue(2000)

# Cast to float
cast = vtkImageCast()
cast.SetInputConnection(magnify.GetOutputPort())
cast.SetOutputScalarTypeToFloat()

cast2 = vtkImageCast()
cast2.SetInputConnection(threshold.GetOutputPort())
cast2.SetOutputScalarTypeToFloat()

# Weighted sum
weighted_sum = vtkImageWeightedSum()
weighted_sum.AddInputConnection(cast.GetOutputPort())
weighted_sum.AddInputConnection(cast2.GetOutputPort())
weighted_sum.SetWeight(0, 1)
weighted_sum.SetWeight(1, 4)
weighted_sum.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(weighted_sum.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("image weighted sum imaging")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
