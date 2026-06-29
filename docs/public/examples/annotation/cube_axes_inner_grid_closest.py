#!/usr/bin/env python

# Test vtkCubeAxesActor with inner gridlines on closest faces using oriented bounds.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkRenderingAnnotation import vtkCubeAxesActor
from vtkmodules.vtkRenderingCore import (
    vtkLight,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Oriented basis vectors (normalized)
base_x = [0.7071067811865475, 0.7071067811865475, 0.0]
base_y = [0.0, 0.7071067811865475, 0.7071067811865475]
base_z = [0.7071067811865475, 0.0, 0.7071067811865475]

# Cube axes actor
axes = vtkCubeAxesActor()
axes.SetUseOrientedBounds(True)
axes.SetOrientedBounds(-1, 1, -0.5, 0.5, 0, 4)
axes.SetAxisBaseForX(base_x)
axes.SetAxisBaseForY(base_y)
axes.SetAxisBaseForZ(base_z)
axes.SetXLabelFormat("{:6.1f}")
axes.SetYLabelFormat("{:6.1f}")
axes.SetZLabelFormat("{:6.1f}")
axes.SetScreenSize(15.0)
axes.SetFlyModeToClosestTriad()
axes.SetDrawXGridlines(True)
axes.SetDrawYGridlines(True)
axes.SetDrawZGridlines(True)
axes.SetGridLineLocation(vtkCubeAxesActor.VTK_GRID_LINES_CLOSEST)
axes.SetCornerOffset(0.0)

# Red for X axis
axes.GetXAxesLinesProperty().SetColor(1.0, 0.0, 0.0)
axes.GetTitleTextProperty(0).SetColor(1.0, 0.0, 0.0)
axes.GetLabelTextProperty(0).SetColor(0.8, 0.0, 0.0)

# Green for Y axis
axes.GetYAxesLinesProperty().SetColor(0.0, 1.0, 0.0)
axes.GetTitleTextProperty(1).SetColor(0.0, 1.0, 0.0)
axes.GetLabelTextProperty(1).SetColor(0.0, 0.8, 0.0)

renderer.AddViewProp(axes)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cube axes inner grid closest")
render_window.SetMultiSamples(0)
render_window.SetSize(600, 600)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
light = vtkLight()
light.SetFocalPoint(0.21406, 1.5, 0.0)
light.SetPosition(8.3761, 4.94858, 4.12505)
renderer.AddLight(light)

renderer.GetActiveCamera().SetClippingRange(1.0, 100.0)
renderer.GetActiveCamera().SetFocalPoint(1.26612, -0.81045, 1.24353)
renderer.GetActiveCamera().SetPosition(-5.66214, -2.58773, 11.243)
axes.SetCamera(renderer.GetActiveCamera())

interactor.Initialize()
interactor.Start()
