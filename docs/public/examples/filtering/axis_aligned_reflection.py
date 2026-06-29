#!/usr/bin/env python

# Demonstrate vtkAxisAlignedReflectionFilter by reflecting a sphere
# through the X_MIN plane and rendering the original and reflected
# surfaces side by side.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkFiltersGeneral import vtkAxisAlignedReflectionFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCompositePolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a sphere source
sphere = vtkSphereSource()
sphere.SetCenter(1.0, 0.0, 0.0)
sphere.SetRadius(0.5)
sphere.SetPhiResolution(20)
sphere.SetThetaResolution(20)

# Reflect through X_MIN
reflect = vtkAxisAlignedReflectionFilter()
reflect.SetInputConnection(sphere.GetOutputPort())
reflect.SetCopyInput(True)
reflect.SetReflectAllInputArrays(True)
reflect.SetPlaneMode(vtkAxisAlignedReflectionFilter.X_MIN)
reflect.Update()

# Extract surfaces from the partitioned dataset collection output
surface = vtkDataSetSurfaceFilter()
surface.SetInputData(reflect.GetOutput().GetPartition(0, 0))

mapper_original = vtkCompositePolyDataMapper()
mapper_original.SetInputConnection(surface.GetOutputPort())

actor_original = vtkActor()
actor_original.SetMapper(mapper_original)
actor_original.GetProperty().SetColor(0.2, 0.6, 1.0)

surface_reflected = vtkDataSetSurfaceFilter()
surface_reflected.SetInputData(reflect.GetOutput().GetPartition(1, 0))

mapper_reflected = vtkCompositePolyDataMapper()
mapper_reflected.SetInputConnection(surface_reflected.GetOutputPort())

actor_reflected = vtkActor()
actor_reflected.SetMapper(mapper_reflected)
actor_reflected.GetProperty().SetColor(1.0, 0.4, 0.2)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor_original)
renderer.AddActor(actor_reflected)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(400, 400)
render_window.SetWindowName("axis aligned reflection")

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

# Scene
renderer.ResetCamera()

interactor.Initialize()
interactor.Start()
