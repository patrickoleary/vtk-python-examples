#!/usr/bin/env python
# Demonstrate vtkMatrixToLinearTransform and vtkMatrixToHomogeneousTransform on a cube of planes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonMath import vtkMatrix4x4
from vtkmodules.vtkCommonTransforms import (
    vtkMatrixToHomogeneousTransform,
    vtkMatrixToLinearTransform,
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

# Build a cube from six plane sources.
plane_top = vtkPlaneSource()
plane_top.SetOrigin(0.5, 0.508, -0.5)
plane_top.SetPoint1(-0.5, 0.508, -0.5)
plane_top.SetPoint2(0.5, 0.508, 0.5)
plane_top.SetXResolution(5)
plane_top.SetYResolution(5)

plane_left = vtkPlaneSource()
plane_left.SetOrigin(-0.508, 0.5, -0.5)
plane_left.SetPoint1(-0.508, -0.5, -0.5)
plane_left.SetPoint2(-0.508, 0.5, 0.5)
plane_left.SetXResolution(5)
plane_left.SetYResolution(5)

plane_bottom = vtkPlaneSource()
plane_bottom.SetOrigin(-0.5, -0.508, -0.5)
plane_bottom.SetPoint1(0.5, -0.508, -0.5)
plane_bottom.SetPoint2(-0.5, -0.508, 0.5)
plane_bottom.SetXResolution(5)
plane_bottom.SetYResolution(5)

plane_right = vtkPlaneSource()
plane_right.SetOrigin(0.508, -0.5, -0.5)
plane_right.SetPoint1(0.508, 0.5, -0.5)
plane_right.SetPoint2(0.508, -0.5, 0.5)
plane_right.SetXResolution(5)
plane_right.SetYResolution(5)

plane_back = vtkPlaneSource()
plane_back.SetOrigin(0.5, 0.5, -0.508)
plane_back.SetPoint1(0.5, -0.5, -0.508)
plane_back.SetPoint2(-0.5, 0.5, -0.508)
plane_back.SetXResolution(5)
plane_back.SetYResolution(5)

plane_front = vtkPlaneSource()
plane_front.SetOrigin(0.5, 0.5, 0.508)
plane_front.SetPoint1(-0.5, 0.5, 0.508)
plane_front.SetPoint2(0.5, -0.5, 0.508)
plane_front.SetXResolution(5)
plane_front.SetYResolution(5)

append = vtkAppendPolyData()
append.AddInputConnection(plane_top.GetOutputPort())
append.AddInputConnection(plane_left.GetOutputPort())
append.AddInputConnection(plane_bottom.GetOutputPort())
append.AddInputConnection(plane_right.GetOutputPort())
append.AddInputConnection(plane_back.GetOutputPort())
append.AddInputConnection(plane_front.GetOutputPort())

# Linear transform from matrix.
linear_transform = vtkMatrixToLinearTransform()
linear_matrix = vtkMatrix4x4()
linear_transform.SetInput(linear_matrix)
linear_matrix.SetElement(0, 0, 1.127631)
linear_matrix.SetElement(0, 1, 0.205212)
linear_matrix.SetElement(0, 2, -0.355438)
linear_matrix.SetElement(1, 0, 0.000000)
linear_matrix.SetElement(1, 1, 0.692820)
linear_matrix.SetElement(1, 2, 0.400000)
linear_matrix.SetElement(2, 0, 0.200000)
linear_matrix.SetElement(2, 1, -0.469846)
linear_matrix.SetElement(2, 2, 0.813798)

linear_fwd_filter = vtkTransformPolyDataFilter()
linear_fwd_filter.SetInputConnection(append.GetOutputPort())
linear_fwd_filter.SetTransform(linear_transform)
linear_fwd_mapper = vtkDataSetMapper()
linear_fwd_mapper.SetInputConnection(linear_fwd_filter.GetOutputPort())
linear_fwd_actor = vtkActor()
linear_fwd_actor.SetMapper(linear_fwd_mapper)
linear_fwd_actor.GetProperty().SetColor(1, 0, 0)
linear_fwd_actor.GetProperty().SetRepresentationToWireframe()

# Inverse linear transform.
linear_inv_filter = vtkTransformPolyDataFilter()
linear_inv_filter.SetInputConnection(append.GetOutputPort())
linear_inv_filter.SetTransform(linear_transform.GetInverse())
linear_inv_mapper = vtkDataSetMapper()
linear_inv_mapper.SetInputConnection(linear_inv_filter.GetOutputPort())
linear_inv_actor = vtkActor()
linear_inv_actor.SetMapper(linear_inv_mapper)
linear_inv_actor.GetProperty().SetColor(0.9, 0.9, 0)
linear_inv_actor.GetProperty().SetRepresentationToWireframe()

# Perspective transform from matrix.
perspective_matrix = vtkMatrix4x4()
perspective_matrix.SetElement(3, 0, -0.11)
perspective_matrix.SetElement(3, 1, 0.3)
perspective_matrix.SetElement(3, 2, 0.2)
homogeneous_transform = vtkMatrixToHomogeneousTransform()
homogeneous_transform.SetInput(perspective_matrix)

homogeneous_fwd_filter = vtkTransformPolyDataFilter()
homogeneous_fwd_filter.SetInputConnection(append.GetOutputPort())
homogeneous_fwd_filter.SetTransform(homogeneous_transform)
homogeneous_fwd_mapper = vtkDataSetMapper()
homogeneous_fwd_mapper.SetInputConnection(homogeneous_fwd_filter.GetOutputPort())
homogeneous_fwd_actor = vtkActor()
homogeneous_fwd_actor.SetMapper(homogeneous_fwd_mapper)
homogeneous_fwd_actor.GetProperty().SetColor(1, 0, 0)
homogeneous_fwd_actor.GetProperty().SetRepresentationToWireframe()

# Inverse perspective transform.
homogeneous_inv_filter = vtkTransformPolyDataFilter()
homogeneous_inv_filter.SetInputConnection(append.GetOutputPort())
homogeneous_inv_filter.SetTransform(homogeneous_transform.GetInverse())
homogeneous_inv_mapper = vtkDataSetMapper()
homogeneous_inv_mapper.SetInputConnection(homogeneous_inv_filter.GetOutputPort())
homogeneous_inv_actor = vtkActor()
homogeneous_inv_actor.SetMapper(homogeneous_inv_mapper)
homogeneous_inv_actor.GetProperty().SetColor(0.9, 0.9, 0)
homogeneous_inv_actor.GetProperty().SetRepresentationToWireframe()

# Linear concatenation (should yield identity).
identity_transform = vtkTransform()
identity_transform.Concatenate(linear_transform)
identity_transform.Concatenate(linear_transform.GetInverse())

identity_fwd_filter = vtkTransformPolyDataFilter()
identity_fwd_filter.SetInputConnection(append.GetOutputPort())
identity_fwd_filter.SetTransform(identity_transform)
identity_fwd_mapper = vtkDataSetMapper()
identity_fwd_mapper.SetInputConnection(identity_fwd_filter.GetOutputPort())
identity_fwd_actor = vtkActor()
identity_fwd_actor.SetMapper(identity_fwd_mapper)
identity_fwd_actor.GetProperty().SetColor(1, 0, 0)
identity_fwd_actor.GetProperty().SetRepresentationToWireframe()

# Inverse of identity concatenation.
identity_inv_filter = vtkTransformPolyDataFilter()
identity_inv_filter.SetInputConnection(append.GetOutputPort())
identity_inv_filter.SetTransform(identity_transform.GetInverse())
identity_inv_mapper = vtkDataSetMapper()
identity_inv_mapper.SetInputConnection(identity_inv_filter.GetOutputPort())
identity_inv_actor = vtkActor()
identity_inv_actor.SetMapper(identity_inv_mapper)
identity_inv_actor.GetProperty().SetColor(0.9, 0.9, 0)
identity_inv_actor.GetProperty().SetRepresentationToWireframe()

# Perspective transform concatenation.
combined_transform = vtkPerspectiveTransform()
combined_transform.Concatenate(linear_transform)
combined_transform.Concatenate(homogeneous_transform)
combined_transform.Concatenate(identity_transform)

combined_fwd_filter = vtkTransformPolyDataFilter()
combined_fwd_filter.SetInputConnection(append.GetOutputPort())
combined_fwd_filter.SetTransform(combined_transform)
combined_fwd_mapper = vtkDataSetMapper()
combined_fwd_mapper.SetInputConnection(combined_fwd_filter.GetOutputPort())
combined_fwd_actor = vtkActor()
combined_fwd_actor.SetMapper(combined_fwd_mapper)
combined_fwd_actor.GetProperty().SetColor(1, 0, 0)
combined_fwd_actor.GetProperty().SetRepresentationToWireframe()

# Inverse of perspective concatenation.
combined_inv_filter = vtkTransformPolyDataFilter()
combined_inv_filter.SetInputConnection(append.GetOutputPort())
combined_inv_filter.SetTransform(combined_transform.GetInverse())
combined_inv_mapper = vtkDataSetMapper()
combined_inv_mapper.SetInputConnection(combined_inv_filter.GetOutputPort())
combined_inv_actor = vtkActor()
combined_inv_actor.SetMapper(combined_inv_mapper)
combined_inv_actor.GetProperty().SetColor(0.9, 0.9, 0)
combined_inv_actor.GetProperty().SetRepresentationToWireframe()

renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.5, 0.25, 1.0)
renderer_0.AddActor(linear_fwd_actor)
renderer_0.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.0, 0.0, 0.25, 0.5)
renderer_1.AddActor(linear_inv_actor)
renderer_1.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.25, 0.5, 0.50, 1.0)
renderer_2.AddActor(homogeneous_fwd_actor)
renderer_2.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_3 = vtkRenderer()
renderer_3.SetViewport(0.25, 0.0, 0.50, 0.5)
renderer_3.AddActor(homogeneous_inv_actor)
renderer_3.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_4 = vtkRenderer()
renderer_4.SetViewport(0.50, 0.5, 0.75, 1.0)
renderer_4.AddActor(identity_fwd_actor)
renderer_4.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_5 = vtkRenderer()
renderer_5.SetViewport(0.5, 0.0, 0.75, 0.5)
renderer_5.AddActor(identity_inv_actor)
renderer_5.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_6 = vtkRenderer()
renderer_6.SetViewport(0.75, 0.5, 1.0, 1.0)
renderer_6.AddActor(combined_fwd_actor)
renderer_6.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

renderer_7 = vtkRenderer()
renderer_7.SetViewport(0.75, 0.0, 1.0, 0.5)
renderer_7.AddActor(combined_inv_actor)
renderer_7.ResetCamera(-0.5, 0.5, -0.5, 0.5, -1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(600, 300)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.AddRenderer(renderer_3)
render_window.AddRenderer(renderer_4)
render_window.AddRenderer(renderer_5)
render_window.AddRenderer(renderer_6)
render_window.AddRenderer(renderer_7)
render_window.SetWindowName("matrix to transform")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
