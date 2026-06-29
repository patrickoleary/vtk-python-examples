#!/usr/bin/env python

# Demonstrate screen-facing 3D text using vtkBillboardTextActor3D,
# labeling three spheres at different positions in the scene.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkBillboardTextActor3D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
steel_blue_rgb = (0.275, 0.510, 0.706)
gold_rgb = (1.0, 0.843, 0.0)
background_rgb = (0.200, 0.302, 0.400)

# Source: generate sphere A
sphere_a_source = vtkSphereSource()
sphere_a_source.SetCenter(-2.0, 0.0, 0.0)
sphere_a_source.SetRadius(0.5)
sphere_a_source.SetThetaResolution(20)
sphere_a_source.SetPhiResolution(20)

sphere_a_mapper = vtkPolyDataMapper()
sphere_a_mapper.SetInputConnection(sphere_a_source.GetOutputPort())

sphere_a_actor = vtkActor()
sphere_a_actor.SetMapper(sphere_a_mapper)
sphere_a_actor.GetProperty().SetColor(tomato_rgb)

billboard_a = vtkBillboardTextActor3D()
billboard_a.SetInput("Sphere A")
billboard_a.SetPosition(-2.0, 0.8, 0.0)
billboard_a.GetTextProperty().SetFontSize(24)
billboard_a.GetTextProperty().SetColor(tomato_rgb)
billboard_a.GetTextProperty().SetJustificationToCentered()
billboard_a.GetTextProperty().BoldOn()

# Source: generate sphere B
sphere_b_source = vtkSphereSource()
sphere_b_source.SetCenter(0.0, 0.0, 0.0)
sphere_b_source.SetRadius(0.5)
sphere_b_source.SetThetaResolution(20)
sphere_b_source.SetPhiResolution(20)

sphere_b_mapper = vtkPolyDataMapper()
sphere_b_mapper.SetInputConnection(sphere_b_source.GetOutputPort())

sphere_b_actor = vtkActor()
sphere_b_actor.SetMapper(sphere_b_mapper)
sphere_b_actor.GetProperty().SetColor(steel_blue_rgb)

billboard_b = vtkBillboardTextActor3D()
billboard_b.SetInput("Sphere B")
billboard_b.SetPosition(0.0, 0.8, 0.0)
billboard_b.GetTextProperty().SetFontSize(24)
billboard_b.GetTextProperty().SetColor(steel_blue_rgb)
billboard_b.GetTextProperty().SetJustificationToCentered()
billboard_b.GetTextProperty().BoldOn()

# Source: generate sphere C
sphere_c_source = vtkSphereSource()
sphere_c_source.SetCenter(2.0, 0.0, 0.0)
sphere_c_source.SetRadius(0.5)
sphere_c_source.SetThetaResolution(20)
sphere_c_source.SetPhiResolution(20)

sphere_c_mapper = vtkPolyDataMapper()
sphere_c_mapper.SetInputConnection(sphere_c_source.GetOutputPort())

sphere_c_actor = vtkActor()
sphere_c_actor.SetMapper(sphere_c_mapper)
sphere_c_actor.GetProperty().SetColor(gold_rgb)

billboard_c = vtkBillboardTextActor3D()
billboard_c.SetInput("Sphere C")
billboard_c.SetPosition(2.0, 0.8, 0.0)
billboard_c.GetTextProperty().SetFontSize(24)
billboard_c.GetTextProperty().SetColor(gold_rgb)
billboard_c.GetTextProperty().SetJustificationToCentered()
billboard_c.GetTextProperty().BoldOn()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(sphere_a_actor)
renderer.AddActor(billboard_a)
renderer.AddActor(sphere_b_actor)
renderer.AddActor(billboard_b)
renderer.AddActor(sphere_c_actor)
renderer.AddActor(billboard_c)
renderer.SetBackground(background_rgb)

# Render window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("billboard text actor3d spheres")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Scene: configure the camera
renderer.ResetCamera()

# Start: launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
