#!/usr/bin/env python

# Plane cut a wavelet volume using vtkFlyingEdgesPlaneCutter with an
# interactive implicit plane widget to manipulate the cut plane.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkFlyingEdgesPlaneCutter
from vtkmodules.vtkFiltersModeling import vtkImageDataOutlineFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
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

# Source: wavelet
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(1, 1, 1)
plane.SetNormal(2, 1, 1.5)

# Plane cutter
cutter = vtkFlyingEdgesPlaneCutter()
cutter.SetInputConnection(wavelet.GetOutputPort())
cutter.SetPlane(plane)

cutter_mapper = vtkPolyDataMapper()
cutter_mapper.SetInputConnection(cutter.GetOutputPort())

cutter_actor = vtkActor()
cutter_actor.SetMapper(cutter_mapper)

# Outline around the image
outline = vtkImageDataOutlineFilter()
outline.SetInputConnection(wavelet.GetOutputPort())
outline.GenerateFacesOn()
outline.Update()

outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline.GetOutputPort())

outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetOpacity(0.25)
outline_actor.GetProperty().SetColor(0, 1, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(outline_actor)
renderer.AddActor(cutter_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(1000, 1000)
render_window.SetWindowName("flying edges plane cut interactive")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Widget callback to update the cut plane (def required for VTK observer)
def move_plane(widget, event_string):
    rep.GetPlane(plane)
    cutter.Modified()

# Implicit plane widget
rep = vtkImplicitPlaneRepresentation()
rep.SetPlaceFactor(1.0)
rep.PlaceWidget(wavelet.GetOutput().GetBounds())
rep.DrawPlaneOff()
rep.SetPlane(plane)

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(interactor)
plane_widget.SetRepresentation(rep)
plane_widget.AddObserver("InteractionEvent", move_plane)
plane_widget.On()

interactor.Initialize()
interactor.Start()
