#!/usr/bin/env python

# Demonstrate depth-of-field camera blur by placing two mace objects at
# different depths and setting a non-zero focal disk on the camera.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
background = (0.102, 0.200, 0.400)

# Source: low-resolution sphere (the ball)
sphere = vtkSphereSource()
sphere.SetPhiResolution(7)
sphere.SetThetaResolution(7)

# Mapper: map the sphere polygon data
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

# Source: cone (the spike template)
cone = vtkConeSource()
cone.SetResolution(5)

# Filter: glyph cones onto each sphere vertex
glyph = vtkGlyph3D()
glyph.SetInputConnection(sphere.GetOutputPort())
glyph.SetSourceConnection(cone.GetOutputPort())
glyph.SetVectorModeToUseNormal()
glyph.SetScaleModeToScaleByVector()
glyph.SetScaleFactor(0.25)

# Mapper: map the glyphed spike data
spike_mapper = vtkPolyDataMapper()
spike_mapper.SetInputConnection(glyph.GetOutputPort())

# Actor: foreground mace (near)
sphere_actor_near = vtkActor()
sphere_actor_near.SetMapper(sphere_mapper)
sphere_actor_near.SetPosition(0, 0.7, 0)

spike_actor_near = vtkActor()
spike_actor_near.SetMapper(spike_mapper)
spike_actor_near.SetPosition(0, 0.7, 0)

# Actor: background mace (far)
sphere_actor_far = vtkActor()
sphere_actor_far.SetMapper(sphere_mapper)
sphere_actor_far.SetPosition(0, -1.0, -10)
sphere_actor_far.SetScale(1.5, 1.5, 1.5)

spike_actor_far = vtkActor()
spike_actor_far.SetMapper(spike_mapper)
spike_actor_far.SetPosition(0, -1.0, -10)
spike_actor_far.SetScale(1.5, 1.5, 1.5)

# Renderer: assemble the scene and configure depth-of-field
renderer = vtkRenderer()
renderer.AddActor(sphere_actor_near)
renderer.AddActor(spike_actor_near)
renderer.AddActor(sphere_actor_far)
renderer.AddActor(spike_actor_far)
renderer.SetBackground(background)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("CameraBlur")

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Camera: zoom in and enable focal-disk blur
render_window.Render()
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().Zoom(1.8)
renderer.GetActiveCamera().SetFocalDisk(0.05)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
