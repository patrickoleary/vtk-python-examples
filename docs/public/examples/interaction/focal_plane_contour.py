#!/usr/bin/env python
# Demonstrate vtkContourWidget on a medical image slice using the focal plane point placer.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionWidgets import vtkContourWidget
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
volume_reader = vtkVolume16Reader()
volume_reader.SetDataDimensions(64, 64)
volume_reader.SetDataByteOrderToLittleEndian()
volume_reader.SetImageRange(1, 93)
volume_reader.SetDataSpacing(3.2, 3.2, 1.5)
volume_reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
volume_reader.ReleaseDataFlagOn()
volume_reader.SetDataMask(0x7FFF)
volume_reader.Update()

# Filter: shift and scale to unsigned char for display
scalar_range = volume_reader.GetOutput().GetScalarRange()
shifter = vtkImageShiftScale()
shifter.SetShift(-1.0 * scalar_range[0])
shifter.SetScale(255.0 / (scalar_range[1] - scalar_range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(volume_reader.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

# Actor: axial slice
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shifter.GetOutputPort())
image_actor.VisibilityOn()
image_actor.SetDisplayExtent(0, 63, 0, 63, 46, 46)
image_actor.InterpolateOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("focal plane contour")
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
contour_widget = vtkContourWidget()
contour_widget.SetInteractor(interactor)
contour_widget.On()

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0, 0, 0)
camera.SetFocalPoint(0, 0, 1)
camera.SetViewUp(0, 1, 0)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
