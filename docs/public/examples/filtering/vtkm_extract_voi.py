#!/usr/bin/env python
# Demonstrate vtkmExtractVOI extracting a sub-region from a wavelet with sampling.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmExtractVOI
from vtkmodules.vtkFiltersCore import vtkTriangleFilter
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersSources import vtkSphereSource
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Sphere for reference.
sphere = vtkSphereSource()
sphere.SetRadius(2.0)

sphere_mapper = vtkPolyDataMapper()
sphere_mapper.SetInputConnection(sphere.GetOutputPort())

sphere_actor = vtkActor()
sphere_actor.SetMapper(sphere_mapper)

# Wavelet source.
rt = vtkRTAnalyticSource()
rt.SetWholeExtent(-50, 50, -50, 50, 0, 0)

# Extract VOI via VTK-m.
voi = vtkmExtractVOI()
voi.SetInputConnection(rt.GetOutputPort())
voi.SetVOI(-11, 39, 5, 45, 0, 0)
voi.SetSampleRate(5, 5, 1)

# Surface and triangulate.
surf = vtkDataSetSurfaceFilter()
surf.SetInputConnection(voi.GetOutputPort())

tris = vtkTriangleFilter()
tris.SetInputConnection(surf.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(tris.GetOutputPort())
mapper.SetScalarRange(130, 280)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(sphere_actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm extract voi")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
