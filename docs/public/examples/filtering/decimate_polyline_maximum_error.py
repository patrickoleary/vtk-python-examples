#!/usr/bin/env python

# Decimate a polyline extracted from a plane boundary using
# vtkDecimatePolylineFilter with a maximum error constraint.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersCore import (
    vtkDecimatePolylineFilter,
    vtkFeatureEdges,
    vtkStripper,
)
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Source: plane with boundary edges
plane = vtkPlaneSource()
plane.SetResolution(50, 100)

# Extract boundary edges
feature_edges = vtkFeatureEdges()
feature_edges.SetInputConnection(plane.GetOutputPort())
feature_edges.BoundaryEdgesOn()
feature_edges.FeatureEdgesOff()
feature_edges.NonManifoldEdgesOff()

# Strip edges into polylines
stripper = vtkStripper()
stripper.SetInputConnection(feature_edges.GetOutputPort())

# Decimate with maximum error constraint
decimator = vtkDecimatePolylineFilter()
decimator.SetInputConnection(stripper.GetOutputPort())
decimator.SetMaximumError(0.00001)
decimator.SetTargetReduction(0.99)
decimator.Update()

# Mapper
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(decimator.GetOutputPort())

# Actor
actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("decimate polyline maximum error")

# Scene
camera = renderer.GetActiveCamera()
camera.SetPosition(0, 0, 1)
camera.SetFocalPoint(0, 0, 0)
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
