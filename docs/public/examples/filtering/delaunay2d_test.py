#!/usr/bin/env python

# Triangulate random 2D points using Delaunay triangulation.

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

# Generate 1000 random points in the unit square
math_util = vtkMath()
points = vtkPoints()
for i in range(1000):
    points.InsertPoint(i, math_util.Random(0, 1), math_util.Random(0, 1), 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Filter: Delaunay 2D triangulation with bounding triangulation
delaunay = vtkDelaunay2D()
delaunay.SetInputData(profile)
delaunay.SetBoundingTriangulation(True)
delaunay.SetAlpha(0.0)
delaunay.SetTolerance(0.001)

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
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(500, 500)
render_window.SetWindowName("delaunay2d test")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
