#!/usr/bin/env python

# Test vtkImageMaskBits with various bitwise operators on a color image.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkImagingCore import vtkImageShrink3D
from vtkmodules.vtkImagingMath import vtkImageMaskBits
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read and shrink image
image1 = vtkTIFFReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

image1.SetFileName(os.path.join(data_dir, "beach.tif"))
image1.SetOrientationType(4)

shrink = vtkImageShrink3D()
shrink.SetInputConnection(image1.GetOutputPort())
shrink.SetShrinkFactors(2, 2, 1)

# ByPass (no mask)
mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(shrink.GetOutputPort())
mapper_0.SetColorWindow(255)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.0, 1.0 / 3.0, 0.5)

# And
mask_bits_1 = vtkImageMaskBits()
mask_bits_1.SetInputConnection(shrink.GetOutputPort())
mask_bits_1.SetOperationToAnd()
mask_bits_1.SetMasks(255, 255, 0)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(mask_bits_1.GetOutputPort())
mapper_1.SetColorWindow(255)
mapper_1.SetColorLevel(127.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(1.0 / 3.0, 0.0, 2.0 / 3.0, 0.5)

# Nand
mask_bits_2 = vtkImageMaskBits()
mask_bits_2.SetInputConnection(shrink.GetOutputPort())
mask_bits_2.SetOperationToNand()
mask_bits_2.SetMasks(255, 255, 0)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(mask_bits_2.GetOutputPort())
mapper_2.SetColorWindow(255)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(2.0 / 3.0, 0.0, 1.0, 0.5)

# Xor
mask_bits_3 = vtkImageMaskBits()
mask_bits_3.SetInputConnection(shrink.GetOutputPort())
mask_bits_3.SetOperationToXor()
mask_bits_3.SetMasks(255, 255, 0)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(mask_bits_3.GetOutputPort())
mapper_3.SetColorWindow(255)
mapper_3.SetColorLevel(127.5)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.0, 0.5, 1.0 / 3.0, 1.0)

# Or
mask_bits_4 = vtkImageMaskBits()
mask_bits_4.SetInputConnection(shrink.GetOutputPort())
mask_bits_4.SetOperationToOr()
mask_bits_4.SetMasks(255, 255, 0)

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(mask_bits_4.GetOutputPort())
mapper_4.SetColorWindow(255)
mapper_4.SetColorLevel(127.5)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(1.0 / 3.0, 0.5, 2.0 / 3.0, 1.0)

# Nor
mask_bits_5 = vtkImageMaskBits()
mask_bits_5.SetInputConnection(shrink.GetOutputPort())
mask_bits_5.SetOperationToNor()
mask_bits_5.SetMasks(255, 255, 0)

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(mask_bits_5.GetOutputPort())
mapper_5.SetColorWindow(255)
mapper_5.SetColorLevel(127.5)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(2.0 / 3.0, 0.5, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(384, 256)
render_window.SetWindowName("all mask bits")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
