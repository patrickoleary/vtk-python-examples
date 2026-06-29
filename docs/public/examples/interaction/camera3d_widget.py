#!/usr/bin/env python
# Demonstrate vtkCamera3DWidget with dual viewports for camera manipulation.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import vtkAppendPolyData
from vtkmodules.vtkFiltersSources import (
    vtkCubeSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkCamera3DRepresentation,
    vtkCamera3DWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create geometry: sphere + cube
sphere = vtkSphereSource()

cube = vtkCubeSource()
cube.SetCenter(0.0, 0.0, 2.0)

source = vtkAppendPolyData()
source.AddInputConnection(sphere.GetOutputPort())
source.AddInputConnection(cube.GetOutputPort())
source.Update()

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(source.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Left viewport: main interactive view
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0.0, 0.0, 0.5, 1.0)
renderer_0.AddActor(actor)
renderer_0.SetBackground(0.7, 0.7, 1.0)

# Right viewport: camera preview (non-interactive)
renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.5, 0.0, 1.0, 1.0)
renderer_1.InteractiveOff()
renderer_1.AddActor(actor)
renderer_1.SetBackground(0.8, 0.8, 1.0)

# Set up rendering pipeline
render_window = vtkRenderWindow()
render_window.SetWindowName("camera3d widget")
render_window.SetSize(600, 300)
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Create the camera 3D widget and representation
camera_rep = vtkCamera3DRepresentation()
camera_widget = vtkCamera3DWidget()
camera_widget.SetInteractor(interactor)
camera_widget.SetRepresentation(camera_rep)

# Set the camera before placing the widget
camera_rep.SetCamera(renderer_1.GetActiveCamera())
camera_rep.PlaceWidget(actor.GetBounds())
camera_widget.On()

interactor.Initialize()
interactor.Start()
