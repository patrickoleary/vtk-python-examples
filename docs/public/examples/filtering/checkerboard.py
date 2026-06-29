#!/usr/bin/env python

# Create a checkerboard pattern from two colored canvas images.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageWrapPad
from vtkmodules.vtkImagingGeneral import vtkImageCheckerboard
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Yellow canvas
image1 = vtkImageCanvasSource2D()
image1.SetNumberOfScalarComponents(3)
image1.SetScalarTypeToUnsignedChar()
image1.SetExtent(0, 511, 0, 511, 0, 0)
image1.SetDrawColor(255, 255, 0)
image1.FillBox(0, 511, 0, 511)

pad1 = vtkImageWrapPad()
pad1.SetInputConnection(image1.GetOutputPort())
pad1.SetOutputWholeExtent(0, 511, 0, 511, 0, 10)
pad1.Update()

# Cyan canvas
image2 = vtkImageCanvasSource2D()
image2.SetNumberOfScalarComponents(3)
image2.SetScalarTypeToUnsignedChar()
image2.SetExtent(0, 511, 0, 511, 0, 0)
image2.SetDrawColor(0, 255, 255)
image2.FillBox(0, 511, 0, 511)

pad2 = vtkImageWrapPad()
pad2.SetInputConnection(image2.GetOutputPort())
pad2.SetOutputWholeExtent(0, 511, 0, 511, 0, 10)
pad2.Update()

# Checkerboard
checkers = vtkImageCheckerboard()
checkers.SetInput1Data(pad1.GetOutput())
checkers.SetInput2Data(pad2.GetOutput())
checkers.SetNumberOfDivisions(11, 6, 0)
checkers.Update()

# Display with vtkImageActor
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputConnection(checkers.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(image_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(256, 256)
render_window.SetWindowName("checkerboard")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
