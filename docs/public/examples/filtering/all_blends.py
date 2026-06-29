#!/usr/bin/env python

# Test vtkImageBlend with various foreground/background luminance and color combinations.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkIOImage import (
    vtkBMPReader,
    vtkTIFFReader,
)
from vtkmodules.vtkImagingColor import vtkImageLuminance
from vtkmodules.vtkImagingCore import (
    vtkImageAppendComponents,
    vtkImageBlend,
    vtkImageMapToColors,
    vtkImageShrink3D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Read images
image1 = vtkTIFFReader()
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

image1.SetFileName(os.path.join(data_dir, "beach.tif"))
image1.SetOrientationType(4)

image2 = vtkBMPReader()
image2.SetFileName(os.path.join(data_dir, "masonry.bmp"))

# Shrink images
color = vtkImageShrink3D()
color.SetInputConnection(image1.GetOutputPort())
color.SetShrinkFactors(2, 2, 1)

background_color = vtkImageShrink3D()
background_color.SetInputConnection(image2.GetOutputPort())
background_color.SetShrinkFactors(2, 2, 1)

# Greyscale versions
luminance = vtkImageLuminance()
luminance.SetInputConnection(color.GetOutputPort())

background_luminance = vtkImageLuminance()
background_luminance.SetInputConnection(background_color.GetOutputPort())

# Alpha mask from luminance
table = vtkLookupTable()
table.SetTableRange(220, 255)
table.SetValueRange(1, 0)
table.SetSaturationRange(0, 0)
table.Build()

alpha = vtkImageMapToColors()
alpha.SetInputConnection(luminance.GetOutputPort())
alpha.SetLookupTable(table)
alpha.SetOutputFormatToLuminance()

# Luminance+alpha and color+alpha
luminance_alpha = vtkImageAppendComponents()
luminance_alpha.AddInputConnection(luminance.GetOutputPort())
luminance_alpha.AddInputConnection(alpha.GetOutputPort())

color_alpha = vtkImageAppendComponents()
color_alpha.AddInputConnection(color.GetOutputPort())
color_alpha.AddInputConnection(alpha.GetOutputPort())

# Row 0 (background_color), Col 0 (luminance)
blend_0 = vtkImageBlend()
blend_0.AddInputConnection(background_color.GetOutputPort())
blend_0.AddInputConnection(luminance.GetOutputPort())
blend_0.SetOpacity(1, 0.8)

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(blend_0.GetOutputPort())
mapper_0.SetColorWindow(255)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.0, 0.25, 0.5)

# Row 0 (background_color), Col 1 (luminance_alpha)
blend_1 = vtkImageBlend()
blend_1.AddInputConnection(background_color.GetOutputPort())
blend_1.AddInputConnection(luminance_alpha.GetOutputPort())
blend_1.SetOpacity(1, 0.8)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(blend_1.GetOutputPort())
mapper_1.SetColorWindow(255)
mapper_1.SetColorLevel(127.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(0.25, 0.0, 0.5, 0.5)

# Row 0 (background_color), Col 2 (color)
blend_2 = vtkImageBlend()
blend_2.AddInputConnection(background_color.GetOutputPort())
blend_2.AddInputConnection(color.GetOutputPort())
blend_2.SetOpacity(1, 0.8)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(blend_2.GetOutputPort())
mapper_2.SetColorWindow(255)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(0.5, 0.0, 0.75, 0.5)

# Row 0 (background_color), Col 3 (color_alpha)
blend_3 = vtkImageBlend()
blend_3.AddInputConnection(background_color.GetOutputPort())
blend_3.AddInputConnection(color_alpha.GetOutputPort())
blend_3.SetOpacity(1, 0.8)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(blend_3.GetOutputPort())
mapper_3.SetColorWindow(255)
mapper_3.SetColorLevel(127.5)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0.75, 0.0, 1.0, 0.5)

# Row 1 (background_luminance), Col 0 (luminance)
blend_4 = vtkImageBlend()
blend_4.AddInputConnection(background_luminance.GetOutputPort())
blend_4.AddInputConnection(luminance.GetOutputPort())
blend_4.SetOpacity(1, 0.8)

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(blend_4.GetOutputPort())
mapper_4.SetColorWindow(255)
mapper_4.SetColorLevel(127.5)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(0.0, 0.5, 0.25, 1.0)

# Row 1 (background_luminance), Col 1 (luminance_alpha)
blend_5 = vtkImageBlend()
blend_5.AddInputConnection(background_luminance.GetOutputPort())
blend_5.AddInputConnection(luminance_alpha.GetOutputPort())
blend_5.SetOpacity(1, 0.8)

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(blend_5.GetOutputPort())
mapper_5.SetColorWindow(255)
mapper_5.SetColorLevel(127.5)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(0.25, 0.5, 0.5, 1.0)

# Row 1 (background_luminance), Col 2 (color) — no foreground blended
blend_6 = vtkImageBlend()
blend_6.AddInputConnection(background_luminance.GetOutputPort())

mapper_6 = vtkImageMapper()
mapper_6.SetInputConnection(blend_6.GetOutputPort())
mapper_6.SetColorWindow(255)
mapper_6.SetColorLevel(127.5)

actor_6 = vtkActor2D()
actor_6.SetMapper(mapper_6)

renderer_6 = vtkRenderer()
renderer_6.AddViewProp(actor_6)
renderer_6.SetViewport(0.5, 0.5, 0.75, 1.0)

# Row 1 (background_luminance), Col 3 (color_alpha) — no foreground blended
blend_7 = vtkImageBlend()
blend_7.AddInputConnection(background_luminance.GetOutputPort())

mapper_7 = vtkImageMapper()
mapper_7.SetInputConnection(blend_7.GetOutputPort())
mapper_7.SetColorWindow(255)
mapper_7.SetColorLevel(127.5)

actor_7 = vtkActor2D()
actor_7.SetMapper(mapper_7)

renderer_7 = vtkRenderer()
renderer_7.AddViewProp(actor_7)
renderer_7.SetViewport(0.75, 0.5, 1.0, 1.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetSize(512, 256)
render_window.SetWindowName("all blends")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
