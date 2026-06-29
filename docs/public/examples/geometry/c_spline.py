#!/usr/bin/env python
# Demonstrate vtkCardinalSpline interpolation through random 3D points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonComputationalGeometry import vtkCardinalSpline
from vtkmodules.vtkCommonCore import vtkMath, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D, vtkTubeFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

math_obj = vtkMath()

number_of_input_points = 30

spline_x = vtkCardinalSpline()
spline_y = vtkCardinalSpline()
spline_z = vtkCardinalSpline()

# Generate random points.
input_points = vtkPoints()
for i in range(number_of_input_points):
    x = math_obj.Random(0, 1)
    y = math_obj.Random(0, 1)
    z = math_obj.Random(0, 1)
    spline_x.AddPoint(i, x)
    spline_y.AddPoint(i, y)
    spline_z.AddPoint(i, z)
    input_points.InsertPoint(i, x, y, z)

input_data = vtkPolyData()
input_data.SetPoints(input_points)

# Glyph the input points as spheres.
balls = vtkSphereSource()
balls.SetRadius(0.01)
balls.SetPhiResolution(10)
balls.SetThetaResolution(10)

glyph_points = vtkGlyph3D()
glyph_points.SetInputData(input_data)
glyph_points.SetSourceConnection(balls.GetOutputPort())

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph_points.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
glyph_actor.GetProperty().SetDiffuseColor(1, 0.4, 0.4)
glyph_actor.GetProperty().SetSpecular(0.3)
glyph_actor.GetProperty().SetSpecularPower(30)

# Evaluate spline and create polyline.
number_of_output_points = 400
offset = 1.0

points = vtkPoints()
for i in range(number_of_output_points):
    t = (number_of_input_points - offset) / (number_of_output_points - 1) * i
    points.InsertPoint(i, spline_x.Evaluate(t), spline_y.Evaluate(t), spline_z.Evaluate(t))

lines = vtkCellArray()
lines.InsertNextCell(number_of_output_points)
for i in range(number_of_output_points):
    lines.InsertCellPoint(i)

profile_data = vtkPolyData()
profile_data.SetPoints(points)
profile_data.SetLines(lines)

# Tube filter for the spline curve.
profile_tubes = vtkTubeFilter()
profile_tubes.SetNumberOfSides(8)
profile_tubes.SetInputData(profile_data)
profile_tubes.SetRadius(0.005)

profile_mapper = vtkPolyDataMapper()
profile_mapper.SetInputConnection(profile_tubes.GetOutputPort())

profile_actor = vtkActor()
profile_actor.SetMapper(profile_mapper)
profile_actor.GetProperty().SetDiffuseColor(1, 1, 0.6)
profile_actor.GetProperty().SetSpecular(0.3)
profile_actor.GetProperty().SetSpecularPower(30)

renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.AddActor(profile_actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.AddRenderer(renderer)
render_window.SetWindowName("c spline")

renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
