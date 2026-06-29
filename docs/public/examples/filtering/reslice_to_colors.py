#!/usr/bin/env python

# Test vtkImageResliceToColors with various axes permutations and lookup tables.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import (
    vtkImageMapToColors,
    vtkImageResliceToColors,
    vtkImageShiftScale,
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

# Regular lookup table
table = vtkLookupTable()
table.SetRange(0, 2000)
table.SetRampToLinear()
table.SetAlphaRange(1.0, 1.0)
table.SetValueRange(0.0, 1.0)
table.SetSaturationRange(1.0, 0.0)
table.SetHueRange(0.0, 0.1)
table.Build()

# Map RGB floats
table2 = vtkLookupTable()
table2.SetRange(0.0, 1.0)
table2.SetVectorModeToRGBColors()

# Map RGB unsigned chars
table3 = vtkLookupTable()
table3.SetRange(0, 255)
table3.SetVectorModeToRGBColors()

# Map to RGB colors
colors = vtkImageMapToColors()
colors.SetInputConnection(reader.GetOutputPort())
colors.SetLookupTable(table)
colors.SetOutputFormatToRGB()

# Convert to float
floats = vtkImageShiftScale()
floats.SetInputConnection(colors.GetOutputPort())
floats.SetShift(0.0)
floats.SetScale(0.0039215686274509803)
floats.SetOutputScalarTypeToFloat()

# Rotation transform
transform = vtkTransform()
transform.Translate(+100.8, +100.8, +69.0)
transform.RotateWXYZ(10, 1, 1, 0)
transform.Translate(-100.8, -100.8, -69.0)

# Reslice 1: RGB input with rotation
reslice1 = vtkImageResliceToColors()
reslice1.SetInputConnection(colors.GetOutputPort())
reslice1.SetResliceAxesDirectionCosines([1, 0, 0, 0, 1, 0, 0, 0, 1])
reslice1.SetLookupTable(table3)
reslice1.SetResliceTransform(transform)
reslice1.SetOutputSpacing(3.2, 3.2, 3.2)
reslice1.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice1.SetBackgroundColor(0, 0, 127, 255)
reslice1.Update()

# Reslice 2: RGB input, permuted axes, luminance output
reslice2 = vtkImageResliceToColors()
reslice2.SetInputConnection(colors.GetOutputPort())
reslice2.SetResliceAxesDirectionCosines([0, 1, 0, 0, 0, 1, 1, 0, 0])
reslice2.SetOutputSpacing(3.2, 3.2, 3.2)
reslice2.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice2.SetOutputFormatToLuminance()
reslice2.SetBackgroundColor(0, 0, 127, 255)

# Reslice 3: float input with rotation, RGB output
reslice3 = vtkImageResliceToColors()
reslice3.SetInputConnection(floats.GetOutputPort())
reslice3.SetLookupTable(table2)
reslice3.SetResliceAxesDirectionCosines([0, 0, 1, 1, 0, 0, 0, 1, 0])
reslice3.SetResliceTransform(transform)
reslice3.SetOutputSpacing(3.2, 3.2, 3.2)
reslice3.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice3.SetOutputFormatToRGB()
reslice3.SetBackgroundColor(0, 0, 127, 255)

# Reslice 4: float input, negated axes
reslice4 = vtkImageResliceToColors()
reslice4.SetInputConnection(floats.GetOutputPort())
reslice4.SetLookupTable(table2)
reslice4.SetResliceAxesDirectionCosines([-1, 0, 0, 0, -1, 0, 0, 0, -1])
reslice4.SetOutputSpacing(3.2, 3.2, 3.2)
reslice4.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice4.SetBackgroundColor(0, 0, 127, 255)

# Reslice 5: scalar input with rotation
reslice5 = vtkImageResliceToColors()
reslice5.SetInputConnection(reader.GetOutputPort())
reslice5.SetLookupTable(table)
reslice5.SetResliceAxesDirectionCosines([0, -1, 0, 0, 0, -1, -1, 0, 0])
reslice5.SetResliceTransform(transform)
reslice5.SetOutputSpacing(3.2, 3.2, 3.2)
reslice5.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice5.SetBackgroundColor(0, 0, 127, 255)

# Reslice 6: scalar input, luminance output
reslice6 = vtkImageResliceToColors()
reslice6.SetInputConnection(reader.GetOutputPort())
reslice6.SetLookupTable(table)
reslice6.SetResliceAxesDirectionCosines([0, 0, -1, -1, 0, 0, 0, -1, 0])
reslice6.SetOutputSpacing(3.2, 3.2, 3.2)
reslice6.SetOutputExtent(0, 74, 0, 74, 0, 0)
reslice6.SetOutputFormatToLuminance()
reslice6.SetBackgroundColor(0, 0, 127, 255)

# Mapper + Actor pairs
mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(reslice1.GetOutputPort())
mapper_0.SetColorWindow(255.0)
mapper_0.SetColorLevel(127.5)
mapper_0.SetZSlice(0)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(reslice2.GetOutputPort())
mapper_1.SetColorWindow(255.0)
mapper_1.SetColorLevel(127.5)
mapper_1.SetZSlice(0)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(reslice3.GetOutputPort())
mapper_2.SetColorWindow(255.0)
mapper_2.SetColorLevel(127.5)
mapper_2.SetZSlice(0)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(reslice4.GetOutputPort())
mapper_3.SetColorWindow(255.0)
mapper_3.SetColorLevel(127.5)
mapper_3.SetZSlice(0)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(reslice5.GetOutputPort())
mapper_4.SetColorWindow(255.0)
mapper_4.SetColorLevel(127.5)
mapper_4.SetZSlice(0)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(reslice6.GetOutputPort())
mapper_5.SetColorWindow(255.0)
mapper_5.SetColorLevel(127.5)
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
render_window.SetWindowName("reslice to colors")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
