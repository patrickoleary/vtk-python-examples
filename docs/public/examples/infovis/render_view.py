#!/usr/bin/env python
# Demonstrate sphere and cube surface rendering using explicit pipeline.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersGeneral import vtkTransformFilter
from vtkmodules.vtkFiltersSources import vtkCubeSource, vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sources.
sphere = vtkSphereSource()

cube = vtkCubeSource()
cube.SetCenter(2, 0, 0)

transform_filter = vtkTransformFilter()
transform = vtkTransform()
transform.Translate(0, 2, 0)
transform_filter.SetTransform(transform)
transform_filter.SetInputConnection(sphere.GetOutputPort())

# Sphere mapper and actor.
sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())
sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Cube mapper and actor.
cube_mapper = vtkPolyDataMapper()
cube_mapper.SetInputConnection(cube.GetOutputPort())
cube_actor = vtkActor()
cube_actor.SetMapper(cube_mapper)

# Transformed sphere mapper and actor.
transform_mapper = vtkPolyDataMapper()
transform_mapper.SetInputConnection(transform_filter.GetOutputPort())
transform_actor = vtkActor()
transform_actor.SetMapper(transform_mapper)

# Renderer.
renderer = vtkRenderer()
renderer.AddActor(sphere_actor)
renderer.AddActor(cube_actor)
renderer.AddActor(transform_actor)
renderer.GradientBackgroundOff()
renderer.ResetCamera()

# Render window.
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("render view")
render_window.SetMultiSamples(0)
render_window.SetSize(400, 400)

# Interactor.
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
