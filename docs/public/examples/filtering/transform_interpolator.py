#!/usr/bin/env python

# Test vtkTransformInterpolator with colored cube keyframes.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkUnsignedCharArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkTransformInterpolator,
)

# Create a colored cube
cube_points = vtkPoints()
cube_points.InsertNextPoint(-1, -1, -1)
cube_points.InsertNextPoint(1, -1, -1)
cube_points.InsertNextPoint(1, 1, -1)
cube_points.InsertNextPoint(-1, 1, -1)
cube_points.InsertNextPoint(-1, -1, 1)
cube_points.InsertNextPoint(1, -1, 1)
cube_points.InsertNextPoint(1, 1, 1)
cube_points.InsertNextPoint(-1, 1, 1)

faces = vtkCellArray()
faces.InsertNextCell(4)
faces.InsertCellPoint(0)
faces.InsertCellPoint(3)
faces.InsertCellPoint(2)
faces.InsertCellPoint(1)
faces.InsertNextCell(4)
faces.InsertCellPoint(4)
faces.InsertCellPoint(5)
faces.InsertCellPoint(6)
faces.InsertCellPoint(7)
faces.InsertNextCell(4)
faces.InsertCellPoint(0)
faces.InsertCellPoint(1)
faces.InsertCellPoint(5)
faces.InsertCellPoint(4)
faces.InsertNextCell(4)
faces.InsertCellPoint(1)
faces.InsertCellPoint(2)
faces.InsertCellPoint(6)
faces.InsertCellPoint(5)
faces.InsertNextCell(4)
faces.InsertCellPoint(2)
faces.InsertCellPoint(3)
faces.InsertCellPoint(7)
faces.InsertCellPoint(6)
faces.InsertNextCell(4)
faces.InsertCellPoint(3)
faces.InsertCellPoint(0)
faces.InsertCellPoint(4)
faces.InsertCellPoint(7)

face_colors = vtkUnsignedCharArray()
face_colors.SetNumberOfComponents(3)
face_colors.SetNumberOfTuples(3)
face_colors.InsertComponent(0, 0, 255)
face_colors.InsertComponent(0, 1, 0)
face_colors.InsertComponent(0, 2, 0)
face_colors.InsertComponent(1, 0, 0)
face_colors.InsertComponent(1, 1, 255)
face_colors.InsertComponent(1, 2, 0)
face_colors.InsertComponent(2, 0, 255)
face_colors.InsertComponent(2, 1, 255)
face_colors.InsertComponent(2, 2, 0)
face_colors.InsertComponent(3, 0, 0)
face_colors.InsertComponent(3, 1, 0)
face_colors.InsertComponent(3, 2, 255)
face_colors.InsertComponent(4, 0, 255)
face_colors.InsertComponent(4, 1, 0)
face_colors.InsertComponent(4, 2, 255)
face_colors.InsertComponent(5, 0, 0)
face_colors.InsertComponent(5, 1, 255)
face_colors.InsertComponent(5, 2, 255)

cube = vtkPolyData()
cube.SetPoints(cube_points)
cube.SetPolys(faces)
cube.GetCellData().SetScalars(face_colors)

# Transform keyframes
transform_1 = vtkTransform()
transform_1.Translate(1, 2, 3)
transform_1.RotateX(15)
transform_1.Scale(4, 2, 1)

filter_1 = vtkTransformPolyDataFilter()
filter_1.SetInputData(cube)
filter_1.SetTransform(transform_1)
cube_1_mapper = vtkPolyDataMapper()
cube_1_mapper.SetInputConnection(filter_1.GetOutputPort())
cube_1 = vtkActor()
cube_1.SetMapper(cube_1_mapper)

transform_2 = vtkTransform()
transform_2.Translate(5, 10, 15)
transform_2.RotateX(22.5)
transform_2.RotateY(15)
transform_2.RotateZ(85)
transform_2.Scale(1, 2, 4)

filter_2 = vtkTransformPolyDataFilter()
filter_2.SetInputData(cube)
filter_2.SetTransform(transform_2)
cube_2_mapper = vtkPolyDataMapper()
cube_2_mapper.SetInputConnection(filter_2.GetOutputPort())
cube_2 = vtkActor()
cube_2.SetMapper(cube_2_mapper)

transform_3 = vtkTransform()
transform_3.Translate(5, -10, 15)
transform_3.RotateX(13)
transform_3.RotateY(72)
transform_3.RotateZ(-15)
transform_3.Scale(2, 4, 1)

filter_3 = vtkTransformPolyDataFilter()
filter_3.SetInputData(cube)
filter_3.SetTransform(transform_3)
cube_3_mapper = vtkPolyDataMapper()
cube_3_mapper.SetInputConnection(filter_3.GetOutputPort())
cube_3 = vtkActor()
cube_3.SetMapper(cube_3_mapper)

transform_4 = vtkTransform()
transform_4.Translate(10, -5, 5)
transform_4.RotateX(66)
transform_4.RotateY(19)
transform_4.RotateZ(24)
transform_4.Scale(2, 0.5, 1)

filter_4 = vtkTransformPolyDataFilter()
filter_4.SetInputData(cube)
filter_4.SetTransform(transform_4)
cube_4_mapper = vtkPolyDataMapper()
cube_4_mapper.SetInputConnection(filter_4.GetOutputPort())
cube_4 = vtkActor()
cube_4.SetMapper(cube_4_mapper)

# Interpolated cube
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputData(cube)
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Set up interpolator
interpolator = vtkTransformInterpolator()
interpolator.SetInterpolationTypeToSpline()
interpolator.AddTransform(0.0, transform_1)
interpolator.AddTransform(8.0, transform_2)
interpolator.AddTransform(18.2, transform_3)
interpolator.AddTransform(24.4, transform_4)

# Interpolate to a specific time
xform = vtkTransform()
interpolator.InterpolateTransform(13.2, xform)
cube_actor.SetUserMatrix(xform.GetMatrix())

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cube_1)
renderer.AddActor(cube_2)
renderer.AddActor(cube_3)
renderer.AddActor(cube_4)
renderer.AddActor(cube_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("transform interpolator")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetClippingRange(31.2977, 81.697)
camera.SetFocalPoint(3.0991, -2.00445, 9.78648)
camera.SetPosition(-44.8481, -25.871, 10.0645)
camera.SetViewAngle(30)
camera.SetViewUp(-0.0356378, 0.0599728, -0.997564)
renderer.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
