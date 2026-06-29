#!/usr/bin/env python
# Demonstrate vtkmPointElevation on a warped plane source.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmPointElevation
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Plane source.
plane = vtkPlaneSource()
res = 200
plane.SetXResolution(res)
plane.SetYResolution(res)
plane.SetOrigin(-10, -10, 0)
plane.SetPoint1(10, -10, 0)
plane.SetPoint2(-10, 10, 0)

# Triangulate.
tf = vtkTriangleFilter()
tf.SetInputConnection(plane.GetOutputPort())
tf.Update()

# Warp points into a cosine surface.
pd = vtkPolyData()
pd.CopyStructure(tf.GetOutput())
num_pts = pd.GetNumberOfPoints()
old_pts = tf.GetOutput().GetPoints()
new_pts = vtkPoints()
new_pts.SetNumberOfPoints(num_pts)
for i in range(num_pts):
    pt = old_pts.GetPoint(i)
    r = math.sqrt(pt[0] ** 2 + pt[1] ** 2)
    z = 1.5 * math.cos(2 * r)
    new_pts.SetPoint(i, pt[0], pt[1], z)
pd.SetPoints(new_pts)

# Point elevation via VTK-m.
pe = vtkmPointElevation()
pe.SetInputData(pd)
pe.SetLowPoint(0, 0, -1.5)
pe.SetHighPoint(0, 0, 1.5)
pe.SetScalarRange(-1.5, 1.5)

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(pe.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SelectColorArray("elevation")

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm point elevation")

# Scene
camera = vtkCamera()
camera.SetPosition(1, 50, 50)
renderer.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
