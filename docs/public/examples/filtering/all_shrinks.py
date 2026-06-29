#!/usr/bin/env python

# Test vtkImageShrink3D with minimum, maximum, mean, median, and no-op modes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageMagnify,
    vtkImageShrink3D,
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
reader.SetDataExtent(0, 63, 0, 63, 1, 93)
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

reader.SetFilePrefix(os.path.join(data_dir, "headsq", "quarter"))
reader.SetDataByteOrderToLittleEndian()
reader.SetDataMask(0x7fff)

# Minimum
shrink_filter_0 = vtkImageShrink3D()
shrink_filter_0.SetMean(0)
shrink_filter_0.MinimumOn()
shrink_filter_0.SetShrinkFactors(4, 4, 4)
shrink_filter_0.SetInputConnection(reader.GetOutputPort())

magnify_0 = vtkImageMagnify()
magnify_0.SetMagnificationFactors(8, 8, 8)
magnify_0.InterpolateOff()
magnify_0.SetInputConnection(shrink_filter_0.GetOutputPort())

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(magnify_0.GetOutputPort())
mapper_0.SetColorWindow(2000)
mapper_0.SetColorLevel(1000)
mapper_0.SetZSlice(45)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0, 0, .5, .33)

# Maximum
shrink_filter_1 = vtkImageShrink3D()
shrink_filter_1.SetMean(0)
shrink_filter_1.MaximumOn()
shrink_filter_1.SetShrinkFactors(4, 4, 4)
shrink_filter_1.SetInputConnection(reader.GetOutputPort())

magnify_1 = vtkImageMagnify()
magnify_1.SetMagnificationFactors(8, 8, 8)
magnify_1.InterpolateOff()
magnify_1.SetInputConnection(shrink_filter_1.GetOutputPort())

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(magnify_1.GetOutputPort())
mapper_1.SetColorWindow(2000)
mapper_1.SetColorLevel(1000)
mapper_1.SetZSlice(45)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0, .33, .5, .667)

# Mean
shrink_filter_2 = vtkImageShrink3D()
shrink_filter_2.SetMean(0)
shrink_filter_2.MeanOn()
shrink_filter_2.SetShrinkFactors(4, 4, 4)
shrink_filter_2.SetInputConnection(reader.GetOutputPort())

magnify_2 = vtkImageMagnify()
magnify_2.SetMagnificationFactors(8, 8, 8)
magnify_2.InterpolateOff()
magnify_2.SetInputConnection(shrink_filter_2.GetOutputPort())

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(magnify_2.GetOutputPort())
mapper_2.SetColorWindow(2000)
mapper_2.SetColorLevel(1000)
mapper_2.SetZSlice(45)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(.5, 0, 1, .33)

# Median
shrink_filter_3 = vtkImageShrink3D()
shrink_filter_3.SetMean(0)
shrink_filter_3.MedianOn()
shrink_filter_3.SetShrinkFactors(4, 4, 4)
shrink_filter_3.SetInputConnection(reader.GetOutputPort())

magnify_3 = vtkImageMagnify()
magnify_3.SetMagnificationFactors(8, 8, 8)
magnify_3.InterpolateOff()
magnify_3.SetInputConnection(shrink_filter_3.GetOutputPort())

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(magnify_3.GetOutputPort())
mapper_3.SetColorWindow(2000)
mapper_3.SetColorLevel(1000)
mapper_3.SetZSlice(45)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(.5, .33, 1, .667)

# NoOp
shrink_filter_4 = vtkImageShrink3D()
shrink_filter_4.SetMean(0)
shrink_filter_4.SetShrinkFactors(4, 4, 4)
shrink_filter_4.SetInputConnection(reader.GetOutputPort())

magnify_4 = vtkImageMagnify()
magnify_4.SetMagnificationFactors(8, 8, 8)
magnify_4.InterpolateOff()
magnify_4.SetInputConnection(shrink_filter_4.GetOutputPort())

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(magnify_4.GetOutputPort())
mapper_4.SetColorWindow(2000)
mapper_4.SetColorLevel(1000)
mapper_4.SetZSlice(45)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(0, .667, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.SetSize(256, 384)
render_window.SetWindowName("all shrinks")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
