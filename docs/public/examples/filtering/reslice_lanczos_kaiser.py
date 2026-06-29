#!/usr/bin/env python

# Test vtkImageReslice with Lanczos and Kaiser sinc interpolators.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageReslice,
    vtkImageSincInterpolator,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Image pipeline
reader = vtkImageReader()
reader.ReleaseDataFlagOff()
reader.SetDataByteOrderToLittleEndian()
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
reader.SetDataSpacing(3.2, 3.2, 1.5)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataMask(0x7fff)

# Rotate about the center of the image
transform = vtkTransform()
transform.Translate(+100.8, +100.8, +69.0)
transform.RotateWXYZ(10, 1, 1, 0)
transform.Translate(-100.8, -100.8, -69.0)

# Interpolators
lanczos = vtkImageSincInterpolator()
lanczos.SetWindowFunctionToLanczos()

kaiser = vtkImageSincInterpolator()
kaiser.SetWindowFunctionToKaiser()

# Lanczos with rotation
reslice1 = vtkImageReslice()
reslice1.SetInputConnection(reader.GetOutputPort())
reslice1.SetResliceTransform(transform)
reslice1.SetInterpolator(lanczos)
reslice1.SetOutputSpacing(2.0, 2.0, 1.5)
reslice1.SetOutputOrigin(-32, -32, 40)
reslice1.SetOutputExtent(0, 127, 0, 127, 0, 0)

# Lanczos without rotation
reslice2 = vtkImageReslice()
reslice2.SetInputConnection(reader.GetOutputPort())
reslice2.SetInterpolator(lanczos)
reslice2.SetOutputSpacing(2.0, 2.0, 1.5)
reslice2.SetOutputOrigin(-32, -32, 40)
reslice2.SetOutputExtent(0, 127, 0, 127, 0, 0)

# Kaiser with rotation
reslice3 = vtkImageReslice()
reslice3.SetInputConnection(reader.GetOutputPort())
reslice3.SetResliceTransform(transform)
reslice3.SetInterpolator(kaiser)
reslice3.SetOutputSpacing(2.0, 2.0, 1.5)
reslice3.SetOutputOrigin(-32, -32, 40)
reslice3.SetOutputExtent(0, 127, 0, 127, 0, 0)

# Kaiser without rotation
reslice4 = vtkImageReslice()
reslice4.SetInputConnection(reader.GetOutputPort())
reslice4.SetInterpolator(kaiser)
reslice4.SetOutputSpacing(2.0, 2.0, 1.5)
reslice4.SetOutputOrigin(-32, -32, 40)
reslice4.SetOutputExtent(0, 127, 0, 127, 0, 0)

# Mapper + Actor pairs
mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(reslice1.GetOutputPort())
mapper_0.SetColorWindow(2000)
mapper_0.SetColorLevel(1000)
mapper_0.SetZSlice(0)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(reslice2.GetOutputPort())
mapper_1.SetColorWindow(2000)
mapper_1.SetColorLevel(1000)
mapper_1.SetZSlice(0)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(reslice3.GetOutputPort())
mapper_2.SetColorWindow(2000)
mapper_2.SetColorLevel(1000)
mapper_2.SetZSlice(0)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(reslice4.GetOutputPort())
mapper_3.SetColorWindow(2000)
mapper_3.SetColorLevel(1000)
mapper_3.SetZSlice(0)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

# Renderers in four viewports
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.5, 0.0, 1.0, 0.5)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.0, 0.0, 0.5, 0.5)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.5, 0.5, 1.0, 1.0)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.0, 0.5, 0.5, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.SetSize(256, 256)
render_window.SetWindowName("reslice lanczos kaiser")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
