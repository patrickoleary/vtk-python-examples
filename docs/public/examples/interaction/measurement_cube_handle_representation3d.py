#!/usr/bin/env python
# Demonstrate vtkMeasurementCubeHandleRepresentation3D with a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkHandleWidget,
    vtkMeasurementCubeHandleRepresentation3D,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

bounds = [-1.0, 1.0, -1.0, 1.0, -1.0, 1.0]

# Source
sphere_source = vtkSphereSource()
sphere_source.Update()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("measurement cube handle representation3d")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
unit_cube_rep = vtkMeasurementCubeHandleRepresentation3D()
unit_cube_rep.PlaceWidget(bounds)
unit_cube_rep.SetHandleSize(30)
unit_cube_rep.SetWorldPosition((1.0, 0.0, 0.0))

handle_widget = vtkHandleWidget()
handle_widget.SetInteractor(interactor)
handle_widget.SetRepresentation(unit_cube_rep)
handle_widget.EnabledOn()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
