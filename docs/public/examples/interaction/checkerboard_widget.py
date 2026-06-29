#!/usr/bin/env python
# Demonstrate vtkCheckerboardWidget with two synthetic images in a checkerboard pattern.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageWrapPad
from vtkmodules.vtkImagingGeneral import vtkImageCheckerboard
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionWidgets import (
    vtkCheckerboardRepresentation,
    vtkCheckerboardWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create first synthetic image (yellow)
image_1 = vtkImageCanvasSource2D()
image_1.SetNumberOfScalarComponents(3)
image_1.SetScalarTypeToUnsignedChar()
image_1.SetExtent(0, 511, 0, 511, 0, 0)
image_1.SetExtent(0, 511, 0, 0, 0, 511)
image_1.SetDrawColor(255, 255, 0)
image_1.FillBox(0, 511, 0, 511)

pad_1 = vtkImageWrapPad()
pad_1.SetInputConnection(image_1.GetOutputPort())
pad_1.SetOutputWholeExtent(0, 511, 0, 511, 0, 0)

# Create second synthetic image (cyan)
image_2 = vtkImageCanvasSource2D()
image_2.SetNumberOfScalarComponents(3)
image_2.SetScalarTypeToUnsignedChar()
image_2.SetExtent(0, 511, 0, 511, 0, 0)
image_2.SetDrawColor(0, 255, 255)
image_2.FillBox(0, 511, 0, 511)

pad_2 = vtkImageWrapPad()
pad_2.SetInputConnection(image_2.GetOutputPort())
pad_2.SetOutputWholeExtent(0, 511, 0, 511, 0, 0)

# Create checkerboard from the two images
checkers = vtkImageCheckerboard()
checkers.SetInputConnection(0, pad_1.GetOutputPort())
checkers.SetInputConnection(1, pad_2.GetOutputPort())
checkers.SetNumberOfDivisions(10, 6, 1)

checkerboard_actor = vtkImageActor()
checkerboard_actor.GetMapper().SetInputConnection(checkers.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(checkerboard_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("checkerboard widget")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
rep = vtkCheckerboardRepresentation()
rep.SetImageActor(checkerboard_actor)
rep.SetCheckerboard(checkers)
rep.GetLeftRepresentation().SetTitleText("Left")
rep.GetRightRepresentation().SetTitleText("Right")
rep.GetTopRepresentation().SetTitleText("Top")
rep.GetBottomRepresentation().SetTitleText("Bottom")
rep.SetCornerOffset(0.2)

checkerboard_widget = vtkCheckerboardWidget()
checkerboard_widget.SetInteractor(interactor)
checkerboard_widget.SetRepresentation(rep)
checkerboard_widget.On()

interactor.Initialize()
interactor.Start()
