#!/usr/bin/env python

# Demonstrate vtkGroupDataSetsFilter by grouping multiple sources into
# a partitioned dataset collection and rendering the combined result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkGroupDataSetsFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create sources
sphere = vtkSphereSource()
sphere.SetCenter(0, 0, 0)
sphere.Update()

sphere_2 = vtkSphereSource()
sphere_2.SetCenter(3, 0, 0)
sphere_2.Update()

# Group datasets
group = vtkGroupDataSetsFilter()
group.AddInputConnection(sphere.GetOutputPort())
group.AddInputConnection(sphere_2.GetOutputPort())
group.SetInputName(0, "Sphere0")
group.SetInputName(1, "Sphere1")
group.Update()

# Render with composite mapper
mapper = vtkCompositePolyDataMapper()
mapper.SetInputConnection(group.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("group datasets")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
