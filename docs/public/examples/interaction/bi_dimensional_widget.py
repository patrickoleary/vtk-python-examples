#!/usr/bin/env python
# Demonstrate vtkBiDimensionalWidget with 2D measurement on an image slice.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import (
    vtkBiDimensionalRepresentation2D,
    vtkBiDimensionalWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Load volume data from headsq dataset
v16 = vtkVolume16Reader()
v16.SetDataDimensions(64, 64)
v16.SetDataByteOrderToLittleEndian()
v16.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
v16.SetImageRange(1, 93)
v16.SetDataSpacing(3.2, 3.2, 1.5)
v16.Update()

# Shift and scale to unsigned char for display
scalar_range = v16.GetOutput().GetScalarRange()
shifter = vtkImageShiftScale()
shifter.SetShift(-1.0 * scalar_range[0])
shifter.SetScale(255.0 / (scalar_range[1] - scalar_range[0]))
shifter.SetOutputScalarTypeToUnsignedChar()
shifter.SetInputConnection(v16.GetOutputPort())
shifter.ReleaseDataFlagOff()
shifter.Update()

# Display image slice with vtkImageActor
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
render_window.SetWindowName("bi dimensional widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Use image interaction style for 2D
style = vtkInteractorStyleImage()
interactor.SetInteractorStyle(style)


# Callback prints measurement on end interaction
def bidimensional_callback(widget, event_string):
    rep = widget.GetRepresentation()
    length_1 = rep.GetLength1()
    length_2 = rep.GetLength2()
    print(f"Length1: {length_1:.3f}, Length2: {length_2:.3f}")


# Widget
rep = vtkBiDimensionalRepresentation2D()

bidim_widget = vtkBiDimensionalWidget()
bidim_widget.SetInteractor(interactor)
bidim_widget.SetRepresentation(rep)
bidim_widget.AddObserver("EndInteractionEvent", bidimensional_callback)
bidim_widget.On()

interactor.Initialize()
interactor.Start()
