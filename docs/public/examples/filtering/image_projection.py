#!/usr/bin/env python

# Test vtkImageSlab with various projection operations and orientations.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageReslice
from vtkmodules.vtkImagingGeneral import vtkImageSlab
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

# Mean slab along Z with trapezoid integration
slab1 = vtkImageSlab()
slab1.SetInputConnection(reader.GetOutputPort())
slab1.SetOperationToMean()
slab1.TrapezoidIntegrationOn()
slab1.SetOrientationToZ()

# Max slab along Z
slab2 = vtkImageSlab()
slab2.SetInputConnection(reader.GetOutputPort())
slab2.SetOperationToMax()
slab2.MultiSliceOutputOff()
slab2.SetOutputScalarTypeToInputScalarType()

# Sum slab along X with reslice
slab3 = vtkImageSlab()
slab3.SetInputConnection(reader.GetOutputPort())
slab3.SetOperationToSum()
slab3.SetOrientationToX()
slab3.MultiSliceOutputOn()
slab3.SetOutputScalarTypeToDouble()

reslice3 = vtkImageReslice()
reslice3.SetInputConnection(slab3.GetOutputPort())
reslice3.SetResliceAxesDirectionCosines([0, 1, 0, 0, 0, -1, 1, 0, 0])
reslice3.SetOutputSpacing(3.2, 3.2, 3.2)
reslice3.SetOutputExtent(0, 74, 0, 74, 0, 0)

# Max slab along X with reslice
slab4 = vtkImageSlab()
slab4.SetInputConnection(reader.GetOutputPort())
slab4.SetOperationToMax()
slab4.SetOrientation(0)
slab4.MultiSliceOutputOn()
slab4.SetOutputScalarTypeToFloat()

reslice4 = vtkImageReslice()
reslice4.SetInputConnection(slab4.GetOutputPort())
reslice4.SetResliceAxesDirectionCosines([0, 1, 0, 0, 0, -1, 1, 0, 0])
reslice4.SetOutputSpacing(3.2, 3.2, 3.2)
reslice4.SetOutputExtent(0, 74, 0, 74, 0, 0)

# Mean slab along Y with reslice
slab5 = vtkImageSlab()
slab5.SetInputConnection(reader.GetOutputPort())
slab5.SetOperationToMean()
slab5.SetOrientationToY()
slab5.MultiSliceOutputOn()

reslice5 = vtkImageReslice()
reslice5.SetInputConnection(slab5.GetOutputPort())
reslice5.SetResliceAxesDirectionCosines([1, 0, 0, 0, 0, -1, 0, 1, 0])
reslice5.SetOutputSpacing(3.2, 3.2, 3.2)
reslice5.SetOutputExtent(0, 74, 0, 74, 0, 0)

# Max slab along Y with reslice
slab6 = vtkImageSlab()
slab6.SetInputConnection(reader.GetOutputPort())
slab6.SetOperationToMax()
slab6.SetOrientation(1)
slab6.MultiSliceOutputOn()

reslice6 = vtkImageReslice()
reslice6.SetInputConnection(slab6.GetOutputPort())
reslice6.SetResliceAxesDirectionCosines([1, 0, 0, 0, 0, -1, 0, 1, 0])
reslice6.SetOutputSpacing(3.2, 3.2, 3.2)
reslice6.SetOutputExtent(0, 74, 0, 74, 0, 0)

# Mapper/Actor pairs
mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(slab1.GetOutputPort())
mapper_0.SetColorWindow(2000)
mapper_0.SetColorLevel(1000)
mapper_0.SetZSlice(0)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(slab2.GetOutputPort())
mapper_1.SetColorWindow(2000)
mapper_1.SetColorLevel(1000)
mapper_1.SetZSlice(0)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(reslice3.GetOutputPort())
mapper_2.SetColorWindow(128000)
mapper_2.SetColorLevel(64000)
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

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(reslice5.GetOutputPort())
mapper_4.SetColorWindow(2000)
mapper_4.SetColorLevel(1000)
mapper_4.SetZSlice(0)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(reslice6.GetOutputPort())
mapper_5.SetColorWindow(2000)
mapper_5.SetColorLevel(1000)
mapper_5.SetZSlice(0)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

# Renderers in six viewports (3x2 grid)
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.3333, 0.5)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.0, 0.5, 0.3333, 1.0)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.3333, 0.0, 0.6667, 0.5)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.3333, 0.5, 0.6667, 1.0)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(0.6667, 0.0, 1.0, 0.5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(0.6667, 0.5, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(230, 150)
render_window.SetWindowName("image projection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
