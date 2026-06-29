#!/usr/bin/env python

# Test that large images do not cause integer overflow in texture allocation.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import numpy as np

from vtkmodules.vtkCommonDataModel import vtkImageData
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.util.numpy_support import numpy_to_vtk

# Create a large image (25000 x 25000) with a checkered pattern
width = 25000
height = 25000
square_size = 2500

# Build checkerboard efficiently with numpy
y_idx = np.arange(height) // square_size
x_idx = np.arange(width) // square_size
checker = ((x_idx[np.newaxis, :] + y_idx[:, np.newaxis]) % 2).astype(np.uint8) * 255

image = vtkImageData()
image.SetDimensions(width, height, 1)
vtk_arr = numpy_to_vtk(checker.ravel(), deep=True)
vtk_arr.SetNumberOfComponents(1)
image.GetPointData().SetScalars(vtk_arr)

# Mapper and image slice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputData(image)

image_slice = vtkImageSlice()
image_slice.SetMapper(image_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)
renderer.AddViewProp(image_slice)

# Render window
render_window = vtkRenderWindow()
render_window.SetSize(300, 301)
render_window.AddRenderer(renderer)
render_window.SetWindowName("slice mapper large image")

# Scene
camera = renderer.GetActiveCamera()
camera.ParallelProjectionOn()
renderer.ResetCamera()

# Interactor
style = vtkInteractorStyleTrackballCamera()
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)

interactor.Initialize()
interactor.Start()
