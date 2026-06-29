#!/usr/bin/env python

# Shift and scale with clamp overflow to unsigned short, then magnify.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageMagnify,
    vtkImageShiftScale,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkImageReader()
reader.GetExecutive().SetReleaseDataFlag(0, 0)
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Shift and scale with clamp overflow
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(reader.GetOutputPort())
shift_scale.SetShift(-1000.0)
shift_scale.SetScale(4.0)
shift_scale.SetOutputScalarTypeToUnsignedShort()
shift_scale.ClampOverflowOn()

# Second shift/scale
shift_scale2 = vtkImageShiftScale()
shift_scale2.SetInputConnection(shift_scale.GetOutputPort())
shift_scale2.SetShift(0)
shift_scale2.SetScale(2.0)

# Magnify
magnify = vtkImageMagnify()
magnify.SetInputConnection(shift_scale2.GetOutputPort())
magnify.SetMagnificationFactors(4, 4, 1)
magnify.InterpolateOff()
magnify.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(magnify.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("shift scale clamp overflow")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
