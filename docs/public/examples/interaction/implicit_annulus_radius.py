#!/usr/bin/env python
# Demonstrate vtkImplicitAnnulusWidget radius interaction testing.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitAnnulusRepresentation,
    vtkImplicitAnnulusWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source + Mapper + Actor
sphere = vtkSphereSource()
sphere.Update()
sphere_bounds = sphere.GetOutput().GetBounds()

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)
sphere_actor.VisibilityOn()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit annulus radius")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget
annulus_rep = vtkImplicitAnnulusRepresentation()
annulus_rep.SetPlaceFactor(1.25)
annulus_rep.PlaceWidget(sphere_bounds)

annulus_widget = vtkImplicitAnnulusWidget()
annulus_widget.SetInteractor(interactor)
annulus_widget.SetRepresentation(annulus_rep)
annulus_widget.SetEnabled(True)

# Scene
renderer.ResetCamera()
renderer.GetActiveCamera().Azimuth(90)

interactor.Initialize()
interactor.Start()
