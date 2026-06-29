#!/usr/bin/env python

# Triangulate points on a sphere using a transform to map into 2D.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate points on a sphere (data not in z = f(x,y) form)
math_util = vtkMath()
points = vtkPoints()
vectors = vtkFloatArray()
vectors.SetNumberOfComponents(3)
for i in range(100):
    theta = math_util.Random(0.31415, 2.8)
    phi = math_util.Random(0.31415, 2.8)
    x = math.cos(theta) * math.sin(phi)
    y = math.sin(theta) * math.sin(phi)
    z = math.cos(phi)
    points.InsertPoint(i, x, y, z)
    vectors.InsertTuple3(i, x, y, z)

profile = vtkPolyData()
profile.SetPoints(points)
profile.GetPointData().SetVectors(vectors)

# Build a transform that rotates data into z = f(x,y) form
transform = vtkTransform()
transform.RotateX(90)

# Filter: Delaunay 2D with the specified transform
delaunay = vtkDelaunay2D()
delaunay.SetInputData(profile)
delaunay.SetTransform(transform)
delaunay.BoundingTriangulationOff()
delaunay.SetTolerance(0.001)
delaunay.SetAlpha(0.0)

# Filter: shrink triangles for visualization
shrink = vtkShrinkPolyData()
shrink.SetInputConnection(delaunay.GetOutputPort())

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(shrink.GetOutputPort())

# Actor
triangulation = vtkActor()
triangulation.SetMapper(mapper)
triangulation.GetProperty().SetColor(1, 0, 0)
triangulation.GetProperty().BackfaceCullingOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(triangulation)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("delaunay2d transform")

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Zoom(1.5)
camera.Azimuth(90)
camera.Elevation(30)
camera.Azimuth(-60)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
