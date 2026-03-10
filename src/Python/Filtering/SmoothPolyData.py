#!/usr/bin/env python

# Generate a noisy sphere by perturbing point positions, then smooth
# it with vtkSmoothPolyDataFilter and display both side by side.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkMinimalStandardRandomSequence
from vtkmodules.vtkFiltersCore import vtkSmoothPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
coral_rgb = (1.0, 0.498, 0.314)
light_green_rgb = (0.565, 0.933, 0.565)
background_rgb = (0.2, 0.2, 0.2)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetThetaResolution(30)
sphere_source.SetPhiResolution(30)
sphere_source.Update()

# Perturb: add random noise to the sphere points
noisy_sphere = sphere_source.GetOutput()
points = noisy_sphere.GetPoints()
random_seq = vtkMinimalStandardRandomSequence()
random_seq.Initialize(42)
for i in range(points.GetNumberOfPoints()):
    p = list(points.GetPoint(i))
    for j in range(3):
        p[j] += 0.1 * (random_seq.GetValue() - 0.5)
        random_seq.Next()
    points.SetPoint(i, p)
noisy_sphere.Modified()

# Mapper: map the noisy sphere
noisy_mapper = vtkPolyDataMapper()
noisy_mapper.SetInputData(noisy_sphere)

# Actor: assign the noisy sphere (coral), offset left
noisy_actor = vtkActor()
noisy_actor.SetMapper(noisy_mapper)
noisy_actor.GetProperty().SetColor(coral_rgb)
noisy_actor.GetProperty().EdgeVisibilityOn()
noisy_actor.SetPosition(-1.2, 0, 0)

# Filter: smooth the noisy sphere with 50 Laplacian iterations
smooth = vtkSmoothPolyDataFilter()
smooth.SetInputData(noisy_sphere)
smooth.SetNumberOfIterations(50)
smooth.SetRelaxationFactor(0.1)
smooth.FeatureEdgeSmoothingOff()
smooth.BoundarySmoothingOn()

# Mapper: map the smoothed sphere
smooth_mapper = vtkPolyDataMapper()
smooth_mapper.SetInputConnection(smooth.GetOutputPort())

# Actor: assign the smoothed sphere (light green), offset right
smooth_actor = vtkActor()
smooth_actor.SetMapper(smooth_mapper)
smooth_actor.GetProperty().SetColor(light_green_rgb)
smooth_actor.GetProperty().EdgeVisibilityOn()
smooth_actor.SetPosition(1.2, 0, 0)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(noisy_actor)
renderer.AddActor(smooth_actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SmoothPolyData")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
