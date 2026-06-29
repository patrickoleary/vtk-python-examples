#!/usr/bin/env python

# Demonstrate Sobel gradient magnitude edge detection render pass on a cone.

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
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkLightsPass,
    vtkOpaquePass,
    vtkOverlayPass,
    vtkRenderPassCollection,
    vtkSequencePass,
    vtkSobelGradientMagnitudePass,
    vtkTranslucentPass,
    vtkVolumetricPass,
)

# Render pass pipeline
camera_pass = vtkCameraPass()
seq = vtkSequencePass()
lights = vtkLightsPass()
opaque = vtkOpaquePass()
translucent = vtkTranslucentPass()
volume = vtkVolumetricPass()
overlay = vtkOverlayPass()

passes = vtkRenderPassCollection()
passes.AddItem(lights)
passes.AddItem(opaque)
passes.AddItem(translucent)
passes.AddItem(volume)
passes.AddItem(overlay)
seq.SetPasses(passes)
camera_pass.SetDelegatePass(seq)

sobel_pass = vtkSobelGradientMagnitudePass()
sobel_pass.SetDelegatePass(camera_pass)

# Cone actor
cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())

cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.3, 0.0)
renderer.SetPass(sobel_pass)
renderer.AddActor(cone_actor)

render_window = vtkRenderWindow()
render_window.SetSize(400, 400)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("sobel gradient magnitude pass")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
# Pipeline exception: render needed before camera adjustments
render_window.Render()
renderer.GetActiveCamera().Azimuth(-40.0)
renderer.GetActiveCamera().Elevation(20.0)

interactor.Initialize()
interactor.Start()
