#!/usr/bin/env python

# Decimate a sphere using vtkQuadricDecimation, which uses quadric
# error metrics to optimally place the remaining vertices. Side-by-side
# viewports show the original mesh (left) and the decimated mesh (right).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkQuadricDecimation
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

# Source: generate a high-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(40)
sphere.SetPhiResolution(40)

# QuadricDecimation: reduce by 80% using quadric error metrics
decimator = vtkQuadricDecimation()
decimator.SetInputConnection(sphere.GetOutputPort())
decimator.SetTargetReduction(0.8)

# Mapper: original sphere
original_mapper = vtkPolyDataMapper()
original_mapper.SetInputConnection(sphere.GetOutputPort())
original_mapper.ScalarVisibilityOff()

original_actor = vtkActor()
original_actor.SetMapper(original_mapper)
original_actor.GetProperty().SetColor(peach_puff_rgb)
original_actor.GetProperty().SetInterpolationToFlat()

# Mapper: decimated sphere
decimated_mapper = vtkPolyDataMapper()
decimated_mapper.SetInputConnection(decimator.GetOutputPort())
decimated_mapper.ScalarVisibilityOff()

decimated_actor = vtkActor()
decimated_actor.SetMapper(decimated_mapper)
decimated_actor.GetProperty().SetColor(peach_puff_rgb)
decimated_actor.GetProperty().SetInterpolationToFlat()

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, -1, 0)
camera.SetFocalPoint(0, 0, 0)
camera.SetViewUp(0, 0, 1)
camera.Elevation(30)
camera.Azimuth(30)

# Left renderer: original mesh
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(original_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: decimated mesh
right_renderer = vtkRenderer()
right_renderer.SetViewport(0.5, 0.0, 1.0, 1.0)
right_renderer.SetBackground(cornflower_blue_background_rgb)
right_renderer.AddActor(decimated_actor)
right_renderer.SetActiveCamera(camera)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(left_renderer)
render_window.AddRenderer(right_renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("QuadricDecimation")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
