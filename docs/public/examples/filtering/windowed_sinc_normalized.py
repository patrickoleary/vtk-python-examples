#!/usr/bin/env python

# Smooth a noisy sphere offset from the origin using
# vtkWindowedSincPolyDataFilter with NormalizeCoordinates enabled,
# displayed in two viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkFiltersCore import vtkWindowedSincPolyDataFilter
from vtkmodules.vtkFiltersGeneral import (
    vtkBrownianPoints,
    vtkWarpVector,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 100
colors = vtkNamedColors()
rgb = [0.0, 0.0, 0.0]
colors.GetColorRGB("tomato", rgb)

# Source: sphere offset from origin with large radius
sphere = vtkSphereSource()
sphere.SetCenter(100, 200, 400)
sphere.SetRadius(100)
sphere.SetThetaResolution(resolution)
sphere.SetPhiResolution(int(resolution / 2))

# Add noise via Brownian motion vectors
brownian = vtkBrownianPoints()
brownian.SetInputConnection(sphere.GetOutputPort())
brownian.SetMinimumSpeed(0.0)
brownian.SetMaximumSpeed(1)

# Warp sphere with noise
warp = vtkWarpVector()
warp.SetInputConnection(brownian.GetOutputPort())
warp.SetScaleFactor(1.0)

# Smooth with windowed sinc filter and coordinate normalization
smooth = vtkWindowedSincPolyDataFilter()
smooth.SetInputConnection(warp.GetOutputPort())
smooth.SetNumberOfIterations(20)
smooth.FeatureEdgeSmoothingOff()
smooth.BoundarySmoothingOff()
smooth.NonManifoldSmoothingOff()
smooth.SetPassBand(0.1)
smooth.GenerateErrorScalarsOn()
smooth.GenerateErrorVectorsOn()
smooth.NormalizeCoordinatesOn()
smooth.SetWindowFunctionToHamming()
smooth.Update()

# Original noisy sphere
mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(warp.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)
actor_0.GetProperty().SetDiffuseColor(rgb)
actor_0.GetProperty().SetDiffuse(0.8)
actor_0.GetProperty().SetSpecular(0.4)
actor_0.GetProperty().SetSpecularPower(30)

# Smoothed sphere
mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(smooth.GetOutputPort())
mapper_1.SetScalarRange(smooth.GetOutput().GetScalarRange())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)
actor_1.GetProperty().SetDiffuseColor(rgb)
actor_1.GetProperty().SetDiffuse(0.8)
actor_1.GetProperty().SetSpecular(0.4)
actor_1.GetProperty().SetSpecularPower(30)

# Two viewports with shared camera
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.5, 1.0)
renderer_0.SetBackground(1, 1, 1)
renderer_0.AddActor(actor_0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0, 1.0, 1.0)
renderer_1.SetBackground(1, 1, 1)
renderer_1.AddActor(actor_1)
# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetSize(450, 300)
render_window.SetWindowName("windowed sinc normalized")

# Scene
renderer_1.SetActiveCamera(renderer_0.GetActiveCamera())
renderer_0.ResetCamera()
renderer_0.GetActiveCamera().Zoom(1.25)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
