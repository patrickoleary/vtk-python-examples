#!/usr/bin/env python

# Test vtkImageSliceMapper with large origin values and rotated direction matrix.

import os

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkImageActor,
    vtkImageSliceMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read TIFF image
tiff_reader = vtkTIFFReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

tiff_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
tiff_reader.SetOrientationType(4)
tiff_reader.Update()
input_image = tiff_reader.GetOutput()

# Modify origin with very large values to test precision
origin = [999999999.12, 999999999.12, 999999999.12]
input_image.SetOrigin(origin)

# Apply rotation to direction matrix to expose precision issues
transform = vtkTransform()
transform.RotateX(15.0)
transform.RotateZ(16.0)
m = transform.GetMatrix()
input_image.SetDirectionMatrix(
    m.GetElement(0, 0), m.GetElement(0, 1), m.GetElement(0, 2),
    m.GetElement(1, 0), m.GetElement(1, 1), m.GetElement(1, 2),
    m.GetElement(2, 0), m.GetElement(2, 1), m.GetElement(2, 2),
)

# Map with double precision to avoid precision issues
slice_mapper = vtkImageSliceMapper()
slice_mapper.SetInputData(input_image)
slice_mapper.SetOutputPointsPrecision(vtkImageSliceMapper.DOUBLE_PRECISION)

image_actor = vtkImageActor()
image_actor.SetMapper(slice_mapper)

renderer = vtkRenderer()
renderer.AddActor(image_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("image slice mapper")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.GetActiveCamera().SetFocalPoint(input_image.GetCenter())
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
