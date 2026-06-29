#!/usr/bin/env python

# Test flexible joints using transform concatenation pipeline.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkCylinderSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# First segment
cylinder_1 = vtkCylinderSource()
cylinder_1.SetHeight(1.6)
cylinder_1.SetRadius(0.2)
cylinder_1.SetCenter(0, 0.8, 0)

transform_1 = vtkTransform()

filter_1 = vtkTransformPolyDataFilter()
filter_1.SetInputConnection(cylinder_1.GetOutputPort())
filter_1.SetTransform(transform_1)

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(filter_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetColor(1, 0, 0)

# Second segment with relative transform
cylinder_2 = vtkCylinderSource()
cylinder_2.SetHeight(1.6)
cylinder_2.SetRadius(0.15)
cylinder_2.SetCenter(0, 0.8, 0)

joint_1 = vtkTransform()

transform_2 = vtkTransform()
transform_2.SetInput(transform_1)
transform_2.Translate(0, 1.6, 0)
transform_2.Concatenate(joint_1)

filter_2 = vtkTransformPolyDataFilter()
filter_2.SetInputConnection(cylinder_2.GetOutputPort())
filter_2.SetTransform(transform_2)

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(filter_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)
actor_2.GetProperty().SetColor(0.0, 0.7, 1.0)

# Third segment with relative transform
cylinder_3 = vtkCylinderSource()
cylinder_3.SetHeight(0.5)
cylinder_3.SetRadius(0.1)
cylinder_3.SetCenter(0, 0.25, 0)

joint_2 = vtkTransform()

transform_3 = vtkTransform()
transform_3.SetInput(transform_2)
transform_3.Translate(0, 1.6, 0)
transform_3.Concatenate(joint_2)

filter_3 = vtkTransformPolyDataFilter()
filter_3.SetInputConnection(cylinder_3.GetOutputPort())
filter_3.SetTransform(transform_3)

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(filter_3.GetOutputPort())

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)
actor_3.GetProperty().SetColor(0.9, 0.9, 0)

# Set joint angles
joint_1.Identity()
joint_1.RotateY(70)
joint_1.RotateX(85)

joint_2.Identity()
joint_2.RotateY(50)
joint_2.RotateX(90)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("transform concatenation")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera(-1, 1, -0.1, 2, -3, 3)

interactor.Initialize()
interactor.Start()
