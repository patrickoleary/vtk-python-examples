#!/usr/bin/env python

# Test vtkImageLogic with various operators and scalar types on ellipsoid sources.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingMath import vtkImageLogic
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# And (Float)
sphere1_0 = vtkImageEllipsoidSource()
sphere1_0.SetCenter(95, 100, 0)
sphere1_0.SetRadius(70, 70, 70)
sphere1_0.SetOutputScalarTypeToFloat()
sphere1_0.Update()

sphere2_0 = vtkImageEllipsoidSource()
sphere2_0.SetCenter(161, 100, 0)
sphere2_0.SetRadius(70, 70, 70)
sphere2_0.SetOutputScalarTypeToFloat()
sphere2_0.Update()

logic_0 = vtkImageLogic()
logic_0.SetInput1Data(sphere1_0.GetOutput())
logic_0.SetInput2Data(sphere2_0.GetOutput())
logic_0.SetOutputTrueValue(150)
logic_0.SetOperationToAnd()

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(logic_0.GetOutputPort())
mapper_0.SetColorWindow(255)
mapper_0.SetColorLevel(127.5)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0, .5, .33, 1)

# Or (Double)
sphere1_1 = vtkImageEllipsoidSource()
sphere1_1.SetCenter(95, 100, 0)
sphere1_1.SetRadius(70, 70, 70)
sphere1_1.SetOutputScalarTypeToDouble()
sphere1_1.Update()

sphere2_1 = vtkImageEllipsoidSource()
sphere2_1.SetCenter(161, 100, 0)
sphere2_1.SetRadius(70, 70, 70)
sphere2_1.SetOutputScalarTypeToDouble()
sphere2_1.Update()

logic_1 = vtkImageLogic()
logic_1.SetInput1Data(sphere1_1.GetOutput())
logic_1.SetInput2Data(sphere2_1.GetOutput())
logic_1.SetOutputTrueValue(150)
logic_1.SetOperationToOr()

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(logic_1.GetOutputPort())
mapper_1.SetColorWindow(255)
mapper_1.SetColorLevel(127.5)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(.33, .5, .66, 1)

# Xor (UnsignedInt)
sphere1_2 = vtkImageEllipsoidSource()
sphere1_2.SetCenter(95, 100, 0)
sphere1_2.SetRadius(70, 70, 70)
sphere1_2.SetOutputScalarTypeToUnsignedInt()
sphere1_2.Update()

sphere2_2 = vtkImageEllipsoidSource()
sphere2_2.SetCenter(161, 100, 0)
sphere2_2.SetRadius(70, 70, 70)
sphere2_2.SetOutputScalarTypeToUnsignedInt()
sphere2_2.Update()

logic_2 = vtkImageLogic()
logic_2.SetInput1Data(sphere1_2.GetOutput())
logic_2.SetInput2Data(sphere2_2.GetOutput())
logic_2.SetOutputTrueValue(150)
logic_2.SetOperationToXor()

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(logic_2.GetOutputPort())
mapper_2.SetColorWindow(255)
mapper_2.SetColorLevel(127.5)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(.66, .5, 1, 1)

# Nand (UnsignedLong)
sphere1_3 = vtkImageEllipsoidSource()
sphere1_3.SetCenter(95, 100, 0)
sphere1_3.SetRadius(70, 70, 70)
sphere1_3.SetOutputScalarTypeToUnsignedLong()
sphere1_3.Update()

sphere2_3 = vtkImageEllipsoidSource()
sphere2_3.SetCenter(161, 100, 0)
sphere2_3.SetRadius(70, 70, 70)
sphere2_3.SetOutputScalarTypeToUnsignedLong()
sphere2_3.Update()

logic_3 = vtkImageLogic()
logic_3.SetInput1Data(sphere1_3.GetOutput())
logic_3.SetInput2Data(sphere2_3.GetOutput())
logic_3.SetOutputTrueValue(150)
logic_3.SetOperationToNand()

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(logic_3.GetOutputPort())
mapper_3.SetColorWindow(255)
mapper_3.SetColorLevel(127.5)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(0, 0, .33, .5)

# Nor (UnsignedShort)
sphere1_4 = vtkImageEllipsoidSource()
sphere1_4.SetCenter(95, 100, 0)
sphere1_4.SetRadius(70, 70, 70)
sphere1_4.SetOutputScalarTypeToUnsignedShort()
sphere1_4.Update()

sphere2_4 = vtkImageEllipsoidSource()
sphere2_4.SetCenter(161, 100, 0)
sphere2_4.SetRadius(70, 70, 70)
sphere2_4.SetOutputScalarTypeToUnsignedShort()
sphere2_4.Update()

logic_4 = vtkImageLogic()
logic_4.SetInput1Data(sphere1_4.GetOutput())
logic_4.SetInput2Data(sphere2_4.GetOutput())
logic_4.SetOutputTrueValue(150)
logic_4.SetOperationToNor()

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(logic_4.GetOutputPort())
mapper_4.SetColorWindow(255)
mapper_4.SetColorLevel(127.5)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(.33, 0, .66, .5)

# Not (UnsignedChar) — only sphere1, no sphere2
sphere1_5 = vtkImageEllipsoidSource()
sphere1_5.SetCenter(95, 100, 0)
sphere1_5.SetRadius(70, 70, 70)
sphere1_5.SetOutputScalarTypeToUnsignedChar()
sphere1_5.Update()

logic_5 = vtkImageLogic()
logic_5.SetInput1Data(sphere1_5.GetOutput())
logic_5.SetOutputTrueValue(150)
logic_5.SetOperationToNot()

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(logic_5.GetOutputPort())
mapper_5.SetColorWindow(255)
mapper_5.SetColorLevel(127.5)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(.66, 0, 1, .5)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.SetSize(768, 512)
render_window.SetWindowName("all logic")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
