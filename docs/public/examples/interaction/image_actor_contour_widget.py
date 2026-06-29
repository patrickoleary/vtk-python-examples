#!/usr/bin/env python
# Demonstrate vtkContourWidget with vtkImageActorPointPlacer and a slice slider on medical image data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkIOImage import vtkVolume16Reader
from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkInteractionWidgets import (
    vtkContourWidget,
    vtkImageActorPointPlacer,
    vtkOrientedGlyphContourRepresentation,
    vtkSliderRepresentation2D,
    vtkSliderWidget,
)
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

# Actor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(shifter.GetOutputPort())

extent = shifter.GetOutput().GetExtent()
slice_min = extent[4]
slice_max = extent[5]
initial_slice = (slice_min + slice_max) // 2
image_actor.SetDisplayExtent(extent[0], extent[1], extent[2], extent[3], initial_slice, initial_slice)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("image actor contour widget")
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)


# Callback: slider changes slice
def slider_callback(caller, event):
    value = int(caller.GetRepresentation().GetValue())
    image_actor.SetDisplayExtent(
        extent[0], extent[1], extent[2], extent[3], value, value
    )


# Widget: slice slider
slider_rep = vtkSliderRepresentation2D()
slider_rep.SetMinimumValue(slice_min)
slider_rep.SetMaximumValue(slice_max)
slider_rep.SetValue(initial_slice)
slider_rep.SetTitleText("Slice")
slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint1Coordinate().SetValue(0.3, 0.05)
slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
slider_rep.GetPoint2Coordinate().SetValue(0.7, 0.05)
slider_rep.SetSliderLength(0.02)
slider_rep.SetSliderWidth(0.03)
slider_rep.SetEndCapLength(0.01)
slider_rep.SetEndCapWidth(0.03)
slider_rep.SetTubeWidth(0.005)
slider_rep.SetTitleHeight(0.02)
slider_rep.SetLabelHeight(0.02)

slider_widget = vtkSliderWidget()
slider_widget.SetInteractor(interactor)
slider_widget.SetRepresentation(slider_rep)
slider_widget.KeyPressActivationOff()
slider_widget.SetAnimationModeToAnimate()
slider_widget.AddObserver(vtkCommand.InteractionEvent, slider_callback)
slider_widget.SetEnabled(True)

# Widget: contour with image actor point placer
contour_rep = vtkOrientedGlyphContourRepresentation()

image_actor_point_placer = vtkImageActorPointPlacer()
image_actor_point_placer.SetImageActor(image_actor)
contour_rep.SetPointPlacer(image_actor_point_placer)
contour_rep.GetProperty().SetColor(0, 1, 0)

contour_widget = vtkContourWidget()
contour_widget.SetRepresentation(contour_rep)
contour_widget.SetInteractor(interactor)
contour_widget.SetEnabled(True)
contour_widget.ProcessEventsOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
