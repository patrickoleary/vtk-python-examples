#!/usr/bin/env python

# Convert depth image to point cloud with separate color and depth inputs.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPointGaussianMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
    vtkRendererSource,
)
from vtkmodules.vtkRenderingImage import vtkDepthImageToPointCloud

# Sphere with elevation coloring
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(1)

elevation = vtkElevationFilter()
elevation.SetInputConnection(sphere.GetOutputPort())
elevation.SetLowPoint(0, -1, 0)
elevation.SetHighPoint(0, 1, 0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(elevation.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1)
renderer_0.AddActor(sphere_actor)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1, 1)
renderer_1.SetBackground(0, 0, 0)

# Render window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(700, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("depth to point cloud two inputs")

# Scene (renderer_0 camera — must precede depth capture)
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().SetClippingRange(6, 9)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Functional render: required to populate depth buffer for RendererSource
render_window.Render()

# Extract depth-only image
depth_source = vtkRendererSource()
depth_source.SetInput(renderer_0)
depth_source.WholeWindowOff()
depth_source.DepthValuesOnlyOn()
depth_source.Update()

# Extract color-only image
color_source = vtkRendererSource()
color_source.SetInput(renderer_0)
color_source.WholeWindowOff()
color_source.DepthValuesOff()
color_source.DepthValuesInScalarsOff()
color_source.Update()

# Convert to point cloud using two inputs
point_cloud = vtkDepthImageToPointCloud()
point_cloud.SetInputConnection(0, depth_source.GetOutputPort())
point_cloud.SetInputConnection(1, color_source.GetOutputPort())
point_cloud.SetCamera(renderer_0.GetActiveCamera())
point_cloud.CullNearPointsOn()
point_cloud.CullFarPointsOn()
point_cloud.ProduceVertexCellArrayOff()
point_cloud.Update()

point_cloud_mapper = vtkPointGaussianMapper()
point_cloud_mapper.SetInputConnection(point_cloud.GetOutputPort())
point_cloud_mapper.EmissiveOff()
point_cloud_mapper.SetScaleFactor(0.0)

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
