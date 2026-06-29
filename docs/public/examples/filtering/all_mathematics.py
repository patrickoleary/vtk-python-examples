#!/usr/bin/env python

# Test vtkImageMathematics with various math operators on ellipsoid sources.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkImagingMath import vtkImageMathematics
from vtkmodules.vtkImagingSources import vtkImageEllipsoidSource
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkImageMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source ellipsoids
sphere1 = vtkImageEllipsoidSource()
sphere1.SetCenter(40, 20, 0)
sphere1.SetRadius(30, 30, 0)
sphere1.SetInValue(.75)
sphere1.SetOutValue(.3)
sphere1.SetOutputScalarTypeToFloat()
sphere1.SetWholeExtent(0, 99, 0, 74, 0, 0)
sphere1.Update()

sphere2 = vtkImageEllipsoidSource()
sphere2.SetCenter(60, 30, 0)
sphere2.SetRadius(20, 20, 20)
sphere2.SetInValue(.2)
sphere2.SetOutValue(.5)
sphere2.SetOutputScalarTypeToFloat()
sphere2.SetWholeExtent(0, 99, 0, 74, 0, 0)
sphere2.Update()

# Add (row 1, col 1)
math_filter_0 = vtkImageMathematics()
math_filter_0.SetInput1Data(sphere1.GetOutput())
math_filter_0.SetInput2Data(sphere2.GetOutput())
math_filter_0.SetOperationToAdd()
math_filter_0.SetConstantK(.3)
math_filter_0.SetConstantC(.75)

mapper_0 = vtkImageMapper()
mapper_0.SetInputConnection(math_filter_0.GetOutputPort())
mapper_0.SetColorWindow(2.0)
mapper_0.SetColorLevel(.75)

actor_0 = vtkActor2D()
actor_0.SetMapper(mapper_0)

renderer_0 = vtkRenderer()
renderer_0.AddViewProp(actor_0)
renderer_0.SetViewport(0.0, 0.0, 1.0 / 6.0, 0.25)

# Subtract (row 1, col 2)
math_filter_1 = vtkImageMathematics()
math_filter_1.SetInput1Data(sphere1.GetOutput())
math_filter_1.SetInput2Data(sphere2.GetOutput())
math_filter_1.SetOperationToSubtract()
math_filter_1.SetConstantK(.3)
math_filter_1.SetConstantC(.75)

mapper_1 = vtkImageMapper()
mapper_1.SetInputConnection(math_filter_1.GetOutputPort())
mapper_1.SetColorWindow(2.0)
mapper_1.SetColorLevel(.75)

actor_1 = vtkActor2D()
actor_1.SetMapper(mapper_1)

renderer_1 = vtkRenderer()
renderer_1.AddViewProp(actor_1)
renderer_1.SetViewport(1.0 / 6.0, 0.0, 2.0 / 6.0, 0.25)

# Multiply (row 1, col 3)
math_filter_2 = vtkImageMathematics()
math_filter_2.SetInput1Data(sphere1.GetOutput())
math_filter_2.SetInput2Data(sphere2.GetOutput())
math_filter_2.SetOperationToMultiply()
math_filter_2.SetConstantK(.3)
math_filter_2.SetConstantC(.75)

mapper_2 = vtkImageMapper()
mapper_2.SetInputConnection(math_filter_2.GetOutputPort())
mapper_2.SetColorWindow(2.0)
mapper_2.SetColorLevel(.75)

actor_2 = vtkActor2D()
actor_2.SetMapper(mapper_2)

renderer_2 = vtkRenderer()
renderer_2.AddViewProp(actor_2)
renderer_2.SetViewport(2.0 / 6.0, 0.0, 3.0 / 6.0, 0.25)

# Divide (row 1, col 4)
math_filter_3 = vtkImageMathematics()
math_filter_3.SetInput1Data(sphere1.GetOutput())
math_filter_3.SetInput2Data(sphere2.GetOutput())
math_filter_3.SetOperationToDivide()
math_filter_3.SetConstantK(.3)
math_filter_3.SetConstantC(.75)

mapper_3 = vtkImageMapper()
mapper_3.SetInputConnection(math_filter_3.GetOutputPort())
mapper_3.SetColorWindow(2.0)
mapper_3.SetColorLevel(.75)

actor_3 = vtkActor2D()
actor_3.SetMapper(mapper_3)

renderer_3 = vtkRenderer()
renderer_3.AddViewProp(actor_3)
renderer_3.SetViewport(3.0 / 6.0, 0.0, 4.0 / 6.0, 0.25)

# Invert (row 1, col 5)
math_filter_4 = vtkImageMathematics()
math_filter_4.SetInput1Data(sphere1.GetOutput())
math_filter_4.SetInput2Data(sphere2.GetOutput())
math_filter_4.SetOperationToInvert()
math_filter_4.SetConstantK(.3)
math_filter_4.SetConstantC(.75)

mapper_4 = vtkImageMapper()
mapper_4.SetInputConnection(math_filter_4.GetOutputPort())
mapper_4.SetColorWindow(2.0)
mapper_4.SetColorLevel(.75)

actor_4 = vtkActor2D()
actor_4.SetMapper(mapper_4)

renderer_4 = vtkRenderer()
renderer_4.AddViewProp(actor_4)
renderer_4.SetViewport(4.0 / 6.0, 0.0, 5.0 / 6.0, 0.25)

# Sin (row 1, col 6)
math_filter_5 = vtkImageMathematics()
math_filter_5.SetInput1Data(sphere1.GetOutput())
math_filter_5.SetInput2Data(sphere2.GetOutput())
math_filter_5.SetOperationToSin()
math_filter_5.SetConstantK(.3)
math_filter_5.SetConstantC(.75)

mapper_5 = vtkImageMapper()
mapper_5.SetInputConnection(math_filter_5.GetOutputPort())
mapper_5.SetColorWindow(2.0)
mapper_5.SetColorLevel(.75)

actor_5 = vtkActor2D()
actor_5.SetMapper(mapper_5)

renderer_5 = vtkRenderer()
renderer_5.AddViewProp(actor_5)
renderer_5.SetViewport(5.0 / 6.0, 0.0, 1.0, 0.25)

# Cos (row 2, col 1)
math_filter_6 = vtkImageMathematics()
math_filter_6.SetInput1Data(sphere1.GetOutput())
math_filter_6.SetInput2Data(sphere2.GetOutput())
math_filter_6.SetOperationToCos()
math_filter_6.SetConstantK(.3)
math_filter_6.SetConstantC(.75)

mapper_6 = vtkImageMapper()
mapper_6.SetInputConnection(math_filter_6.GetOutputPort())
mapper_6.SetColorWindow(2.0)
mapper_6.SetColorLevel(.75)

actor_6 = vtkActor2D()
actor_6.SetMapper(mapper_6)

renderer_6 = vtkRenderer()
renderer_6.AddViewProp(actor_6)
renderer_6.SetViewport(0.0, 0.25, 1.0 / 6.0, 0.5)

# Exp (row 2, col 2)
math_filter_7 = vtkImageMathematics()
math_filter_7.SetInput1Data(sphere1.GetOutput())
math_filter_7.SetInput2Data(sphere2.GetOutput())
math_filter_7.SetOperationToExp()
math_filter_7.SetConstantK(.3)
math_filter_7.SetConstantC(.75)

mapper_7 = vtkImageMapper()
mapper_7.SetInputConnection(math_filter_7.GetOutputPort())
mapper_7.SetColorWindow(2.0)
mapper_7.SetColorLevel(.75)

actor_7 = vtkActor2D()
actor_7.SetMapper(mapper_7)

renderer_7 = vtkRenderer()
renderer_7.AddViewProp(actor_7)
renderer_7.SetViewport(1.0 / 6.0, 0.25, 2.0 / 6.0, 0.5)

# Log (row 2, col 3)
math_filter_8 = vtkImageMathematics()
math_filter_8.SetInput1Data(sphere1.GetOutput())
math_filter_8.SetInput2Data(sphere2.GetOutput())
math_filter_8.SetOperationToLog()
math_filter_8.SetConstantK(.3)
math_filter_8.SetConstantC(.75)

mapper_8 = vtkImageMapper()
mapper_8.SetInputConnection(math_filter_8.GetOutputPort())
mapper_8.SetColorWindow(2.0)
mapper_8.SetColorLevel(.75)

actor_8 = vtkActor2D()
actor_8.SetMapper(mapper_8)

renderer_8 = vtkRenderer()
renderer_8.AddViewProp(actor_8)
renderer_8.SetViewport(2.0 / 6.0, 0.25, 3.0 / 6.0, 0.5)

# AbsoluteValue (row 2, col 4)
math_filter_9 = vtkImageMathematics()
math_filter_9.SetInput1Data(sphere1.GetOutput())
math_filter_9.SetInput2Data(sphere2.GetOutput())
math_filter_9.SetOperationToAbsoluteValue()
math_filter_9.SetConstantK(.3)
math_filter_9.SetConstantC(.75)

mapper_9 = vtkImageMapper()
mapper_9.SetInputConnection(math_filter_9.GetOutputPort())
mapper_9.SetColorWindow(2.0)
mapper_9.SetColorLevel(.75)

actor_9 = vtkActor2D()
actor_9.SetMapper(mapper_9)

renderer_9 = vtkRenderer()
renderer_9.AddViewProp(actor_9)
renderer_9.SetViewport(3.0 / 6.0, 0.25, 4.0 / 6.0, 0.5)

# Square (row 2, col 5)
math_filter_10 = vtkImageMathematics()
math_filter_10.SetInput1Data(sphere1.GetOutput())
math_filter_10.SetInput2Data(sphere2.GetOutput())
math_filter_10.SetOperationToSquare()
math_filter_10.SetConstantK(.3)
math_filter_10.SetConstantC(.75)

mapper_10 = vtkImageMapper()
mapper_10.SetInputConnection(math_filter_10.GetOutputPort())
mapper_10.SetColorWindow(2.0)
mapper_10.SetColorLevel(.75)

actor_10 = vtkActor2D()
actor_10.SetMapper(mapper_10)

renderer_10 = vtkRenderer()
renderer_10.AddViewProp(actor_10)
renderer_10.SetViewport(4.0 / 6.0, 0.25, 5.0 / 6.0, 0.5)

# SquareRoot (row 2, col 6)
math_filter_11 = vtkImageMathematics()
math_filter_11.SetInput1Data(sphere1.GetOutput())
math_filter_11.SetInput2Data(sphere2.GetOutput())
math_filter_11.SetOperationToSquareRoot()
math_filter_11.SetConstantK(.3)
math_filter_11.SetConstantC(.75)

mapper_11 = vtkImageMapper()
mapper_11.SetInputConnection(math_filter_11.GetOutputPort())
mapper_11.SetColorWindow(2.0)
mapper_11.SetColorLevel(.75)

actor_11 = vtkActor2D()
actor_11.SetMapper(mapper_11)

renderer_11 = vtkRenderer()
renderer_11.AddViewProp(actor_11)
renderer_11.SetViewport(5.0 / 6.0, 0.25, 1.0, 0.5)

# Min (row 3, col 1)
math_filter_12 = vtkImageMathematics()
math_filter_12.SetInput1Data(sphere1.GetOutput())
math_filter_12.SetInput2Data(sphere2.GetOutput())
math_filter_12.SetOperationToMin()
math_filter_12.SetConstantK(.3)
math_filter_12.SetConstantC(.75)

mapper_12 = vtkImageMapper()
mapper_12.SetInputConnection(math_filter_12.GetOutputPort())
mapper_12.SetColorWindow(2.0)
mapper_12.SetColorLevel(.75)

actor_12 = vtkActor2D()
actor_12.SetMapper(mapper_12)

renderer_12 = vtkRenderer()
renderer_12.AddViewProp(actor_12)
renderer_12.SetViewport(0.0, 0.5, 1.0 / 6.0, 0.75)

# Max (row 3, col 2)
math_filter_13 = vtkImageMathematics()
math_filter_13.SetInput1Data(sphere1.GetOutput())
math_filter_13.SetInput2Data(sphere2.GetOutput())
math_filter_13.SetOperationToMax()
math_filter_13.SetConstantK(.3)
math_filter_13.SetConstantC(.75)

mapper_13 = vtkImageMapper()
mapper_13.SetInputConnection(math_filter_13.GetOutputPort())
mapper_13.SetColorWindow(2.0)
mapper_13.SetColorLevel(.75)

actor_13 = vtkActor2D()
actor_13.SetMapper(mapper_13)

renderer_13 = vtkRenderer()
renderer_13.AddViewProp(actor_13)
renderer_13.SetViewport(1.0 / 6.0, 0.5, 2.0 / 6.0, 0.75)

# ATAN (row 3, col 3)
math_filter_14 = vtkImageMathematics()
math_filter_14.SetInput1Data(sphere1.GetOutput())
math_filter_14.SetInput2Data(sphere2.GetOutput())
math_filter_14.SetOperationToATAN()
math_filter_14.SetConstantK(.3)
math_filter_14.SetConstantC(.75)

mapper_14 = vtkImageMapper()
mapper_14.SetInputConnection(math_filter_14.GetOutputPort())
mapper_14.SetColorWindow(2.0)
mapper_14.SetColorLevel(.75)

actor_14 = vtkActor2D()
actor_14.SetMapper(mapper_14)

renderer_14 = vtkRenderer()
renderer_14.AddViewProp(actor_14)
renderer_14.SetViewport(2.0 / 6.0, 0.5, 3.0 / 6.0, 0.75)

# ATAN2 (row 3, col 4)
math_filter_15 = vtkImageMathematics()
math_filter_15.SetInput1Data(sphere1.GetOutput())
math_filter_15.SetInput2Data(sphere2.GetOutput())
math_filter_15.SetOperationToATAN2()
math_filter_15.SetConstantK(.3)
math_filter_15.SetConstantC(.75)

mapper_15 = vtkImageMapper()
mapper_15.SetInputConnection(math_filter_15.GetOutputPort())
mapper_15.SetColorWindow(2.0)
mapper_15.SetColorLevel(.75)

actor_15 = vtkActor2D()
actor_15.SetMapper(mapper_15)

renderer_15 = vtkRenderer()
renderer_15.AddViewProp(actor_15)
renderer_15.SetViewport(3.0 / 6.0, 0.5, 4.0 / 6.0, 0.75)

# MultiplyByK (row 3, col 5)
math_filter_16 = vtkImageMathematics()
math_filter_16.SetInput1Data(sphere1.GetOutput())
math_filter_16.SetInput2Data(sphere2.GetOutput())
math_filter_16.SetOperationToMultiplyByK()
math_filter_16.SetConstantK(.3)
math_filter_16.SetConstantC(.75)

mapper_16 = vtkImageMapper()
mapper_16.SetInputConnection(math_filter_16.GetOutputPort())
mapper_16.SetColorWindow(2.0)
mapper_16.SetColorLevel(.75)

actor_16 = vtkActor2D()
actor_16.SetMapper(mapper_16)

renderer_16 = vtkRenderer()
renderer_16.AddViewProp(actor_16)
renderer_16.SetViewport(4.0 / 6.0, 0.5, 5.0 / 6.0, 0.75)

# ReplaceCByK (row 3, col 6)
math_filter_17 = vtkImageMathematics()
math_filter_17.SetInput1Data(sphere1.GetOutput())
math_filter_17.SetInput2Data(sphere2.GetOutput())
math_filter_17.SetOperationToReplaceCByK()
math_filter_17.SetConstantK(.3)
math_filter_17.SetConstantC(.75)

mapper_17 = vtkImageMapper()
mapper_17.SetInputConnection(math_filter_17.GetOutputPort())
mapper_17.SetColorWindow(2.0)
mapper_17.SetColorLevel(.75)

actor_17 = vtkActor2D()
actor_17.SetMapper(mapper_17)

renderer_17 = vtkRenderer()
renderer_17.AddViewProp(actor_17)
renderer_17.SetViewport(5.0 / 6.0, 0.5, 1.0, 0.75)

# AddConstant (row 4, col 1 — extended to fill row)
math_filter_18 = vtkImageMathematics()
math_filter_18.SetInput1Data(sphere1.GetOutput())
math_filter_18.SetInput2Data(sphere2.GetOutput())
math_filter_18.SetOperationToAddConstant()
math_filter_18.SetConstantK(.3)
math_filter_18.SetConstantC(.75)

mapper_18 = vtkImageMapper()
mapper_18.SetInputConnection(math_filter_18.GetOutputPort())
mapper_18.SetColorWindow(2.0)
mapper_18.SetColorLevel(.75)

actor_18 = vtkActor2D()
actor_18.SetMapper(mapper_18)

renderer_18 = vtkRenderer()
renderer_18.AddViewProp(actor_18)
renderer_18.SetViewport(0.0, 0.75, 1.0, 1.0)

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
render_window.AddRenderer(renderer_12)
render_window.AddRenderer(renderer_13)
render_window.AddRenderer(renderer_14)
render_window.AddRenderer(renderer_15)
render_window.AddRenderer(renderer_16)
render_window.AddRenderer(renderer_17)
render_window.AddRenderer(renderer_18)
render_window.SetSize(600, 300)
render_window.SetWindowName("all mathematics")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
