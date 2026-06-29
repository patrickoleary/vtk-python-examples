#!/usr/bin/env python

# Demonstrate vtkAxisAlignedTransformFilter by applying translation,
# scaling, and rotation to a sphere and rendering the original and
# transformed surfaces.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkAxisAlignedTransformFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere source
sphere = vtkSphereSource()
sphere.SetCenter(0.0, 0.0, 0.0)
sphere.SetRadius(1.0)
sphere.SetPhiResolution(20)
sphere.SetThetaResolution(20)

# Original surface
surface_orig = vtkDataSetSurfaceFilter()
surface_orig.SetInputConnection(sphere.GetOutputPort())

mapper_orig = vtkPolyDataMapper()
mapper_orig.SetInputConnection(surface_orig.GetOutputPort())

actor_orig = vtkActor()
actor_orig.SetMapper(mapper_orig)
actor_orig.GetProperty().SetColor(0.8, 0.8, 0.8)
actor_orig.GetProperty().SetOpacity(0.3)

# Apply axis-aligned transform: translate, scale, and rotate 90 deg about X
transform = vtkAxisAlignedTransformFilter()
transform.SetInputConnection(sphere.GetOutputPort())
transform.SetTranslation(2.0, 1.0, 0.0)
transform.SetScale(1.5, 0.5, 1.0)
transform.SetRotationAngle(1)  # ROT90
transform.SetRotationAxis(0)   # X axis
transform.Update()

# Transformed surface
surface_xform = vtkDataSetSurfaceFilter()
surface_xform.SetInputConnection(transform.GetOutputPort())

mapper_xform = vtkPolyDataMapper()
mapper_xform.SetInputConnection(surface_xform.GetOutputPort())

actor_xform = vtkActor()
actor_xform.SetMapper(mapper_xform)
actor_xform.GetProperty().SetColor(1.0, 0.3, 0.3)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_orig)
renderer.AddActor(actor_xform)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("axis aligned transform")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
