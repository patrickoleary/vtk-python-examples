#!/usr/bin/env python

# Clip a high-resolution sphere with a plane using vtkPolyDataPlaneClipper,
# displaying both the clipped surface and the capping polygon.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonDataModel import vtkPlane
from vtkmodules.vtkFiltersCore import vtkPolyDataPlaneClipper
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

resolution = 1024

# Source: high-resolution sphere
sphere = vtkSphereSource()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(0.25)
sphere.SetThetaResolution(2 * resolution)
sphere.SetPhiResolution(resolution)
sphere.Update()

# Cut plane
plane = vtkPlane()
plane.SetOrigin(0, 0, 0)
plane.SetNormal(-1, -1, -1)

# Plane clipper with capping
clipper = vtkPolyDataPlaneClipper()
clipper.SetInputConnection(sphere.GetOutputPort())
clipper.SetPlane(plane)
clipper.SetBatchSize(10000)
clipper.CappingOn()
clipper.Update()

# Clipped surface
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(clipper.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Cap surface
cap_mapper = vtkPolyDataMapper()
cap_mapper.SetInputConnection(clipper.GetOutputPort(1))

cap_actor = vtkActor()
cap_actor.SetMapper(cap_mapper)
cap_actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(cap_actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("polydata plane clipper")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
