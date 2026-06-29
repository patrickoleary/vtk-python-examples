#!/usr/bin/env python

# Generate random points, Delaunay triangulate them, and color by point
# connectivity count using vtkPointConnectivityFilter.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkDelaunay2D
from vtkmodules.vtkFiltersGeneral import vtkPointConnectivityFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

npts = 1000

# Generate random 2D points
vtk_math = vtkMath()
points = vtkPoints()
for i in range(npts):
    points.InsertPoint(i, vtk_math.Random(0, 1), vtk_math.Random(0, 1), 0.0)

profile = vtkPolyData()
profile.SetPoints(points)

# Delaunay triangulation
del2d = vtkDelaunay2D()
del2d.SetInputData(profile)
del2d.BoundingTriangulationOff()
del2d.SetTolerance(0.001)
del2d.SetAlpha(0.0)

# Compute point connectivity
conn = vtkPointConnectivityFilter()
conn.SetInputConnection(del2d.GetOutputPort())
conn.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(conn.GetOutputPort())
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Point Connectivity Count")
mapper.SetScalarRange(conn.GetOutput().GetPointData().GetArray("Point Connectivity Count").GetRange())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 1, 1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("point connectivity")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
camera = vtkCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(0, 0, 1)
renderer.SetActiveCamera(camera)
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
