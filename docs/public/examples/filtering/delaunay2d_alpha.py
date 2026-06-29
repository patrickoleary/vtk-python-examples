#!/usr/bin/env python

# Triangulate random 2D points with alpha-shape filtering.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersGeneral import vtkShrinkPolyData
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate 100 random points in the unit square
math_util = vtkMath()
points = vtkPoints()
for i in range(100):
    points.InsertPoint(i, math_util.Random(0, 1), math_util.Random(0, 1), 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Filter: Delaunay 2D with alpha value to remove large triangles
delaunay = vtkDelaunay2D()
delaunay.SetInputData(profile)
delaunay.SetTolerance(0.001)
delaunay.SetAlpha(0.1)

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

# Renderer
renderer = vtkRenderer()
renderer.AddActor(triangulation)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("delaunay2d alpha")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
