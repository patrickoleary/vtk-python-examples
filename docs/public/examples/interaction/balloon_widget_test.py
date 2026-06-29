#!/usr/bin/env python
# Demonstrate vtkBalloonWidget with hover tooltips on sphere, cylinder, and cone actors.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import os

from vtkmodules.vtkFiltersSources import (
    vtkConeSource,
    vtkCylinderSource,
    vtkSphereSource,
)
from vtkmodules.vtkInteractionWidgets import (
    vtkBalloonRepresentation,
    vtkBalloonWidget,
)
from vtkmodules.vtkIOImage import vtkTIFFReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkPropPicker,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Dataset: balloon tooltip image
data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))
image_reader = vtkTIFFReader()
image_reader.SetFileName(os.path.join(data_dir, "beach.tif"))
image_reader.SetOrientationType(4)

# Source + Mapper + Actor: sphere
sphere = vtkSphereSource()
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Source + Mapper + Actor: cylinder
cylinder = vtkCylinderSource()
cylinder_mapper = vtkPolyDataMapper()
cylinder_mapper.SetInputConnection(cylinder.GetOutputPort())
cylinder_actor = vtkActor()
cylinder_actor.SetMapper(cylinder_mapper)
cylinder_actor.AddPosition(5, 0, 0)

# Source + Mapper + Actor: cone
cone = vtkConeSource()
cone_mapper = vtkPolyDataMapper()
cone_mapper.SetInputConnection(cone.GetOutputPort())
cone_actor = vtkActor()
cone_actor.SetMapper(cone_mapper)
cone_actor.AddPosition(0, 5, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cylinder_actor)
renderer.AddActor(cone_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("balloon widget test")
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

picker = vtkPropPicker()
interactor.SetPicker(picker)


# Callbacks
def pick_callback(caller, event_string):
    prop = caller.GetViewProp()
    if prop is not None:
        balloon_widget.UpdateBalloonString(prop, "Picked")


picker.AddObserver("PickEvent", pick_callback)


def balloon_callback(widget, event_string):
    if widget.GetCurrentProp() is not None:
        print("Prop selected")


# Widget
balloon_rep = vtkBalloonRepresentation()
balloon_rep.SetBalloonLayoutToImageRight()

balloon_widget = vtkBalloonWidget()
balloon_widget.SetInteractor(interactor)
balloon_widget.SetRepresentation(balloon_rep)
balloon_widget.AddBalloon(sphere_actor, "This is a sphere", None)
balloon_widget.AddBalloon(cylinder_actor, "This is a\ncylinder", image_reader.GetOutput())
balloon_widget.AddBalloon(
    cone_actor,
    "This is a\ncone,\na really big cone,\nyou wouldn't believe how big",
    image_reader.GetOutput(),
)
balloon_widget.AddObserver("WidgetActivateEvent", balloon_callback)
balloon_widget.On()

interactor.Initialize()
interactor.Start()
