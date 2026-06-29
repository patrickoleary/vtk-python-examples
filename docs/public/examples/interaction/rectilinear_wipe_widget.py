#!/usr/bin/env python
# Demonstrate vtkRectilinearWipeWidget with two canvas images.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageWrapPad
from vtkmodules.vtkImagingHybrid import vtkImageRectilinearWipe
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkInteractionWidgets import (
    vtkRectilinearWipeRepresentation,
    vtkRectilinearWipeWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sources
image_1 = vtkImageCanvasSource2D()
image_1.SetNumberOfScalarComponents(3)
image_1.SetScalarTypeToUnsignedChar()
image_1.SetExtent(0, 511, 0, 511, 0, 0)
image_1.SetDrawColor(255, 255, 0)
image_1.FillBox(0, 511, 0, 511)

pad_1 = vtkImageWrapPad()
pad_1.SetInputConnection(image_1.GetOutputPort())
pad_1.SetOutputWholeExtent(0, 511, 0, 511, 0, 0)

image_2 = vtkImageCanvasSource2D()
image_2.SetNumberOfScalarComponents(3)
image_2.SetScalarTypeToUnsignedChar()
image_2.SetExtent(0, 511, 0, 511, 0, 0)
image_2.SetDrawColor(0, 255, 255)
image_2.FillBox(0, 511, 0, 511)

pad_2 = vtkImageWrapPad()
pad_2.SetInputConnection(image_2.GetOutputPort())
pad_2.SetOutputWholeExtent(0, 511, 0, 511, 0, 0)

# Filter
wipe = vtkImageRectilinearWipe()
wipe.SetInputConnection(0, pad_1.GetOutputPort())
wipe.SetInputConnection(1, pad_2.GetOutputPort())
wipe.SetPosition(100, 256)
wipe.SetWipe(0)

# Actor
wipe_actor = vtkImageActor()
wipe_actor.GetMapper().SetInputConnection(wipe.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(wipe_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("rectilinear wipe widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
wipe_widget = vtkRectilinearWipeWidget()
wipe_widget.SetInteractor(interactor)

wipe_widget_rep = wipe_widget.GetRepresentation()
wipe_widget_rep.SetImageActor(wipe_actor)
wipe_widget_rep.SetRectilinearWipe(wipe)
wipe_widget_rep.GetProperty().SetLineWidth(2.0)
wipe_widget_rep.GetProperty().SetOpacity(0.75)
wipe_widget.On()

interactor.Initialize()
interactor.Start()
