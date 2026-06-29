#!/usr/bin/env python

# Test vtkOpenGLImageGradient on a 3D CT volume slice.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader2
from vtkmodules.vtkImagingOpenGL2 import vtkOpenGLImageGradient
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkImageSlice,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read 3D CT volume
reader = vtkImageReader2()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))

# OpenGL image gradient filter
gradient = vtkOpenGLImageGradient()
gradient.SetInputConnection(reader.GetOutputPort())
gradient.Update()

# Display slice
image_mapper = vtkImageSliceMapper()
image_mapper.SetInputConnection(gradient.GetOutputPort())
image_mapper.SetOrientation(2)
image_mapper.SliceAtFocalPointOn()

image = vtkImageSlice()
image.SetMapper(image_mapper)
image.GetProperty().SetColorWindow(200.0)
image.GetProperty().SetColorLevel(0.0)
image.GetProperty().SetInterpolationTypeToNearest()

renderer = vtkRenderer()
renderer.AddViewProp(image)
renderer.SetBackground(0.2, 0.3, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(512, 512)
render_window.SetWindowName("opengl image gradient")

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
camera.SetParallelScale(0.8 * 128)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor_style_image = vtkInteractorStyleImage()
interactor.SetInteractorStyle(interactor_style_image)

interactor.Initialize()
interactor.Start()
