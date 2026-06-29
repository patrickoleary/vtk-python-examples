#!/usr/bin/env python
# Demonstrate vtkPolyDataSilhouette extracting silhouette edges from a sphere.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersHybrid import vtkPolyDataSilhouette
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere geometry
sphere = vtkSphereSource()
sphere.Update()

# Surface actor
mapper = vtkPolyDataMapper()
mapper.SetInputData(sphere.GetOutput())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetInterpolationToFlat()

renderer = vtkRenderer()
renderer.SetBackground(0.1, 0.2, 0.3)
renderer.AddActor(actor)

# Silhouette extraction
silhouette = vtkPolyDataSilhouette()
silhouette.SetInputData(sphere.GetOutput())
silhouette.SetCamera(renderer.GetActiveCamera())
silhouette.SetEnableFeatureAngle(0)

silhouette_mapper = vtkPolyDataMapper()
silhouette_mapper.SetInputConnection(silhouette.GetOutputPort())

silhouette_actor = vtkActor()
silhouette_actor.SetMapper(silhouette_mapper)
silhouette_actor.GetProperty().SetColor(1.0, 0.3882, 0.2784)
silhouette_actor.GetProperty().SetLineWidth(5)

renderer.AddActor(silhouette_actor)

render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("polydata silhouette")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
