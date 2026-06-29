#!/usr/bin/env python

# Demonstrate depth peeling with translucent spheres in front of an opaque cube.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Opaque box
box = vtkCubeSource()
box.SetXLength(3.0)
box.SetYLength(3.0)
box_mapper = vtkPolyDataMapper()
box_mapper.SetInputConnection(box.GetOutputPort())
box_actor = vtkActor()
box_actor.GetProperty().SetColor(0.1, 0.1, 0.1)
box_actor.SetMapper(box_mapper)

# Shared sphere source
sphere = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

# Translucent red sphere
sphere_actor_1 = vtkActor()
sphere_actor_1.GetProperty().SetColor(1.0, 0.0, 0.0)
sphere_actor_1.GetProperty().SetOpacity(0.2)
sphere_actor_1.SetPosition(0.0, 0.0, 1.0)
sphere_actor_1.SetMapper(sphere_mapper)

# Translucent green sphere
sphere_actor_2 = vtkActor()
sphere_actor_2.GetProperty().SetColor(0.0, 1.0, 0.0)
sphere_actor_2.GetProperty().SetOpacity(0.2)
sphere_actor_2.SetPosition(0.0, 0.0, 2.0)
sphere_actor_2.SetMapper(sphere_mapper)

# Renderer with depth peeling
renderer = vtkRenderer()
renderer.AddActor(box_actor)
renderer.AddActor(sphere_actor_1)
renderer.AddActor(sphere_actor_2)
renderer.SetUseDepthPeeling(1)
renderer.SetMaximumNumberOfPeels(20)
renderer.SetOcclusionRatio(0.0)
render_window = vtkRenderWindow()
render_window.SetSize(500, 500)
render_window.SetMultiSamples(0)
render_window.SetAlphaBitPlanes(1)
render_window.AddRenderer(renderer)
render_window.SetWindowName("depth peeling occlusion query")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
