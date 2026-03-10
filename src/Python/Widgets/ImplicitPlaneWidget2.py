#!/usr/bin/env python

# Use an implicit plane widget to interactively clip a sphere.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkCommand
from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkClipPolyData
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkInteractionWidgets import (
    vtkImplicitPlaneRepresentation,
    vtkImplicitPlaneWidget2,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkProperty,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
gold_rgb = (1.0, 0.843, 0.0)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: generate a sphere
sphere_source = vtkSphereSource()
sphere_source.SetRadius(10.0)

# Clip plane: the implicit function used for clipping
plane = vtkPlane()

# Filter: clip the sphere with the plane
clipper = vtkClipPolyData()
clipper.SetClipFunction(plane)
clipper.InsideOutOn()
clipper.SetInputConnection(sphere_source.GetOutputPort())

# Mapper: map clipped polygon data to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)

back_faces = vtkProperty()
back_faces.SetDiffuseColor(gold_rgb)
actor.SetBackfaceProperty(back_faces)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.SetSize(640, 480)
render_window.SetWindowName("ImplicitPlaneWidget2")
render_window.AddRenderer(renderer)

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# ImplicitPlaneWidget2: interactive plane for clipping
rep = vtkImplicitPlaneRepresentation()
rep.SetPlaceFactor(1.25)
rep.PlaceWidget(actor.GetBounds())
rep.SetNormal(plane.GetNormal())

plane_widget = vtkImplicitPlaneWidget2()
plane_widget.SetInteractor(render_window_interactor)
plane_widget.SetRepresentation(rep)

plane_widget.AddObserver(vtkCommand.InteractionEvent,
                         lambda caller, event: caller.GetRepresentation().GetPlane(plane))

# Camera: set a good viewing angle
renderer.GetActiveCamera().Azimuth(-60)
renderer.GetActiveCamera().Elevation(30)
renderer.ResetCamera()
renderer.GetActiveCamera().Zoom(0.75)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window.Render()
plane_widget.On()
render_window_interactor.Start()
