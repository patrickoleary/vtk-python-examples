#!/usr/bin/env python

# Demonstrate outline glow render pass using a layered renderer on a cone.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkConeSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import vtkOutlineGlowPass, vtkRenderStepsPass

# Two renderers: main (layer 0) and outline (layer 1)
renderer = vtkRenderer()
renderer_outline = vtkRenderer()
renderer_outline.SetLayer(1)

# Outline glow pass on the overlay renderer
basic_passes = vtkRenderStepsPass()
glow_pass = vtkOutlineGlowPass()
glow_pass.SetDelegatePass(basic_passes)
renderer_outline.SetPass(glow_pass)

# Shared cone source
cone = vtkConeSource()

# Main cone actor
mapper_main = vtkPolyDataMapper()
mapper_main.SetInputConnection(cone.GetOutputPort())
actor_main = vtkActor()
actor_main.SetMapper(mapper_main)
renderer.AddActor(actor_main)

# Outline cone actor (solid color, no lighting)
mapper_outline = vtkPolyDataMapper()
mapper_outline.SetInputConnection(cone.GetOutputPort())
actor_outline = vtkActor()
actor_outline.SetMapper(mapper_outline)
actor_outline.GetProperty().SetColor(1.0, 0.0, 1.0)
actor_outline.GetProperty().LightingOff()
renderer_outline.AddActor(actor_outline)

# Render window with two layers
render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer_outline)
render_window.AddRenderer(renderer)
render_window.SetWindowName("outline glow pass opengl")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()
camera = renderer.GetActiveCamera()
camera.Azimuth(-40.0)
camera.Elevation(20.0)
renderer.ResetCamera()
renderer_outline.SetActiveCamera(camera)

interactor.Initialize()
interactor.Start()
