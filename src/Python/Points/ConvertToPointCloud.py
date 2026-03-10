#!/usr/bin/env python

# Convert polydata vertices to a point cloud using vtkConvertToPointCloud.
# The left viewport shows the original sphere mesh and the right shows
# the resulting point cloud.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersPoints import vtkConvertToPointCloud
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
slate_gray_background_rgb = (0.439, 0.502, 0.565)

# Source: create a sphere
sphere = vtkSphereSource()
sphere.SetRadius(1.0)
sphere.SetPhiResolution(30)
sphere.SetThetaResolution(30)

# ---- Left viewport: original mesh ----
mesh_mapper = vtkPolyDataMapper()
mesh_mapper.SetInputConnection(sphere.GetOutputPort())

mesh_actor = vtkActor()
mesh_actor.SetMapper(mesh_mapper)
mesh_actor.GetProperty().SetColor(tomato_rgb)
mesh_actor.GetProperty().EdgeVisibilityOn()
mesh_actor.GetProperty().SetEdgeColor(0.2, 0.2, 0.2)

left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.AddActor(mesh_actor)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.ResetCamera()

# ---- Right viewport: point cloud ----
to_cloud = vtkConvertToPointCloud()
to_cloud.SetInputConnection(sphere.GetOutputPort())

cloud_mapper = vtkPolyDataMapper()
cloud_mapper.SetInputConnection(to_cloud.GetOutputPort())

cloud_actor = vtkActor()
cloud_actor.SetMapper(cloud_mapper)
cloud_actor.GetProperty().SetColor(tomato_rgb)
cloud_actor.GetProperty().SetPointSize(4)

right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.AddActor(cloud_actor)
right_renderer.SetBackground(slate_gray_background_rgb)
right_renderer.SetActiveCamera(left_renderer.GetActiveCamera())

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(800, 400)
render_window.SetWindowName("ConvertToPointCloud")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
