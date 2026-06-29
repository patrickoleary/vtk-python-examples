#!/usr/bin/env python

# Triangulate random 3D points using Delaunay 3D with alpha shapes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay3D
from vtkmodules.vtkFiltersGeneral import vtkShrinkFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Generate 25 random points in the unit cube
math_util = vtkMath()
points = vtkPoints()
for i in range(25):
    points.InsertPoint(i, math_util.Random(0, 1), math_util.Random(0, 1), math_util.Random(0, 1))

profile = vtkPolyData()
profile.SetPoints(points)

# Filter: Delaunay 3D triangulation with alpha
delaunay = vtkDelaunay3D()
delaunay.SetInputData(profile)
delaunay.BoundingTriangulationOn()
delaunay.SetTolerance(0.01)
delaunay.SetAlpha(0.2)
delaunay.BoundingTriangulationOff()

# Filter: shrink tetrahedra for visualization
shrink = vtkShrinkFilter()
shrink.SetInputConnection(delaunay.GetOutputPort())
shrink.SetShrinkFactor(0.9)

# Mapper
mapper = vtkDataSetMapper()
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
render_window.SetSize(250, 250)
render_window.SetWindowName("delaunay3d")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
