#!/usr/bin/env python

# Demonstrate how to set up and position a vtkCamera explicitly.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
light_sky_blue = (0.529, 0.808, 0.980)
misty_rose = (1.000, 0.894, 0.882)

# Source: generate sphere polygon data
source = vtkSphereSource()
source.SetCenter(0.0, 0.0, 0.0)
source.SetRadius(10.0)
source.SetPhiResolution(30)
source.SetThetaResolution(30)

# Mapper: map polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

# Actor: assign the mapped geometry with specular highlights
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetSpecular(0.6)
actor.GetProperty().SetSpecularPower(30)
actor.GetProperty().SetColor(light_sky_blue)

# Camera: position the viewpoint explicitly
camera = vtkCamera()
camera.SetPosition(0, 0, 100)
camera.SetFocalPoint(0, 0, 0)

# Renderer: assemble the scene and configure the camera
renderer = vtkRenderer()
renderer.SetActiveCamera(camera)
renderer.AddActor(actor)
renderer.SetBackground(misty_rose)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Camera")
render_window.SetSize(640, 480)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Start()
