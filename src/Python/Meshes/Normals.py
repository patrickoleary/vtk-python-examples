#!/usr/bin/env python

# Compute and visualize surface normals on a sphere using
# vtkPolyDataNormals. Side-by-side viewports show the sphere without
# normals / flat shading (left) and with computed normals / smooth
# shading (right).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkPolyDataNormals
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
slate_gray_background_rgb = (0.439, 0.502, 0.565)
cornflower_blue_background_rgb = (0.392, 0.584, 0.929)
peach_puff_rgb = (1.000, 0.855, 0.725)

# Source: generate a low-resolution sphere (faceted appearance)
sphere = vtkSphereSource()
sphere.SetThetaResolution(12)
sphere.SetPhiResolution(12)

# PolyDataNormals: compute point normals for smooth shading
normals = vtkPolyDataNormals()
normals.SetInputConnection(sphere.GetOutputPort())
normals.SetFeatureAngle(60.0)
normals.ComputePointNormalsOn()
normals.SplittingOff()

# Mapper: flat-shaded sphere (no normals computed)
flat_mapper = vtkPolyDataMapper()
flat_mapper.SetInputConnection(sphere.GetOutputPort())
flat_mapper.ScalarVisibilityOff()

flat_actor = vtkActor()
flat_actor.SetMapper(flat_mapper)
flat_actor.GetProperty().SetColor(peach_puff_rgb)
flat_actor.GetProperty().SetInterpolationToFlat()

# Mapper: smooth-shaded sphere (with computed normals)
smooth_mapper = vtkPolyDataMapper()
smooth_mapper.SetInputConnection(normals.GetOutputPort())
smooth_mapper.ScalarVisibilityOff()

smooth_actor = vtkActor()
smooth_actor.SetMapper(smooth_mapper)
smooth_actor.GetProperty().SetColor(peach_puff_rgb)
smooth_actor.GetProperty().SetInterpolationToPhong()

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, 0, 3)
camera.SetFocalPoint(0, 0, 0)

# Left renderer: flat shading
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(flat_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: smooth shading with normals
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(smooth_actor)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Normals")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
