#!/usr/bin/env python

# Compare vtkSimpleElevationFilter and vtkElevationFilter on a
# cosine-deformed plane mesh in two viewports.

import math

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkElevationFilter,
    vtkSimpleElevationFilter,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 200

# Source: plane mesh
plane = vtkPlaneSource()
plane.SetXResolution(resolution)
plane.SetYResolution(resolution)
plane.SetOrigin(-10, -10, 0)
plane.SetPoint1(10, -10, 0)
plane.SetPoint2(-10, 10, 0)

# Triangulate
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(plane.GetOutputPort())
triangle_filter.Update()

# Deform to a cosine surface
deformed_mesh = vtkPolyData()
deformed_mesh.CopyStructure(triangle_filter.GetOutput())
num_pts = deformed_mesh.GetNumberOfPoints()
old_pts = triangle_filter.GetOutput().GetPoints()
new_pts = vtkPoints()
new_pts.SetNumberOfPoints(num_pts)
for i in range(num_pts):
    pt = old_pts.GetPoint(i)
    r = math.sqrt(pt[0] * pt[0] + pt[1] * pt[1])
    z = 1.5 * math.cos(2 * r)
    new_pts.SetPoint(i, pt[0], pt[1], z)
deformed_mesh.SetPoints(new_pts)

# Simple elevation filter (projects onto direction vector)
simple_elevation = vtkSimpleElevationFilter()
simple_elevation.SetInputData(deformed_mesh)

simple_mapper = vtkPolyDataMapper()
simple_mapper.SetInputConnection(simple_elevation.GetOutputPort())

simple_actor = vtkActor()
simple_actor.SetMapper(simple_mapper)

# Elevation filter (projects onto low-high line)
elevation = vtkElevationFilter()
elevation.SetInputData(deformed_mesh)
elevation.SetLowPoint(0, 0, -1.5)
elevation.SetHighPoint(0, 0, 1.5)
elevation.SetScalarRange(-1.5, 1.5)

elevation_mapper = vtkPolyDataMapper()
elevation_mapper.SetInputConnection(elevation.GetOutputPort())

elevation_actor = vtkActor()
elevation_actor.SetMapper(elevation_mapper)

# Two viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.SetBackground(0, 0, 0)
renderer_0.AddActor(simple_actor)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)
renderer_1.AddActor(elevation_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(500, 250)
render_window.SetWindowName("elevation")

# Scene
camera = vtkCamera()
camera.SetPosition(1, 1, 1)
renderer_0.SetActiveCamera(camera)
renderer_1.SetActiveCamera(camera)
renderer_0.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
