#!/usr/bin/env python
# Demonstrate vtkAffineWidget with vtkAffineRepresentation2D on an image actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import (
    vtkAffineRepresentation2D,
    vtkAffineWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Load volume data from headsq dataset
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)

# Shift and scale image data to unsigned char range for display
shift_scale = vtkImageShiftScale()
shift_scale.SetInputConnection(v16.GetOutputPort())
shift_scale.SetShift(0)
shift_scale.SetScale(0.07)
shift_scale.SetOutputScalarTypeToUnsignedChar()

# Display image slice with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shift_scale.GetOutputPort())
image_actor.SetDisplayExtent(0, 63, 0, 63, 46, 46)

# Renderer
renderer = vtkRenderer()
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.AddActor(image_actor)
renderer.SetBackground(0, 0, 0)
renderer.ResetCamera()

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("affine widget")
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Use image interaction style for 2D interaction
style = vtkInteractorStyleImage()
interactor.SetInteractorStyle(style)

# Create affine transform for the callback
transform = vtkTransform()


def affine_callback(widget, event_string):
    rep = widget.GetRepresentation()
    rep.GetTransform(transform)
    image_actor.SetUserTransform(transform)


# Widget
affine_rep = vtkAffineRepresentation2D()

affine_widget = vtkAffineWidget()
affine_widget.SetInteractor(interactor)
affine_widget.SetRepresentation(affine_rep)
affine_widget.AddObserver("InteractionEvent", affine_callback)
affine_widget.AddObserver("EndInteractionEvent", affine_callback)
affine_widget.On()

interactor.Initialize()
interactor.Start()
