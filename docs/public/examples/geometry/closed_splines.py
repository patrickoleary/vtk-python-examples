#!/usr/bin/env python
# Demonstrate closed Cardinal and Kochanek splines on a square of control points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonComputationalGeometry import vtkCardinalSpline, vtkKochanekSpline
from vtkmodules.vtkCommonCore import vtkPoints
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

colors = vtkNamedColors()

# Closed Kochanek splines.
k_spline_x = vtkKochanekSpline()
k_spline_x.ClosedOn()
k_spline_y = vtkKochanekSpline()
k_spline_y.ClosedOn()
k_spline_z = vtkKochanekSpline()
k_spline_z.ClosedOn()

# Closed Cardinal splines.
c_spline_x = vtkCardinalSpline()
c_spline_x.ClosedOn()
c_spline_y = vtkCardinalSpline()
c_spline_y.ClosedOn()
c_spline_z = vtkCardinalSpline()
c_spline_z.ClosedOn()

# Control points forming a square.
control_points = [(-1.0, -1.0, 0.0), (1.0, -1.0, 0.0), (1.0, 1.0, 0.0), (-1.0, 1.0, 0.0)]

input_points = vtkPoints()
for i, (x, y, z) in enumerate(control_points):
    k_spline_x.AddPoint(i, x)
    k_spline_y.AddPoint(i, y)
    k_spline_z.AddPoint(i, z)
    c_spline_x.AddPoint(i, x)
    c_spline_y.AddPoint(i, y)
    c_spline_z.AddPoint(i, z)
    input_points.InsertPoint(i, x, y, z)

input_data = vtkPolyData()
input_data.SetPoints(input_points)

# Glyph control points.
balls = vtkSphereSource()
balls.SetRadius(0.04)
balls.SetPhiResolution(10)
balls.SetThetaResolution(10)

glyph_points = vtkGlyph3D()
glyph_points.SetInputData(input_data)
glyph_points.SetSourceConnection(balls.GetOutputPort())

glyph_mapper = vtkPolyDataMapper()
glyph_mapper.SetInputConnection(glyph_points.GetOutputPort())

glyph_actor = vtkActor()
glyph_actor.SetMapper(glyph_mapper)
tomato_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", tomato_rgb)
glyph_actor.GetProperty().SetDiffuseColor(tomato_rgb)
glyph_actor.GetProperty().SetSpecular(0.3)
glyph_actor.GetProperty().SetSpecularPower(30)

# Evaluate splines.
number_of_input_points = 5
number_of_output_points = 100
offset = 1.0

k_points = vtkPoints()
c_points = vtkPoints()
for i in range(number_of_output_points):
    t = (number_of_input_points - offset) / (number_of_output_points - 1) * i
    k_points.InsertPoint(i, k_spline_x.Evaluate(t), k_spline_y.Evaluate(t), k_spline_z.Evaluate(t))
    c_points.InsertPoint(i, c_spline_x.Evaluate(t), c_spline_y.Evaluate(t), c_spline_z.Evaluate(t))

lines = vtkCellArray()
lines.InsertNextCell(number_of_output_points)
for i in range(number_of_output_points):
    lines.InsertCellPoint(i)

# Kochanek spline polydata.
k_profile_data = vtkPolyData()
k_profile_data.SetPoints(k_points)
k_profile_data.SetLines(lines)

k_tubes = vtkTubeFilter()
k_tubes.SetNumberOfSides(8)
k_tubes.SetInputData(k_profile_data)
k_tubes.SetRadius(0.01)

k_mapper = vtkPolyDataMapper()
k_mapper.SetInputConnection(k_tubes.GetOutputPort())

banana_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("banana", banana_rgb)
k_actor = vtkActor()
k_actor.SetMapper(k_mapper)
k_actor.GetProperty().SetDiffuseColor(banana_rgb)
k_actor.GetProperty().SetSpecular(0.3)
k_actor.GetProperty().SetSpecularPower(30)

# Cardinal spline polydata.
c_profile_data = vtkPolyData()
c_profile_data.SetPoints(c_points)
c_profile_data.SetLines(lines)

c_tubes = vtkTubeFilter()
c_tubes.SetNumberOfSides(8)
c_tubes.SetInputData(c_profile_data)
c_tubes.SetRadius(0.01)

c_mapper = vtkPolyDataMapper()
c_mapper.SetInputConnection(c_tubes.GetOutputPort())

peacock_rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("peacock", peacock_rgb)
c_actor = vtkActor()
c_actor.SetMapper(c_mapper)
c_actor.GetProperty().SetDiffuseColor(peacock_rgb)
c_actor.GetProperty().SetSpecular(0.3)
c_actor.GetProperty().SetSpecularPower(30)

renderer = vtkRenderer()
renderer.AddActor(glyph_actor)
renderer.AddActor(k_actor)
renderer.AddActor(c_actor)

render_window = vtkRenderWindow()
render_window.SetSize(300, 300)
render_window.AddRenderer(renderer)
render_window.SetWindowName("closed splines")

renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(1.5)
renderer.ResetCameraClippingRange()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
