#!/usr/bin/env python

# Test vtkImageThreshold with various output types, replace modes, and threshold functions.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkIOImage import vtkImageReader
from vtkmodules.vtkImagingCore import vtkImageThreshold
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

# --- Pipeline 0: ReplaceInOn, ReplaceOutOn, ThresholdByLower(800), SignedChar ---
threshold_0 = vtkImageThreshold()
threshold_0.SetInValue(2000)
threshold_0.SetOutValue(0)
threshold_0.ReplaceInOn()
threshold_0.ReplaceOutOn()
threshold_0.SetInputConnection(reader.GetOutputPort())
threshold_0.ThresholdByLower(800)
threshold_0.SetOutputScalarTypeToSignedChar()

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(threshold_0.GetOutputPort())
mapper_0.SetColorWindow(255)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

# --- Pipeline 1: ReplaceInOn, ReplaceOutOn, ThresholdByUpper(1200), UnsignedChar ---
threshold_1 = vtkImageThreshold()
threshold_1.SetInValue(2000)
threshold_1.SetOutValue(0)
threshold_1.ReplaceInOn()
threshold_1.ReplaceOutOn()
threshold_1.SetInputConnection(reader.GetOutputPort())
threshold_1.ThresholdByUpper(1200)
threshold_1.SetOutputScalarTypeToUnsignedChar()

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(threshold_1.GetOutputPort())
mapper_1.SetColorWindow(255)
mapper_1.SetColorLevel(127.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

# --- Pipeline 2: ReplaceInOn, ReplaceOutOn, ThresholdBetween(800, 1200), Long ---
threshold_2 = vtkImageThreshold()
threshold_2.SetInValue(2000)
threshold_2.SetOutValue(0)
threshold_2.ReplaceInOn()
threshold_2.ReplaceOutOn()
threshold_2.SetInputConnection(reader.GetOutputPort())
threshold_2.ThresholdBetween(800, 1200)
threshold_2.SetOutputScalarTypeToLong()

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(threshold_2.GetOutputPort())
mapper_2.SetColorWindow(255)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

# --- Pipeline 3: ReplaceInOn, ReplaceOutOff, ThresholdByLower(800), UnsignedLong ---
threshold_3 = vtkImageThreshold()
threshold_3.SetInValue(2000)
threshold_3.SetOutValue(0)
threshold_3.ReplaceInOn()
threshold_3.ReplaceOutOff()
threshold_3.SetInputConnection(reader.GetOutputPort())
threshold_3.ThresholdByLower(800)
threshold_3.SetOutputScalarTypeToUnsignedLong()

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(threshold_3.GetOutputPort())
mapper_3.SetColorWindow(2000)
mapper_3.SetColorLevel(1000)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

# --- Pipeline 4: ReplaceInOn, ReplaceOutOff, ThresholdByUpper(1200), Int ---
threshold_4 = vtkImageThreshold()
threshold_4.SetInValue(2000)
threshold_4.SetOutValue(0)
threshold_4.ReplaceInOn()
threshold_4.ReplaceOutOff()
threshold_4.SetInputConnection(reader.GetOutputPort())
threshold_4.ThresholdByUpper(1200)
threshold_4.SetOutputScalarTypeToInt()

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(threshold_4.GetOutputPort())
mapper_4.SetColorWindow(2000)
mapper_4.SetColorLevel(1000)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

# --- Pipeline 5: ReplaceInOn, ReplaceOutOff, ThresholdBetween(800, 1200), UnsignedInt ---
threshold_5 = vtkImageThreshold()
threshold_5.SetInValue(2000)
threshold_5.SetOutValue(0)
threshold_5.ReplaceInOn()
threshold_5.ReplaceOutOff()
threshold_5.SetInputConnection(reader.GetOutputPort())
threshold_5.ThresholdBetween(800, 1200)
threshold_5.SetOutputScalarTypeToUnsignedInt()

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(threshold_5.GetOutputPort())
mapper_5.SetColorWindow(2000)
mapper_5.SetColorLevel(1000)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

# --- Pipeline 6: ReplaceInOff, ReplaceOutOn, ThresholdByLower(800), Short ---
threshold_6 = vtkImageThreshold()
threshold_6.SetInValue(2000)
threshold_6.SetOutValue(0)
threshold_6.ReplaceInOff()
threshold_6.ReplaceOutOn()
threshold_6.SetInputConnection(reader.GetOutputPort())
threshold_6.ThresholdByLower(800)
threshold_6.SetOutputScalarTypeToShort()

mapper_6 = vtkImageMapper()
mapper_6.SetInputConnection(threshold_6.GetOutputPort())
mapper_6.SetColorWindow(2000)
mapper_6.SetColorLevel(1000)

actor_6 = vtkActor2D()
actor_6.SetMapper(mapper_6)

# --- Pipeline 7: ReplaceInOff, ReplaceOutOn, ThresholdByUpper(1200), UnsignedShort ---
threshold_7 = vtkImageThreshold()
threshold_7.SetInValue(2000)
threshold_7.SetOutValue(0)
threshold_7.ReplaceInOff()
threshold_7.ReplaceOutOn()
threshold_7.SetInputConnection(reader.GetOutputPort())
threshold_7.ThresholdByUpper(1200)
threshold_7.SetOutputScalarTypeToUnsignedShort()

mapper_7 = vtkImageMapper()
mapper_7.SetInputConnection(threshold_7.GetOutputPort())
mapper_7.SetColorWindow(2000)
mapper_7.SetColorLevel(1000)

actor_7 = vtkActor2D()
actor_7.SetMapper(mapper_7)

# --- Pipeline 8: ReplaceInOff, ReplaceOutOn, ThresholdBetween(800, 1200), Double ---
threshold_8 = vtkImageThreshold()
threshold_8.SetInValue(2000)
threshold_8.SetOutValue(0)
threshold_8.ReplaceInOff()
threshold_8.ReplaceOutOn()
threshold_8.SetInputConnection(reader.GetOutputPort())
threshold_8.ThresholdBetween(800, 1200)
threshold_8.SetOutputScalarTypeToDouble()

mapper_8 = vtkImageMapper()
mapper_8.SetInputConnection(threshold_8.GetOutputPort())
mapper_8.SetColorWindow(2000)
mapper_8.SetColorLevel(1000)

actor_8 = vtkActor2D()
actor_8.SetMapper(mapper_8)

# --- Pipeline 9: ReplaceInOff, ReplaceOutOff, ThresholdByLower(800), Float ---
threshold_9 = vtkImageThreshold()
threshold_9.SetInValue(2000)
threshold_9.SetOutValue(0)
threshold_9.ReplaceInOff()
threshold_9.ReplaceOutOff()
threshold_9.SetInputConnection(reader.GetOutputPort())
threshold_9.ThresholdByLower(800)
threshold_9.SetOutputScalarTypeToFloat()

mapper_9 = vtkImageMapper()
mapper_9.SetInputConnection(threshold_9.GetOutputPort())
mapper_9.SetColorWindow(2000)
mapper_9.SetColorLevel(1000)

actor_9 = vtkActor2D()
actor_9.SetMapper(mapper_9)

# --- Pipeline 10: ReplaceInOff, ReplaceOutOff, ThresholdByUpper(1200), Double ---
threshold_10 = vtkImageThreshold()
threshold_10.SetInValue(2000)
threshold_10.SetOutValue(0)
threshold_10.ReplaceInOff()
threshold_10.ReplaceOutOff()
threshold_10.SetInputConnection(reader.GetOutputPort())
threshold_10.ThresholdByUpper(1200)
threshold_10.SetOutputScalarTypeToDouble()

mapper_10 = vtkImageMapper()
mapper_10.SetInputConnection(threshold_10.GetOutputPort())
mapper_10.SetColorWindow(2000)
mapper_10.SetColorLevel(1000)

actor_10 = vtkActor2D()
actor_10.SetMapper(mapper_10)

# --- Pipeline 11: ReplaceInOff, ReplaceOutOff, ThresholdBetween(800, 1200), Float ---
threshold_11 = vtkImageThreshold()
threshold_11.SetInValue(2000)
threshold_11.SetOutValue(0)
threshold_11.ReplaceInOff()
threshold_11.ReplaceOutOff()
threshold_11.SetInputConnection(reader.GetOutputPort())
threshold_11.ThresholdBetween(800, 1200)
threshold_11.SetOutputScalarTypeToFloat()

mapper_11 = vtkImageMapper()
mapper_11.SetInputConnection(threshold_11.GetOutputPort())
mapper_11.SetColorWindow(2000)
mapper_11.SetColorLevel(1000)

actor_11 = vtkActor2D()
actor_11.SetMapper(mapper_11)

# Renderers (4x3 grid)
renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0, 0, .33333, .25)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(.33333, 0, .66667, .25)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(.66667, 0, 1, .25)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0, .25, .33333, .5)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(.33333, .25, .66667, .5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(.66667, .25, 1, .5)

renderer_6 = vtkRenderer()
renderer_6.AddViewProp(actor_6)
renderer_6.SetViewport(0, .5, .33333, .75)

renderer_7 = vtkRenderer()
renderer_7.AddViewProp(actor_7)
renderer_7.SetViewport(.33333, .5, .66667, .75)

renderer_8 = vtkRenderer()
renderer_8.AddViewProp(actor_8)
renderer_8.SetViewport(.66667, .5, 1, .75)

renderer_9 = vtkRenderer()
renderer_9.AddViewProp(actor_9)
renderer_9.SetViewport(0, .75, .33333, 1)

renderer_10 = vtkRenderer()
renderer_10.AddViewProp(actor_10)
renderer_10.SetViewport(.33333, .75, .66667, 1)

renderer_11 = vtkRenderer()
renderer_11.AddViewProp(actor_11)
renderer_11.SetViewport(.66667, .75, 1, 1)

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
render_window.AddRenderer(renderer_8)
render_window.AddRenderer(renderer_9)
render_window.AddRenderer(renderer_10)
render_window.AddRenderer(renderer_11)
render_window.SetSize(192, 256)
render_window.SetWindowName("threshold")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
