#!/usr/bin/env python
# Demonstrate vtkSeedWidget for placing and interacting with seed points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkPointHandleRepresentation2D,
    vtkSeedRepresentation,
    vtkSeedWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
sphere_source = vtkSphereSource()

# Mapper + Actor
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere_source.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("seed widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback for seed widget events
def seed_callback(caller, event_string):
    if event_string == "PlacePointEvent":
        print(f"Point placed, total of: {seed_rep.GetNumberOfSeeds()}")
    elif event_string == "StartInteractionEvent":
        print("Start interacting with seed")
    elif event_string == "InteractionEvent":
        print("Interacting with seed")


# Widget
handle_rep = vtkPointHandleRepresentation2D()
handle_rep.GetProperty().SetColor(1, 0, 0)

seed_rep = vtkSeedRepresentation()
seed_rep.SetHandleRepresentation(handle_rep)

seed_widget = vtkSeedWidget()
seed_widget.SetInteractor(interactor)
seed_widget.SetRepresentation(seed_rep)
seed_widget.AddObserver("PlacePointEvent", seed_callback)
seed_widget.AddObserver("StartInteractionEvent", seed_callback)
seed_widget.AddObserver("InteractionEvent", seed_callback)
seed_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
