#!/usr/bin/env python

# Smooth a noisy sphere using vtkWindowedSincPolyDataFilter, which
# applies a windowed sinc function as a low-pass filter on the mesh
# geometry. Side-by-side viewports show before (left) and after (right).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersCore import vtkWindowedSincPolyDataFilter
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

# Source: generate a tessellated sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(30)
sphere.SetPhiResolution(30)
sphere.Update()

# Perturb each point with random noise
rng = vtkMinimalStandardRandomSequence()
rng.SetSeed(54321)
noisy_poly = sphere.GetOutput()
points = noisy_poly.GetPoints()
for i in range(points.GetNumberOfPoints()):
    p = list(points.GetPoint(i))
    for j in range(3):
        rng.Next()
        p[j] += rng.GetRangeValue(-0.05, 0.05)
    points.SetPoint(i, p)
noisy_poly.Modified()

# Windowed sinc smoothing: 20 iterations with a pass band of 0.1
smoother = vtkWindowedSincPolyDataFilter()
smoother.SetInputData(noisy_poly)
smoother.SetNumberOfIterations(20)
smoother.SetPassBand(0.1)
smoother.BoundarySmoothingOff()
smoother.NonManifoldSmoothingOn()
smoother.NormalizeCoordinatesOn()

# Mapper: noisy surface
noisy_mapper = vtkPolyDataMapper()
noisy_mapper.SetInputData(noisy_poly)
noisy_mapper.ScalarVisibilityOff()

noisy_actor = vtkActor()
noisy_actor.SetMapper(noisy_mapper)
noisy_actor.GetProperty().SetColor(peach_puff_rgb)

# Mapper: smoothed surface
smooth_mapper = vtkPolyDataMapper()
smooth_mapper.SetInputConnection(smoother.GetOutputPort())
smooth_mapper.ScalarVisibilityOff()

smooth_actor = vtkActor()
smooth_actor.SetMapper(smooth_mapper)
smooth_actor.GetProperty().SetColor(peach_puff_rgb)

# Shared camera
camera = vtkCamera()
camera.SetPosition(0, 0, 3)
camera.SetFocalPoint(0, 0, 0)

# Left renderer: noisy mesh
left_renderer = vtkRenderer()
left_renderer.SetViewport(0.0, 0.0, 0.5, 1.0)
left_renderer.SetBackground(slate_gray_background_rgb)
left_renderer.AddActor(noisy_actor)
left_renderer.SetActiveCamera(camera)
left_renderer.ResetCamera()

# Right renderer: smoothed mesh
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
render_window.SetWindowName("WindowedSincSmoothing")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
