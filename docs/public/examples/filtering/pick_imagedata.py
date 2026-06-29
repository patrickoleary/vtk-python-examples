#!/usr/bin/env python

# Test picking on image data using vtkImageSliceMapper.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingCore import vtkImageWrapPad
from vtkmodules.vtkImagingGeneral import vtkImageCheckerboard
from vtkmodules.vtkImagingSources import vtkImageCanvasSource2D
from vtkmodules.vtkRenderingCore import (
    vtkCellPicker,
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkPicker,
    vtkPointPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
size = 400

image_1 = vtkImageCanvasSource2D()
image_1.SetNumberOfScalarComponents(3)
image_1.SetScalarTypeToUnsignedChar()
image_1.SetExtent(0, size, 0, size, 0, 0)
image_1.SetDrawColor(255, 255, 0)
image_1.FillBox(0, size, 0, size)

pad_1 = vtkImageWrapPad()
pad_1.SetInputConnection(image_1.GetOutputPort())
pad_1.SetOutputWholeExtent(0, size, 0, size, 0, 10)
pad_1.Update()

image_2 = vtkImageCanvasSource2D()
image_2.SetNumberOfScalarComponents(3)
image_2.SetScalarTypeToUnsignedChar()
image_2.SetExtent(0, size, 0, size, 0, 0)
image_2.SetDrawColor(0, 255, 255)
image_2.FillBox(0, size, 0, size)

pad_2 = vtkImageWrapPad()
pad_2.SetInputConnection(image_2.GetOutputPort())
pad_2.SetOutputWholeExtent(0, size, 0, size, 0, 10)
pad_2.Update()

checkers = vtkImageCheckerboard()
checkers.SetInput1Data(pad_1.GetOutput())
checkers.SetInput2Data(pad_2.GetOutput())
checkers.SetNumberOfDivisions(11, 6, 0)

mapper = vtkImageSliceMapper()
mapper.SetInputConnection(checkers.GetOutputPort())
mapper.SliceAtFocalPointOn()
mapper.SliceFacesCameraOn()

image_slice = vtkImageSlice()
image_slice.SetMapper(mapper)
image_slice.GetProperty().SetColorLevel(127.5)
image_slice.GetProperty().SetColorWindow(255)

renderer = vtkRenderer()
renderer.AddViewProp(image_slice)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("pick imagedata")
render_window.SetMultiSamples(0)
render_window.SetSize(size, size)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

render_window.Render()

# Perform picks
point_picker = vtkPointPicker()
cell_picker = vtkCellPicker()
prop_picker = vtkPicker()

for (i, j, cid, pid) in ((20, 40, -1, -1), (160, 100, 821341, 825800), (240, 300, 938658, 943010)):
    pos = [i, j]
    prop_picker.Pick(pos[0], pos[1], 0, renderer)
    cell_picker.Pick(pos[0], pos[1], 0, renderer)
    point_picker.Pick(pos[0], pos[1], 0, renderer)

interactor.Initialize()
interactor.Start()
