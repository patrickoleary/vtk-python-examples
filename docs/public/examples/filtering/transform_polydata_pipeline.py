#!/usr/bin/env python

# Test identity, linear, perspective, and concatenated transforms on polydata.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import (
    vtkIdentityTransform,
    vtkPerspectiveTransform,
    vtkTransform,
)
from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create six plane sources forming a cube
plane_1 = vtkPlaneSource()
plane_1.SetOrigin(0.5, 0.508, -0.5)
plane_1.SetPoint1(-0.5, 0.508, -0.5)
plane_1.SetPoint2(0.5, 0.508, 0.5)
plane_1.SetXResolution(5)
plane_1.SetYResolution(5)
plane_1.Update()

plane_2 = vtkPlaneSource()
plane_2.SetOrigin(-0.508, 0.5, -0.5)
plane_2.SetPoint1(-0.508, -0.5, -0.5)
plane_2.SetPoint2(-0.508, 0.5, 0.5)
plane_2.SetXResolution(5)
plane_2.SetYResolution(5)
plane_2.Update()

plane_3 = vtkPlaneSource()
plane_3.SetOrigin(-0.5, -0.508, -0.5)
plane_3.SetPoint1(0.5, -0.508, -0.5)
plane_3.SetPoint2(-0.5, -0.508, 0.5)
plane_3.SetXResolution(5)
plane_3.SetYResolution(5)
plane_3.Update()

plane_4 = vtkPlaneSource()
plane_4.SetOrigin(0.508, -0.5, -0.5)
plane_4.SetPoint1(0.508, 0.5, -0.5)
plane_4.SetPoint2(0.508, -0.5, 0.5)
plane_4.SetXResolution(5)
plane_4.SetYResolution(5)
plane_4.Update()

plane_5 = vtkPlaneSource()
plane_5.SetOrigin(0.5, 0.5, -0.508)
plane_5.SetPoint1(0.5, -0.5, -0.508)
plane_5.SetPoint2(-0.5, 0.5, -0.508)
plane_5.SetXResolution(5)
plane_5.SetYResolution(5)
plane_5.Update()

plane_6 = vtkPlaneSource()
plane_6.SetOrigin(0.5, 0.5, 0.508)
plane_6.SetPoint1(-0.5, 0.5, 0.508)
plane_6.SetPoint2(0.5, -0.5, 0.508)
plane_6.SetXResolution(5)
plane_6.SetYResolution(5)
plane_6.Update()

# Append together
append = vtkAppendPolyData()
append.AddInputData(plane_1.GetOutput())
append.AddInputData(plane_2.GetOutput())
append.AddInputData(plane_3.GetOutput())
append.AddInputData(plane_4.GetOutput())
append.AddInputData(plane_5.GetOutput())
append.AddInputData(plane_6.GetOutput())

# Identity transform
identity_transform = vtkIdentityTransform()

filter_11 = vtkTransformPolyDataFilter()
filter_11.SetInputConnection(append.GetOutputPort())
filter_11.SetTransform(identity_transform)
mapper_11 = vtkDataSetMapper()
mapper_11.SetInputConnection(filter_11.GetOutputPort())
actor_11 = vtkActor()
actor_11.SetMapper(mapper_11)
actor_11.GetProperty().SetColor(1, 0, 0)
actor_11.GetProperty().SetRepresentationToWireframe()
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.25, 1.0)
renderer_0.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_0.AddActor(actor_11)

# Inverse identity transform
filter_12 = vtkTransformPolyDataFilter()
filter_12.SetInputConnection(append.GetOutputPort())
filter_12.SetTransform(identity_transform.GetInverse())
mapper_12 = vtkDataSetMapper()
mapper_12.SetInputConnection(filter_12.GetOutputPort())
actor_12 = vtkActor()
actor_12.SetMapper(mapper_12)
actor_12.GetProperty().SetColor(0.9, 0.9, 0)
actor_12.GetProperty().SetRepresentationToWireframe()
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.0, 0.0, 0.25, 0.5)
renderer_1.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_1.AddActor(actor_12)

# Linear transform
linear_transform = vtkTransform()
linear_transform.RotateX(50)
linear_transform.RotateY(30)
linear_transform.Translate(0.2, 0.1, -0.15)

filter_21 = vtkTransformPolyDataFilter()
filter_21.SetInputConnection(append.GetOutputPort())
filter_21.SetTransform(linear_transform)
mapper_21 = vtkDataSetMapper()
mapper_21.SetInputConnection(filter_21.GetOutputPort())
actor_21 = vtkActor()
actor_21.SetMapper(mapper_21)
actor_21.GetProperty().SetColor(1, 0, 0)
actor_21.GetProperty().SetRepresentationToWireframe()
renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.25, 0.5, 0.50, 1.0)
renderer_2.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_2.AddActor(actor_21)

# Inverse linear transform
filter_22 = vtkTransformPolyDataFilter()
filter_22.SetInputConnection(append.GetOutputPort())
filter_22.SetTransform(linear_transform.GetInverse())
mapper_22 = vtkDataSetMapper()
mapper_22.SetInputConnection(filter_22.GetOutputPort())
actor_22 = vtkActor()
actor_22.SetMapper(mapper_22)
actor_22.GetProperty().SetColor(0.9, 0.9, 0)
actor_22.GetProperty().SetRepresentationToWireframe()
renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.25, 0.0, 0.50, 0.5)
renderer_3.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_3.AddActor(actor_22)

# Perspective transform
matrix = vtkMatrix4x4()
matrix.SetElement(3, 0, 0.1)
matrix.SetElement(3, 1, 0.2)
matrix.SetElement(3, 2, 0.5)

perspective_transform = vtkPerspectiveTransform()
perspective_transform.SetMatrix(matrix)

filter_31 = vtkTransformPolyDataFilter()
filter_31.SetInputConnection(append.GetOutputPort())
filter_31.SetTransform(perspective_transform)
mapper_31 = vtkDataSetMapper()
mapper_31.SetInputConnection(filter_31.GetOutputPort())
actor_31 = vtkActor()
actor_31.SetMapper(mapper_31)
actor_31.GetProperty().SetColor(1, 0, 0)
actor_31.GetProperty().SetRepresentationToWireframe()
renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.50, 0.5, 0.75, 1.0)
renderer_4.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_4.AddActor(actor_31)

# Inverse perspective transform
filter_32 = vtkTransformPolyDataFilter()
filter_32.SetInputConnection(append.GetOutputPort())
filter_32.SetTransform(perspective_transform.GetInverse())
mapper_32 = vtkDataSetMapper()
mapper_32.SetInputConnection(filter_32.GetOutputPort())
actor_32 = vtkActor()
actor_32.SetMapper(mapper_32)
actor_32.GetProperty().SetColor(0.9, 0.9, 0)
actor_32.GetProperty().SetRepresentationToWireframe()
renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.5, 0.0, 0.75, 0.5)
renderer_5.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_5.AddActor(actor_32)

# Perspective transform concatenation
concat_transform = vtkPerspectiveTransform()
concat_transform.Concatenate(identity_transform)
concat_transform.Concatenate(linear_transform)
concat_transform.Concatenate(perspective_transform)

filter_41 = vtkTransformPolyDataFilter()
filter_41.SetInputConnection(append.GetOutputPort())
filter_41.SetTransform(concat_transform)
mapper_41 = vtkDataSetMapper()
mapper_41.SetInputConnection(filter_41.GetOutputPort())
actor_41 = vtkActor()
actor_41.SetMapper(mapper_41)
actor_41.GetProperty().SetColor(1, 0, 0)
actor_41.GetProperty().SetRepresentationToWireframe()
renderer_6 = vtkRenderer()
renderer_6.SetViewport(0.75, 0.5, 1.0, 1.0)
renderer_6.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_6.AddActor(actor_41)

# Inverse concatenated transform
filter_42 = vtkTransformPolyDataFilter()
filter_42.SetInputConnection(append.GetOutputPort())
filter_42.SetTransform(concat_transform.GetInverse())
mapper_42 = vtkDataSetMapper()
mapper_42.SetInputConnection(filter_42.GetOutputPort())
actor_42 = vtkActor()
actor_42.SetMapper(mapper_42)
actor_42.GetProperty().SetColor(0.9, 0.9, 0)
actor_42.GetProperty().SetRepresentationToWireframe()
renderer_7 = vtkRenderer()
renderer_7.SetViewport(0.75, 0.0, 1.0, 0.5)
renderer_7.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)
renderer_7.AddActor(actor_42)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetWindowName("transform polydata pipeline")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
