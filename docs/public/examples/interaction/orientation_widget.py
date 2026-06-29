#!/usr/bin/env python
# Demonstrate vtkOrientationWidget controlling the orientation of a cube actor.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersSources import vtkCubeSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleTrackballCamera
from vtkmodules.vtkInteractionWidgets import (
    vtkOrientationRepresentation,
    vtkOrientationWidget,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source
cube_source = vtkCubeSource()

# Mapper + Actor
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube_source.GetOutputPort())

cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cube_actor)
renderer.SetBackground(0.7, 0.7, 1.0)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("orientation widget")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
style = vtkInteractorStyleTrackballCamera()

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)
interactor.SetInteractorStyle(style)


# Callback syncs the cube actor orientation with the widget
def orientation_callback(caller, event_string):
    widget_rep = caller.GetRepresentation()
    cube_actor.SetOrientation(widget_rep.GetOrientation())


# Widget
orientation_rep = vtkOrientationRepresentation()
orientation_rep.PlaceWidget(cube_actor.GetBounds())
orientation_rep.ShowArrowsOn()
orientation_rep.SetArrowDistance(0.05)
orientation_rep.SetArrowLength(0.1)
orientation_rep.SetArrowTipLength(0.35)
orientation_rep.SetArrowTipRadius(0.03)
orientation_rep.SetArrowShaftRadius(0.01)
orientation_rep.GetPropertyX(False).SetColor(1.0, 0.0, 1.0)
orientation_rep.GetPropertyY(True).SetColor(1.0, 1.0, 0.0)

property_z = vtkProperty()
property_z.SetColor(0.0, 1.0, 1.0)
orientation_rep.SetPropertyZ(False, property_z)

orientation_widget = vtkOrientationWidget()
orientation_widget.SetInteractor(interactor)
orientation_widget.SetRepresentation(orientation_rep)
orientation_widget.AddObserver("InteractionEvent", orientation_callback)
orientation_widget.On()

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(1.0, 1.0, -4.0)
renderer.ResetCameraClippingRange()

interactor.Initialize()
interactor.Start()
