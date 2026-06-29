#!/usr/bin/env python
# Demonstrate vtkmPointTransform applying rotation to a warped plane source.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmPointTransform
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Plane source.
plane = vtkPlaneSource()
res = 300
plane.SetXResolution(res)
plane.SetYResolution(res)
plane.SetOrigin(-10.0, -10.0, 0.0)
plane.SetPoint1(10.0, -10.0, 0.0)
plane.SetPoint2(-10.0, 10.0, 0.0)

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

# Point transform via VTK-m.
pf = vtkmPointTransform()
pf.SetInputData(pd)
transform_matrix = vtkTransform()
transform_matrix.RotateX(30)
transform_matrix.RotateY(60)
transform_matrix.RotateZ(90)
pf.SetTransform(transform_matrix)

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(pf.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.0, 0.0, 0.0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm point transform")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
