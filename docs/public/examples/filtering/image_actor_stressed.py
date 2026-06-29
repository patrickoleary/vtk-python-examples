#!/usr/bin/env python

# Stress test vtkImageActor with various image extents and texture sizes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageShiftScale
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# First: changing display extent without changing size (reuses texture)
gs_one = vtkImageEllipsoidSource()
gs_one.SetWholeExtent(0, 999, 0, 999, 0, 0)
gs_one.SetCenter(500, 500, 0)
gs_one.SetRadius(300, 400, 0)
gs_one.SetInValue(0)
gs_one.SetOutValue(255)
gs_one.SetOutputScalarTypeToUnsignedChar()

ss_one = vtkImageShiftScale()
ss_one.SetInputConnection(gs_one.GetOutputPort())
ss_one.SetOutputScalarTypeToUnsignedChar()
ss_one.SetShift(0)
ss_one.SetScale(1)
ss_one.UpdateWholeExtent()

ia_one = vtkImageActor()
ia_one.GetMapper().SetInputConnection(ss_one.GetOutputPort())

# Second: really large texture
gs_two = vtkImageEllipsoidSource()
gs_two.SetWholeExtent(1000, 8999, 1000, 8999, 0, 0)
gs_two.SetCenter(4000, 4000, 0)
gs_two.SetRadius(1800, 1800, 0)
gs_two.SetInValue(250)
gs_two.SetOutValue(150)
gs_two.SetOutputScalarTypeToUnsignedChar()

ss_two = vtkImageShiftScale()
ss_two.SetInputConnection(gs_two.GetOutputPort())
ss_two.SetOutputScalarTypeToUnsignedChar()
ss_two.SetShift(0)
ss_two.SetScale(1)
ss_two.UpdateWholeExtent()

ia_two = vtkImageActor()
ia_two.GetMapper().SetInputConnection(ss_two.GetOutputPort())
ia_two.SetScale(0.1, 0.1, 1.0)
ia_two.AddPosition(1000, 1000, 0)

# Third: changing input and power of two texture
gs_three = vtkImageEllipsoidSource()
gs_three.SetWholeExtent(0, 511, 2000, 2511, 0, 0)
gs_three.SetCenter(255, 2255, 0)
gs_three.SetRadius(100, 200, 0)
gs_three.SetInValue(250)
gs_three.SetOutValue(0)
gs_three.SetOutputScalarTypeToUnsignedChar()

ss_three = vtkImageShiftScale()
ss_three.SetInputConnection(gs_three.GetOutputPort())
ss_three.SetOutputScalarTypeToUnsignedChar()
ss_three.SetShift(0)
ss_three.SetScale(1)
ss_three.UpdateWholeExtent()

ia_three = vtkImageActor()
ia_three.GetMapper().SetInputConnection(ss_three.GetOutputPort())

# Fourth: contiguous power-of-two display extents
gs_four = vtkImageEllipsoidSource()
gs_four.SetWholeExtent(2000, 2511, 0, 511, 0, 0)
gs_four.SetCenter(2255, 255, 0)
gs_four.SetRadius(130, 130, 0)
gs_four.SetInValue(40)
gs_four.SetOutValue(190)
gs_four.SetOutputScalarTypeToUnsignedChar()

ss_four = vtkImageShiftScale()
ss_four.SetInputConnection(gs_four.GetOutputPort())
ss_four.SetOutputScalarTypeToUnsignedChar()
ss_four.SetShift(0)
ss_four.SetScale(1)
ss_four.UpdateWholeExtent()

ia_four = vtkImageActor()
ia_four.GetMapper().SetInputConnection(ss_four.GetOutputPort())

# Fifth: contiguous non-power-of-two display extents
gs_five = vtkImageEllipsoidSource()
gs_five.SetWholeExtent(1200, 1712, 0, 512, 0, 0)
gs_five.SetCenter(1456, 256, 0)
gs_five.SetRadius(130, 180, 0)
gs_five.SetInValue(190)
gs_five.SetOutValue(100)
gs_five.SetOutputScalarTypeToUnsignedChar()

ss_five = vtkImageShiftScale()
ss_five.SetInputConnection(gs_five.GetOutputPort())
ss_five.SetOutputScalarTypeToUnsignedChar()
ss_five.SetShift(0)
ss_five.SetScale(1)
ss_five.UpdateWholeExtent()

ia_five = vtkImageActor()
ia_five.GetMapper().SetInputConnection(ss_five.GetOutputPort())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(ia_one)
renderer.AddActor(ia_two)
renderer.AddActor(ia_three)
renderer.AddActor(ia_four)
renderer.AddActor(ia_five)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("image actor stressed")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# First render initializes textures
render_window.Render()

# Stress test: change display extents and input
ia_one.SetDisplayExtent(200, 999, 200, 999, 0, 0)
ia_four.SetDisplayExtent(2000, 2511, 0, 300, 0, 0)
ia_five.SetDisplayExtent(1200, 1712, 0, 300, 0, 0)
gs_three.SetRadius(120, 120, 0)
render_window.Render()

ia_one.SetDisplayExtent(0, 799, 0, 799, 0, 0)
ia_four.SetDisplayExtent(2000, 2511, 200, 500, 0, 0)
ia_five.SetDisplayExtent(1200, 1712, 200, 500, 0, 0)
gs_three.SetRadius(150, 150, 0)

interactor.Initialize()
interactor.Start()
