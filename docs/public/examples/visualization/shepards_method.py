#!/usr/bin/env python

# Test vtkShepardMethod with three power parameters in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkImagingHybrid import vtkShepardMethod
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create points and scalars with some on volume grid points
points = vtkPoints()
points.InsertPoint(0, -1, -1, -1)
points.InsertPoint(1, 1, -1, -1)
points.InsertPoint(2, 0, 0, -1)
points.InsertPoint(3, -1, 1, -1)
points.InsertPoint(4, 1, 1, -1)
points.InsertPoint(5, -1, -1, 0)
points.InsertPoint(6, 1, -1, 0)
points.InsertPoint(7, 0, 0, 0)
points.InsertPoint(8, -1, 1, 0)
points.InsertPoint(9, 1, 1, 0)
points.InsertPoint(10, -1, -1, 1)
points.InsertPoint(11, 1, -1, 1)
points.InsertPoint(12, 0, 0, 1)
points.InsertPoint(13, -1, 1, 1)
points.InsertPoint(14, 1, 1, 1)

scalars = vtkFloatArray()
scalars.InsertValue(0, 5)
scalars.InsertValue(1, 5)
scalars.InsertValue(2, 10)
scalars.InsertValue(3, 5)
scalars.InsertValue(4, 5)
scalars.InsertValue(5, 10)
scalars.InsertValue(6, 10)
scalars.InsertValue(7, 20)
scalars.InsertValue(8, 10)
scalars.InsertValue(9, 10)
scalars.InsertValue(10, 20)
scalars.InsertValue(11, 20)
scalars.InsertValue(12, 40)
scalars.InsertValue(13, 20)
scalars.InsertValue(14, 20)

profile = vtkPolyData()
profile.SetPoints(points)
profile.GetPointData().SetScalars(scalars)

dim = 51

# Shepard P=1
shepard_1 = vtkShepardMethod()
shepard_1.SetInputData(profile)
shepard_1.SetModelBounds(-2, 2, -2, 2, -1, 1)
shepard_1.SetSampleDimensions(dim, dim, dim)
shepard_1.SetNullValue(0)
shepard_1.SetMaximumDistance(1)
shepard_1.SetPowerParameter(1)

mapper_1 = vtkDataSetMapper()
mapper_1.SetInputConnection(shepard_1.GetOutputPort())
mapper_1.SetScalarRange(0, 40)

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Shepard P=2 (default)
shepard_2 = vtkShepardMethod()
shepard_2.SetInputData(profile)
shepard_2.SetModelBounds(-2, 2, -2, 2, -1, 1)
shepard_2.SetSampleDimensions(dim, dim, dim)
shepard_2.SetNullValue(0)
shepard_2.SetMaximumDistance(1)

mapper_2 = vtkDataSetMapper()
mapper_2.SetInputConnection(shepard_2.GetOutputPort())
mapper_2.SetScalarRange(0, 40)

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Shepard P=3
shepard_3 = vtkShepardMethod()
shepard_3.SetInputData(profile)
shepard_3.SetModelBounds(-2, 2, -2, 2, -1, 1)
shepard_3.SetSampleDimensions(dim, dim, dim)
shepard_3.SetNullValue(0)
shepard_3.SetMaximumDistance(1)
shepard_3.SetPowerParameter(3)

mapper_3 = vtkDataSetMapper()
mapper_3.SetInputConnection(shepard_3.GetOutputPort())
mapper_3.SetScalarRange(0, 40)

actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.3333, 1)
renderer_0.AddActor(actor_1)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.3333, 0, 0.6667, 1)
renderer_1.AddActor(actor_2)
renderer_1.SetBackground(1, 1, 1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.6667, 0, 1, 1)
renderer_2.AddActor(actor_3)
renderer_2.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("shepards method")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetPosition(1, 1, 1)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
