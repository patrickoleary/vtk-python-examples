#!/usr/bin/env python

# Convert a rendered depth image to a point cloud using vtkDepthImageToPointCloud.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkRendererSource,
)
from vtkmodules.vtkRenderingImage import vtkDepthImageToPointCloud

# Plane with elevation coloring
plane = vtkPlaneSource()
plane.SetOrigin(0, 0, 0)
plane.SetPoint1(2, 0, 0)
plane.SetPoint2(0, 1, 0)

elevation = vtkElevationFilter()
elevation.SetInputConnection(plane.GetOutputPort())
elevation.SetLowPoint(0, 0, 0)
elevation.SetHighPoint(0, 1, 0)

plane_mapper = vtkPolyDataMapper()
plane_mapper.SetInputConnection(elevation.GetOutputPort())

plane_actor = vtkActor()
plane_actor.SetMapper(plane_mapper)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(plane_actor)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(700, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("depth to point cloud")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Functional render: required to populate depth buffer for RendererSource
render_window.Render()

# Extract rendered geometry and convert to point cloud
renderer_source = vtkRendererSource()
renderer_source.SetInput(renderer_0)
renderer_source.WholeWindowOff()
renderer_source.DepthValuesOn()
renderer_source.Update()

point_cloud = vtkDepthImageToPointCloud()
point_cloud.SetInputConnection(renderer_source.GetOutputPort())
point_cloud.SetCamera(renderer_0.GetActiveCamera())
point_cloud.CullFarPointsOff()
point_cloud.Update()

point_cloud_mapper = vtkPolyDataMapper()
point_cloud_mapper.SetInputConnection(point_cloud.GetOutputPort())

point_cloud_actor = vtkActor()
point_cloud_actor.SetMapper(point_cloud_mapper)

renderer_1.AddActor(point_cloud_actor)

# Scene
camera_1 = renderer_1.GetActiveCamera()
camera_1.SetFocalPoint(0, 0, 0)
camera_1.SetPosition(1, 1, 1)
renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
