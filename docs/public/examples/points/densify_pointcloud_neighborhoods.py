#!/usr/bin/env python

# Demonstrate vtkDensifyPointCloudFilter with different neighborhood types
# (N closest points and radius) on a platonic cube, showing original and
# densified point clouds as glyphed spheres in three viewports.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkMath
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersPoints import vtkDensifyPointCloudFilter
from vtkmodules.vtkFiltersSources import (
    vtkPlatonicSolidSource,
    vtkSphereSource,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

math = vtkMath()
math.RandomSeed(31415)

# Eight points forming a cube
cube = vtkPlatonicSolidSource()
cube.SetSolidTypeToCube()

sphere = vtkSphereSource()
sphere.SetRadius(0.05)

# Original cube points as glyphs
glyphs_0 = vtkGlyph3D()
glyphs_0.SetInputConnection(cube.GetOutputPort())
glyphs_0.SetSourceConnection(sphere.GetOutputPort())
glyphs_0.ScalingOff()
glyphs_0.OrientOff()

mapper_0 = vtkPolyDataMapper()
mapper_0.SetInputConnection(glyphs_0.GetOutputPort())

actor_0 = vtkActor()
actor_0.SetMapper(mapper_0)

# Densify using N closest points
densify_filter_1 = vtkDensifyPointCloudFilter()
densify_filter_1.SetInputConnection(cube.GetOutputPort())
densify_filter_1.SetNeighborhoodTypeToNClosest()
densify_filter_1.SetNumberOfClosestPoints(3)
densify_filter_1.SetTargetDistance(1.0)
densify_filter_1.SetMaximumNumberOfIterations(3)

glyphs_1 = vtkGlyph3D()
glyphs_1.SetInputConnection(densify_filter_1.GetOutputPort())
glyphs_1.SetSourceConnection(sphere.GetOutputPort())
glyphs_1.ScalingOff()
glyphs_1.OrientOff()

mapper_1 = vtkPolyDataMapper()
mapper_1.SetInputConnection(glyphs_1.GetOutputPort())

actor_1 = vtkActor()
actor_1.SetMapper(mapper_1)

# Densify using radius
densify_filter_2 = vtkDensifyPointCloudFilter()
densify_filter_2.SetInputConnection(cube.GetOutputPort())
densify_filter_2.SetNeighborhoodTypeToRadius()
densify_filter_2.SetRadius(1.8)
densify_filter_2.SetTargetDistance(1.0)
densify_filter_2.SetMaximumNumberOfIterations(10)
densify_filter_2.SetMaximumNumberOfPoints(50)
densify_filter_2.Update()

glyphs_2 = vtkGlyph3D()
glyphs_2.SetInputConnection(densify_filter_2.GetOutputPort())
glyphs_2.SetSourceConnection(sphere.GetOutputPort())
glyphs_2.ScalingOff()
glyphs_2.OrientOff()

mapper_2 = vtkPolyDataMapper()
mapper_2.SetInputConnection(glyphs_2.GetOutputPort())

actor_2 = vtkActor()
actor_2.SetMapper(mapper_2)

# Three viewports
renderer_0 = vtkRenderer()
renderer_0.SetViewport(0, 0, 0.333, 1.0)
renderer_0.AddActor(actor_0)
renderer_0.SetBackground(0, 0, 0)

renderer_1 = vtkRenderer()
renderer_1.SetViewport(0.333, 0, 0.6667, 1.0)
renderer_1.AddActor(actor_1)
renderer_1.SetBackground(0, 0, 0)

renderer_2 = vtkRenderer()
renderer_2.SetViewport(0.6667, 0, 1, 1.0)
renderer_2.AddActor(actor_2)
renderer_2.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer_0)
render_window.AddRenderer(renderer_1)
render_window.AddRenderer(renderer_2)
render_window.SetSize(900, 300)
render_window.SetWindowName("densify pointcloud neighborhoods")

# Scene
camera = renderer_0.GetActiveCamera()
camera.SetFocalPoint(0, 0, 0)
camera.SetPosition(1, 1, 1)
renderer_0.ResetCamera()
renderer_1.SetActiveCamera(camera)
renderer_2.SetActiveCamera(camera)

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
