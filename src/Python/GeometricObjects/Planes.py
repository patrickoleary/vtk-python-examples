#!/usr/bin/env python

# Demonstrate two ways to create vtkPlanes — from camera frustum planes and
# from bounding-box bounds.  A sphere is placed inside the frustum, and its
# bounding-box hull is shown as a wireframe around it, all in the same
# coordinate space.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonDataModel import (
    vtkPlanes,
    vtkPolyData,
)
from vtkmodules.vtkFiltersCore import vtkHull
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
moccasin_rgb = (1.0, 0.894, 0.710)
light_coral_rgb = (0.941, 0.502, 0.502)
light_blue_rgb = (0.529, 0.808, 0.922)
dark_slate_gray_background_rgb = (0.184, 0.310, 0.310)

# Source: a sphere positioned at the origin
sphere_source = vtkSphereSource()
sphere_source.SetRadius(0.5)
sphere_source.SetThetaResolution(32)
sphere_source.SetPhiResolution(32)
sphere_source.SetCenter(0.0, 0.0, -3.0)
sphere_source.Update()

# Mapper / Actor: solid sphere (light blue)
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(light_blue_rgb)

# ---- Method 1: vtkPlanes from camera frustum planes ----
frustum_planes = vtkPlanes()
frustum_camera = vtkCamera()
frustum_camera.SetClippingRange(1.0, 5.0)
planes_array = [0.0] * 24
frustum_camera.GetFrustumPlanes(1, planes_array)
frustum_planes.SetFrustumPlanes(planes_array)

# Filter: generate a convex hull from the frustum planes
frustum_hull = vtkHull()
frustum_hull.SetPlanes(frustum_planes)
frustum_pd = vtkPolyData()
frustum_hull.GenerateHull(frustum_pd, -10, 10, -10, 10, -10, 10)

# Mapper / Actor: frustum hull (moccasin wireframe)
frustum_mapper = vtkPolyDataMapper()
frustum_mapper.SetInputData(frustum_pd)

frustum_actor = vtkActor()
frustum_actor.SetMapper(frustum_mapper)
frustum_actor.GetProperty().SetColor(moccasin_rgb)
frustum_actor.GetProperty().SetRepresentationToWireframe()
frustum_actor.GetProperty().SetLineWidth(2)

# ---- Method 2: vtkPlanes from bounding-box bounds of the sphere ----
bounds_planes = vtkPlanes()
bounds = [0.0] * 6
sphere_source.GetOutput().GetBounds(bounds)
bounds_planes.SetBounds(bounds)

# Filter: generate a convex hull from the bounding-box planes
bounds_hull = vtkHull()
bounds_hull.SetPlanes(bounds_planes)
bounds_pd = vtkPolyData()
bounds_hull.GenerateHull(bounds_pd, -10, 10, -10, 10, -10, 10)

# Mapper / Actor: bounds hull (light coral wireframe)
bounds_mapper = vtkPolyDataMapper()
bounds_mapper.SetInputData(bounds_pd)

bounds_actor = vtkActor()
bounds_actor.SetMapper(bounds_mapper)
bounds_actor.GetProperty().SetColor(light_coral_rgb)
bounds_actor.GetProperty().SetRepresentationToWireframe()
bounds_actor.GetProperty().SetLineWidth(2)

# Renderer: assemble the scene — sphere inside frustum, bounding box around sphere
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(frustum_actor)
renderer.AddActor(bounds_actor)
renderer.SetBackground(dark_slate_gray_background_rgb)
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(30)
renderer.GetActiveCamera().Elevation(20)
renderer.GetActiveCamera().Zoom(1.3)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Planes")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
