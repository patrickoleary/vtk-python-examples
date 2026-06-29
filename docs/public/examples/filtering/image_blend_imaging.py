#!/usr/bin/env python

# Test vtkImageBlend with two procedurally generated RGBA images.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import VTK_UNSIGNED_SHORT
from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkImagingCore import vtkImageBlend
from vtkmodules.vtkRenderingCore import (
    vtkImageSliceMapper,
    vtkImageSlice,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

dims = [256, 256, 4]

# First image: gradient pattern on left half
image_data1 = vtkImageData()
image_data1.SetDimensions(dims)
image_data1.SetSpacing(1, 1, 1)
image_data1.SetOrigin(0, 0, 0)
image_data1.AllocateScalars(VTK_UNSIGNED_SHORT, 4)

for x in range(dims[0]):
    for y in range(dims[1]):
        if x < dims[0] // 2:
            val = abs((dims[0] - x - 100) * (dims[1] - y - 100))
        else:
            val = 0
        image_data1.SetScalarComponentFromFloat(x, y, 0, 0, val)
        image_data1.SetScalarComponentFromFloat(x, y, 0, 1, val)
        image_data1.SetScalarComponentFromFloat(x, y, 0, 2, val)
        image_data1.SetScalarComponentFromFloat(x, y, 0, 3, val)

# Second image: square pattern in center
image_data2 = vtkImageData()
image_data2.SetDimensions(dims)
image_data2.SetSpacing(1, 1, 1)
image_data2.SetOrigin(0, 0, 0)
image_data2.AllocateScalars(VTK_UNSIGNED_SHORT, 4)

for x in range(dims[0]):
    for y in range(dims[1]):
        if (x > (dims[0] // 2) - 50 and x < (dims[0] // 2) + 50
                and y > (dims[1] // 2) - 50 and y < (dims[1] // 2) + 50):
            val = x * y
        else:
            val = 0
        image_data2.SetScalarComponentFromFloat(x, y, 0, 0, val)
        image_data2.SetScalarComponentFromFloat(x, y, 0, 1, val)
        image_data2.SetScalarComponentFromFloat(x, y, 0, 2, val)
        image_data2.SetScalarComponentFromFloat(x, y, 0, 3, val)

# Blend
blend = vtkImageBlend()
blend.AddInputData(image_data1)
blend.AddInputData(image_data2)
blend.SetOpacity(0, 0.3)
blend.SetOpacity(1, 0.7)
blend.SetBlendModeToNormal()
blend.BlendAlphaOn()

# Display with vtkImageSlice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(blend.GetOutputPort())
image_mapper.BorderOn()

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)

color_range = [0, 4095]
image_slice.GetProperty().SetColorWindow(color_range[1] - color_range[0])
image_slice.GetProperty().SetColorLevel(0.5 * (color_range[0] + color_range[1]))
image_slice.GetProperty().SetInterpolationTypeToNearest()

renderer = vtkRenderer()
renderer.AddViewProp(image_slice)
renderer.SetBackground(0.0, 0.0, 0.0)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("image blend imaging")

# Scene
bounds = image_mapper.GetBounds()
point = [
    0.5 * (bounds[0] + bounds[1]),
    0.5 * (bounds[2] + bounds[3]),
    0.5 * (bounds[4] + bounds[5]),
]
camera = renderer.GetActiveCamera()
camera.SetFocalPoint(point)
point[image_mapper.GetOrientation()] += 500.0
camera.SetPosition(point)
camera.SetViewUp(0.0, 1.0, 0.0)
camera.ParallelProjectionOn()
camera.SetParallelScale(128)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
