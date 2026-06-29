#!/usr/bin/env python

# Generate random planes to form a convex polyhedron using vtkHull.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import (
    vtkFloatArray,
    vtkMath,
    vtkPoints,
)
from vtkmodules.vtkCommonDataModel import (
    vtkPlanes,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkHull
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create random points on a unit sphere with outward normals
math_obj = vtkMath()
points = vtkPoints()
normals = vtkFloatArray()
normals.SetNumberOfComponents(3)

for i in range(100):
    radius = 1.0
    theta = math_obj.Random(0, 360)
    phi = math_obj.Random(0, 180)
    x = radius * math.sin(phi) * math.cos(theta)
    y = radius * math.sin(phi) * math.sin(theta)
    z = radius * math.cos(phi)
    points.InsertPoint(i, x, y, z)
    normals.InsertTuple3(i, x, y, z)

# Define planes from the points and normals
planes = vtkPlanes()
planes.SetPoints(points)
planes.SetNormals(normals)

# Generate the convex hull
hull = vtkHull()
hull.SetPlanes(planes)

hull_polydata = vtkPolyData()
hull.GenerateHull(hull_polydata, -20, 20, -20, 20, -20, 20)

# Map and display the hull
hull_mapper = vtkPolyDataMapper()
hull_mapper.SetInputData(hull_polydata)

hull_actor = vtkActor()
hull_actor.SetMapper(hull_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(hull_actor)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(250, 250)
render_window.SetWindowName("hull")

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(1.5)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
