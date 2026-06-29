#!/usr/bin/env python
# Demonstrate vtkImplicitImageRepresentation with vtkImplicitPlaneWidget2 on sampled sphere data.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import (
    vtkPlane,
    vtkSphere,
)
from vtkmodules.vtkImagingHybrid import vtkSampleFunction
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitImageRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: sample a sphere across a volume
sphere = vtkSphere()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)

resolution = 200
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

# Renderer
renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.4)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("implicit image representation")
render_window.SetMultiSamples(0)
render_window.SetSize(300, 300)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)


# Callback to update the plane from widget interaction
def move_plane(widget, event_string):
    image_rep.GetPlane(plane)


# Widget
image_rep = vtkImplicitImageRepresentation()
image_rep.SetPlaceFactor(1.0)
image_rep.PlaceImage(sample.GetOutputPort())
image_rep.SetPlane(plane)

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(image_rep)
plane_widget.AddObserver("InteractionEvent", move_plane)
plane_widget.On()

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
