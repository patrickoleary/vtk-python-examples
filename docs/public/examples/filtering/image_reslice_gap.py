#!/usr/bin/env python

# Test vtkImageReslice gap bug fix with a near-0.5 shift transform.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_UNSIGNED_CHAR
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkImagingCore import (
    vtkImageCast,
    vtkImageReslice,
)
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a solid input image, two slices thick
image = vtkImageData()
image.SetDimensions(5, 4, 2)
image.AllocateScalars(VTK_UNSIGNED_CHAR, 1)
image.GetPointData().GetScalars().Fill(255)

# Shift by just under 0.5 to trigger the bug if present
transform = vtkTransform()
transform.Translate(1.0, 1.0, 0.499999)

# Upstream filter (needed to trigger the bug)
upstream = vtkImageCast()
upstream.SetInputData(image)
upstream.SetOutputScalarTypeToShort()

# Reslice
reslice = vtkImageReslice()
reslice.SetInputConnection(upstream.GetOutputPort())
reslice.SetResliceTransform(transform)

# Display
actor = vtkImageActor()
actor.GetMapper().SetInputConnection(reslice.GetOutputPort())

renderer = vtkRenderer()
renderer.AddViewProp(actor)
renderer.SetBackground(0.2, 0.1, 1.0)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("image reslice gap")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
