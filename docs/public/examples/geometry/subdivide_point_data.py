#!/usr/bin/env python

# Demonstrate vtkButterflySubdivisionFilter and vtkLinearSubdivisionFilter
# preserving point data (elevation) on a sphere, shown in three viewports:
# butterfly subdivision, linear subdivision, and original sphere.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersModeling import (
    vtkButterflySubdivisionFilter,
    vtkLinearSubdivisionFilter,
)
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkLight,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere with elevation coloring
sphere = vtkSphereSource()
sphere.SetPhiResolution(11)
sphere.SetThetaResolution(11)

color_it = vtkElevationFilter()
color_it.SetInputConnection(sphere.GetOutputPort())
color_it.SetLowPoint(0, 0, -0.5)
color_it.SetHighPoint(0, 0, 0.5)

# Butterfly subdivision
butterfly = vtkButterflySubdivisionFilter()
butterfly.SetInputConnection(color_it.GetOutputPort())
butterfly.SetNumberOfSubdivisions(3)

# Linear subdivision
linear = vtkLinearSubdivisionFilter()
linear.SetInputConnection(color_it.GetOutputPort())
linear.SetNumberOfSubdivisions(3)

lookup_table = vtkLookupTable()
lookup_table.SetNumberOfColors(256)
lookup_table.Build()

# Mapper and actor pairs
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(butterfly.GetOutputPort())
mapper.SetLookupTable(lookup_table)
actor = vtkActor()
actor.SetMapper(mapper)

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(linear.GetOutputPort())
mapper_2.SetLookupTable(lookup_table)
actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

mapper_3 = vtkPolyDataMapper()
mapper_3.SetInputConnection(color_it.GetOutputPort())
mapper_3.SetLookupTable(lookup_table)
actor_3 = vtkActor()
actor_3.SetMapper(mapper_3)

# Renderers
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.33, 1)
renderer_0.AddActor(actor_3)
renderer_0.SetBackground(1, 1, 1)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.33, 0, 0.67, 1)
renderer_1.AddActor(actor_2)
renderer_1.SetBackground(1, 1, 1)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.67, 0, 1, 1)
renderer_2.AddActor(actor)
renderer_2.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(600, 200)
render_window.SetWindowName("subdivide point data")

# Scene
camera = vtkCamera()
camera.Azimuth(70)

light = vtkLight()
light.SetPosition(camera.GetPosition())
light.SetFocalPoint(camera.GetFocalPoint())

renderer_2.SetActiveCamera(camera)
renderer_2.AddLight(light)
renderer_2.ResetCamera()
camera.Dolly(1.4)
renderer_2.ResetCameraClippingRange()

renderer_1.SetActiveCamera(camera)
renderer_1.AddLight(light)

renderer_0.SetActiveCamera(camera)
renderer_0.AddLight(light)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
