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

# Actor 0: specular 1.0, power 5
actor_0 = vtkActor()
actor_0.SetMapper(mapper)
actor_0.GetProperty().SetColor(sphere_color)
actor_0.GetProperty().SetAmbient(0.3)
actor_0.GetProperty().SetDiffuse(0.5)
actor_0.GetProperty().SetSpecular(1.0)
actor_0.GetProperty().SetSpecularPower(5.0)
actor_0.GetProperty().SetSpecularColor(specular_color)
actor_0.AddPosition(0.0, 0.0, 0.0)

# Actor 1: specular 1.0, power 10
actor_1 = vtkActor()
actor_1.SetMapper(mapper)
actor_1.GetProperty().SetColor(sphere_color)
actor_1.GetProperty().SetAmbient(0.3)
actor_1.GetProperty().SetDiffuse(0.5)
actor_1.GetProperty().SetSpecular(1.0)
actor_1.GetProperty().SetSpecularPower(10.0)
actor_1.GetProperty().SetSpecularColor(specular_color)
actor_1.AddPosition(1.25, 0.0, 0.0)

# Actor 2: specular 1.0, power 20
actor_2 = vtkActor()
actor_2.SetMapper(mapper)
actor_2.GetProperty().SetColor(sphere_color)
actor_2.GetProperty().SetAmbient(0.3)
actor_2.GetProperty().SetDiffuse(0.5)
actor_2.GetProperty().SetSpecular(1.0)
actor_2.GetProperty().SetSpecularPower(20.0)
actor_2.GetProperty().SetSpecularColor(specular_color)
actor_2.AddPosition(2.50, 0.0, 0.0)

# Actor 3: specular 1.0, power 40
actor_3 = vtkActor()
actor_3.SetMapper(mapper)
actor_3.GetProperty().SetColor(sphere_color)
actor_3.GetProperty().SetAmbient(0.3)
actor_3.GetProperty().SetDiffuse(0.5)
actor_3.GetProperty().SetSpecular(1.0)
actor_3.GetProperty().SetSpecularPower(40.0)
actor_3.GetProperty().SetSpecularColor(specular_color)
actor_3.AddPosition(3.75, 0.0, 0.0)

# Actor 4: specular 0.5, power 5
actor_4 = vtkActor()
actor_4.SetMapper(mapper)
actor_4.GetProperty().SetColor(sphere_color)
actor_4.GetProperty().SetAmbient(0.3)
actor_4.GetProperty().SetDiffuse(0.5)
actor_4.GetProperty().SetSpecular(0.5)
actor_4.GetProperty().SetSpecularPower(5.0)
actor_4.GetProperty().SetSpecularColor(specular_color)
actor_4.AddPosition(0.0, 1.25, 0.0)

# Actor 5: specular 0.5, power 10
actor_5 = vtkActor()
actor_5.SetMapper(mapper)
actor_5.GetProperty().SetColor(sphere_color)
actor_5.GetProperty().SetAmbient(0.3)
actor_5.GetProperty().SetDiffuse(0.5)
actor_5.GetProperty().SetSpecular(0.5)
actor_5.GetProperty().SetSpecularPower(10.0)
actor_5.GetProperty().SetSpecularColor(specular_color)
actor_5.AddPosition(1.25, 1.25, 0.0)

# Actor 6: specular 0.5, power 20
actor_6 = vtkActor()
actor_6.SetMapper(mapper)
actor_6.GetProperty().SetColor(sphere_color)
actor_6.GetProperty().SetAmbient(0.3)
actor_6.GetProperty().SetDiffuse(0.5)
actor_6.GetProperty().SetSpecular(0.5)
actor_6.GetProperty().SetSpecularPower(20.0)
actor_6.GetProperty().SetSpecularColor(specular_color)
actor_6.AddPosition(2.50, 1.25, 0.0)

# Actor 7: specular 0.5, power 40
actor_7 = vtkActor()
actor_7.SetMapper(mapper)
actor_7.GetProperty().SetColor(sphere_color)
actor_7.GetProperty().SetAmbient(0.3)
actor_7.GetProperty().SetDiffuse(0.5)
actor_7.GetProperty().SetSpecular(0.5)
actor_7.GetProperty().SetSpecularPower(40.0)
actor_7.GetProperty().SetSpecularColor(specular_color)
actor_7.AddPosition(3.75, 1.25, 0.0)

# Light: single directional light for uniform comparison
light = vtkLight()
light.SetFocalPoint(1.875, 0.6125, 0)
light.SetPosition(0.875, 1.6125, 1)

# Renderer: assemble the scene with parallel projection
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddActor(actor_2)
renderer.AddActor(actor_3)
renderer.AddActor(actor_4)
renderer.AddActor(actor_5)
renderer.AddActor(actor_6)
renderer.AddActor(actor_7)
renderer.AddLight(light)
renderer.SetBackground(background)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("specular spheres")
render_window.SetMultiSamples(0)
render_window.SetSize(640, 480)

# Scene: configure the camera
renderer.GetActiveCamera().SetFocalPoint(0, 0, 0)
renderer.GetActiveCamera().SetPosition(0, 0, 1)
renderer.GetActiveCamera().SetViewUp(0, 1, 0)
renderer.GetActiveCamera().ParallelProjectionOn()
renderer.ResetCamera()
renderer.GetActiveCamera().SetParallelScale(2.0)

# Interactor: handle mouse and keyboard events
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
interactor.Start()
