#!/usr/bin/env python

# Test vtkPolarAxesActor with no input data (standalone polar axes).

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingAnnotation import vtkPolarAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkLight,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.8, 0.8, 0.8)

# Polar axes (no data)
polar_axes = vtkPolarAxesActor()
polar_axes.SetPole(0.5, 1.0, 3.0)
polar_axes.SetMaximumRadius(3.0)
polar_axes.SetMinimumAngle(-60.0)
polar_axes.SetMaximumAngle(210.0)
polar_axes.SetRequestedNumberOfRadialAxes(10)
polar_axes.SetPolarLabelFormat("{:6.1f}")
polar_axes.GetLastRadialAxisProperty().SetColor(0.0, 1.0, 0.0)
polar_axes.GetSecondaryRadialAxesProperty().SetColor(0.0, 0.0, 1.0)
polar_axes.GetPolarArcsProperty().SetColor(1.0, 0.0, 0.0)
polar_axes.GetSecondaryPolarArcsProperty().SetColor(1.0, 0.0, 1.0)
polar_axes.GetPolarAxisProperty().SetColor(1.0, 0.5, 0.0)
polar_axes.GetPolarAxisTitleTextProperty().SetColor(0.0, 0.0, 0.0)
polar_axes.GetPolarAxisLabelTextProperty().SetColor(1.0, 1.0, 0.0)
polar_axes.GetLastRadialAxisTextProperty().SetColor(0.0, 0.5, 0.0)
polar_axes.GetSecondaryRadialAxesTextProperty().SetColor(0.0, 1.0, 1.0)
polar_axes.SetScreenSize(9.0)

renderer.AddViewProp(polar_axes)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polar axes no data")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(7.0, 7.0, 4.0)
renderer.AddLight(light)

renderer.GetActiveCamera().SetClippingRange(1.0, 100.0)
renderer.GetActiveCamera().SetFocalPoint(0.0, 0.5, 0.0)
renderer.GetActiveCamera().SetPosition(5.0, 6.0, 14.0)
polar_axes.SetCamera(renderer.GetActiveCamera())

interactor.Initialize()
interactor.Start()
