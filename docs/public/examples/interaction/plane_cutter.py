#!/usr/bin/env python
# Demonstrate vtkImplicitPlaneWidget2 with vtkFlyingEdgesPlaneCutter on sampled sphere data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkFiltersCore import vtkFlyingEdgesPlaneCutter
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: sample a sphere across a volume
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

resolution = 100
sample = vtkSampleFunction()
sample.SetImplicitFunction(sphere)
sample.SetModelBounds(-0.5, 0.5, -0.5, 0.5, -0.5, 0.5)
sample.SetSampleDimensions(resolution, resolution, resolution)
sample.SetOutputScalarTypeToFloat()
sample.Update()

# Define the cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(1, 1, 1)

# Filter
cutter = vtkFlyingEdgesPlaneCutter()
cutter.SetInputConnection(sample.GetOutputPort())
cutter.SetPlane(plane)
cutter.ComputeNormalsOff()

# Mapper + Actor
cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)
cutter_actor.GetProperty().SetColor(1, 1, 1)
cutter_actor.GetProperty().SetOpacity(1)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(cutter_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("plane cutter")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback to update the plane from widget interaction
def move_plane(widget, event_string):
    plane_rep.GetPlane(plane)


# Widget
plane_rep = vtkImplicitPlaneRepresentation()
plane_rep.SetPlaceFactor(1.0)
plane_rep.PlaceWidget(sample.GetOutput().GetBounds())
plane_rep.DrawPlaneOff()
plane_rep.SetPlane(plane)

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(plane_rep)
plane_widget.AddObserver("InteractionEvent", move_plane)
plane_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
