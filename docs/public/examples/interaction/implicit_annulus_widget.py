#!/usr/bin/env python
# Demonstrate vtkImplicitAnnulusWidget clipping a sphere geometry.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkAnnulus
from vtkmodules.vtkFiltersCore import vtkClipPolyData
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

# Source
sphere = vtkSphereSource()

# Implicit function + Filter
annulus = vtkAnnulus()
clipper = vtkClipPolyData()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetClipFunction(annulus)

# Mapper + Actor: sphere
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Mapper + Actor: clipped region
clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clipper.GetOutputPort())

clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(0, 1, 0)
clip_actor.VisibilityOff()
clip_actor.SetScale(1.01, 1.01, 1.01)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(clip_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit annulus widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback updates the annulus implicit function on interaction
def annulus_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    widget_rep.GetAnnulus(annulus)
    clip_actor.VisibilityOn()


# Widget
annulus_rep = vtkImplicitAnnulusRepresentation()
annulus_rep.SetPlaceFactor(1.25)
annulus_rep.PlaceWidget(sphere.GetOutput().GetBounds())

annulus_widget = vtkImplicitAnnulusWidget()
annulus_widget.SetInteractor(interactor)
annulus_widget.SetRepresentation(annulus_rep)
annulus_widget.AddObserver("InteractionEvent", annulus_callback)
annulus_widget.SetEnabled(True)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
