#!/usr/bin/env python

# Demonstrate vtkMathTextUtilities::RenderString with matplotlib backend.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
import vtkmodules.vtkRenderingMatplotlib  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTextProperty,
)
from vtkmodules.vtkRenderingFreeType import vtkMathTextUtilities

# Render a LaTeX math string to an image
math_string = (
    "$\\hat{H}\\psi = \\left(-\\frac{\\hbar}{2m}\\nabla^2"
    " + V(r)\\right) \\psi = \\psi\\cdot E $"
)

image = vtkImageData()
utils = vtkMathTextUtilities()
utils.SetScaleToPowerOfTwo(False)

tprop = vtkTextProperty()
tprop.SetColor(1, 1, 1)
tprop.SetFontSize(50)

# Need a render window for DPI
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetWindowName("string")

utils.RenderString(math_string, image, tprop, render_window.GetDPI())

# Display with standard rendering pipeline (no vtkImageViewer2)
image_actor = vtkImageActor()
image_actor.GetMapper().SetInputData(image)

renderer = vtkRenderer()
renderer.AddActor(image_actor)

render_window.AddRenderer(renderer)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(6.0)

interactor.Initialize()
interactor.Start()
