#!/usr/bin/env python

# Demonstrate depth peeling with two renderers using different viewports and layers.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere source
sphere = vtkSphereSource()
sphere.SetRadius(10)

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Main renderer (full viewport, layer 0)
renderer_0 = vtkRenderer()
renderer_0.LightFollowCameraOn()
renderer_0.TwoSidedLightingOn()
renderer_0.SetUseDepthPeeling(1)
renderer_0.SetMaximumNumberOfPeels(8)
renderer_0.SetOcclusionRatio(0.0)
renderer_0.SetLayer(0)

# Translucent sphere in main renderer
actor_0 = vtkActor()
actor_0.SetMapper(mapper)
actor_0.GetProperty().SetOpacity(0.35)
actor_0.SetPosition(0.0, 0.0, 1.0)
renderer_0.AddActor(actor_0)

# Inset renderer (small viewport, layer 1)
renderer_1 = vtkRenderer()
renderer_1.LightFollowCameraOn()
renderer_1.TwoSidedLightingOn()
renderer_1.SetUseDepthPeeling(1)
renderer_1.SetMaximumNumberOfPeels(8)
renderer_1.SetOcclusionRatio(0.0)
renderer_1.SetViewport(0.0, 0.1, 0.2, 0.3)
renderer_1.InteractiveOff()
renderer_1.SetLayer(1)

# Opaque warm-toned sphere in inset
actor_1 = vtkActor()
actor_1.SetMapper(mapper)
actor_1.GetProperty().SetAmbientColor(1.0, 0.0, 0.0)
actor_1.GetProperty().SetDiffuseColor(1.0, 0.8, 0.3)
actor_1.GetProperty().SetSpecular(0.0)
actor_1.GetProperty().SetDiffuse(0.5)
actor_1.GetProperty().SetAmbient(0.3)
renderer_1.AddActor(actor_1)

# Translucent sphere offset in inset
actor_2 = vtkActor()
actor_2.SetMapper(mapper)
actor_2.GetProperty().SetOpacity(0.35)
actor_2.SetPosition(10.0, 0.0, 0.0)
renderer_1.AddActor(actor_2)

# Render window with two layers
render_window = vtkRenderWindow()
render_window.SetAlphaBitPlanes(1)
render_window.SetMultiSamples(0)
render_window.SetNumberOfLayers(2)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.SetWindowName("depth peeling pass viewport")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer_0.ResetCamera()
renderer_1.ResetCamera()

interactor.Initialize()
interactor.Start()
