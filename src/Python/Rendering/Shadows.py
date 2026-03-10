#!/usr/bin/env python

# Render a sphere on a ground plane with shadow mapping using two lights
# (a warm overhead sun and a cool tungsten fill).

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingOpenGL2 import (
    vtkCameraPass,
    vtkRenderPassCollection,
    vtkSequencePass,
    vtkShadowMapPass,
)

# Colors (normalized RGB)
saddle_brown = (0.545, 0.271, 0.075)
sienna = (0.627, 0.322, 0.176)
white = (1.0, 1.0, 1.0)
silver = (0.753, 0.753, 0.753)
high_noon_sun = (1.0, 1.0, 0.984)
tungsten_100w = (1.0, 0.839, 0.667)

# Source: generate a high-resolution sphere
sphere = vtkSphereSource()
sphere.SetThetaResolution(100)
sphere.SetPhiResolution(100)
sphere.Update()

# Mapper: map sphere polygon data
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

# Actor: the main sphere with rich material properties
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetAmbientColor(saddle_brown)
sphere_actor.GetProperty().SetDiffuseColor(sienna)
sphere_actor.GetProperty().SetSpecularColor(white)
sphere_actor.GetProperty().SetSpecular(0.51)
sphere_actor.GetProperty().SetDiffuse(0.7)
sphere_actor.GetProperty().SetAmbient(0.7)
sphere_actor.GetProperty().SetSpecularPower(30.0)

# Source: ground plane sized to the sphere bounds
bounds = sphere.GetOutput().GetBounds()
extent_x = bounds[1] - bounds[0]
extent_z = bounds[5] - bounds[4]
thickness = extent_z * 0.1

ground = vtkCubeSource()
ground.SetCenter(
    (bounds[1] + bounds[0]) / 2.0,
    bounds[2] - thickness / 2.0,
    (bounds[5] + bounds[4]) / 2.0,
)
ground.SetXLength(extent_x * 2.0)
ground.SetYLength(thickness)
ground.SetZLength(extent_z * 2.0)

# Mapper: map ground plane data
ground_mapper = vtkPolyDataMapper()
ground_mapper.SetInputConnection(ground.GetOutputPort())

# Actor: the ground plane
ground_actor = vtkActor()
ground_actor.SetMapper(ground_mapper)

# Light: overhead sun (5400 K)
light_sun = vtkLight()
light_sun.SetFocalPoint(0, 0, 0)
light_sun.SetPosition(0, 1, 0.2)
light_sun.SetColor(high_noon_sun)
light_sun.SetIntensity(0.3)

# Light: tungsten fill (2850 K)
light_fill = vtkLight()
light_fill.SetFocalPoint(0, 0, 0)
light_fill.SetPosition(1.0, 1.0, 1.0)
light_fill.SetColor(tungsten_100w)
light_fill.SetIntensity(0.8)

# Render pass: shadow map pipeline
shadows = vtkShadowMapPass()
passes = vtkRenderPassCollection()
passes.AddItem(shadows.GetShadowMapBakerPass())
passes.AddItem(shadows)
seq = vtkSequencePass()
seq.SetPasses(passes)
camera_pass = vtkCameraPass()
camera_pass.SetDelegatePass(seq)

# Renderer: assemble the scene with shadow mapping
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(ground_actor)
renderer.AddLight(light_sun)
renderer.AddLight(light_fill)
renderer.SetBackground(silver)
renderer.SetPass(camera_pass)
renderer.GetActiveCamera().SetPosition(-0.2, 0.2, 1)
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.ResetCamera()
renderer.GetActiveCamera().Dolly(2.25)
renderer.ResetCameraClippingRange()

# Window: display the rendered scene (disable multisampling for render passes)
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetMultiSamples(0)
render_window.SetWindowName("Shadows")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
