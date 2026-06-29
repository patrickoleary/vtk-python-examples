#!/usr/bin/env python

# Demonstrate vtkDistancePolyDataFilter by computing signed distances
# between two overlapping spheres and rendering both outputs colored
# by distance with a scalar bar.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkDistancePolyDataFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create two overlapping spheres
sphere_0 = vtkSphereSource()
sphere_0.SetPhiResolution(11)
sphere_0.SetThetaResolution(11)
sphere_0.SetCenter(0.0, 0.0, 0.0)

sphere_1 = vtkSphereSource()
sphere_1.SetPhiResolution(11)
sphere_1.SetThetaResolution(11)
sphere_1.SetCenter(0.2, 0.3, 0.0)

# Compute distance
distance_filter = vtkDistancePolyDataFilter()
distance_filter.SetInputConnection(0, sphere_0.GetOutputPort())
distance_filter.SetInputConnection(1, sphere_1.GetOutputPort())
distance_filter.Update()

# First output: distance on sphere 0
scalar_range_0 = distance_filter.GetOutput().GetPointData().GetScalars().GetRange()

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(distance_filter.GetOutputPort())
mapper_0.SetScalarRange(scalar_range_0[0], scalar_range_0[1])

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Second output: distance on sphere 1
scalar_range_1 = distance_filter.GetSecondDistanceOutput().GetPointData().GetScalars().GetRange()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(distance_filter.GetOutputPort(1))
mapper_1.SetScalarRange(scalar_range_1[0], scalar_range_1[1])

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Scalar bar
scalar_bar = vtkScalarBarActor()
scalar_bar.SetLookupTable(mapper_0.GetLookupTable())
scalar_bar.SetTitle("Distance")
scalar_bar.SetNumberOfLabels(5)
scalar_bar.SetTextPad(4)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_0)
renderer.AddActor(actor_1)
renderer.AddViewProp(scalar_bar)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("distance polydata")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
