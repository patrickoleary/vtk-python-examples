#!/usr/bin/env python

# Demonstrate the effect of specular power on a row of eight spheres.
# Top row: specular=1.0, power doubles from 5 to 640.
# Bottom row: specular=0.5, power doubles from 5 to 640.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
sphere_color = (1.0, 0.0, 0.0)
specular_color = (1.0, 1.0, 1.0)
background = (0.102, 0.200, 0.400)

# Source: generate a high-resolution sphere shared by all actors
sphere = vtkSphereSource()
sphere.SetThetaResolution(100)
sphere.SetPhiResolution(50)

# Mapper: map sphere polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sphere.GetOutputPort())

# Actors: create eight spheres with increasing specular power
actors = []
specular = 1.0
sp_base = 5.0
sp_scale = 1.0
position = [0.0, 0.0, 0.0]
for i in range(8):
    specular_power = sp_base * sp_scale
    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetColor(sphere_color)
    actor.GetProperty().SetAmbient(0.3)
    actor.GetProperty().SetDiffuse(0.5)
    actor.GetProperty().SetSpecular(specular)
    actor.GetProperty().SetSpecularPower(specular_power)
    actor.GetProperty().SetSpecularColor(specular_color)
    actor.AddPosition(position)
    actors.append(actor)
    sp_scale *= 2.0
    position[0] += 1.25
    if i == 3:
        specular = 0.5
        sp_scale = 1.0
        position[0] = 0.0
        position[1] = 1.25

# Light: single directional light for uniform comparison
light = vtkLight()
light.SetFocalPoint(1.875, 0.6125, 0)
light.SetPosition(0.875, 1.6125, 1)

# Renderer: assemble the scene with parallel projection
renderer = vtkRenderer()
for actor in actors:
    renderer.AddActor(actor)
renderer.AddLight(light)
renderer.SetBackground(background)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()
renderer.GetActiveCamera().SetParallelScale(2.0)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("SpecularSpheres")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
