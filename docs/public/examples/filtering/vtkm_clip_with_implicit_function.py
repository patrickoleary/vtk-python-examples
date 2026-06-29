#!/usr/bin/env python
# Demonstrate vtkmClip with a sphere implicit function on a wavelet source.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmClip
from vtkmodules.vtkCommonDataModel import vtkSphere
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Wavelet source.
wavelet = vtkRTAnalyticSource()
wavelet.SetWholeExtent(-8, 8, -8, 8, -8, 8)
wavelet.SetCenter(0, 0, 0)

# Sphere implicit function for clipping.
sphere = vtkSphere()
sphere.SetCenter(0, 0, 0)
sphere.SetRadius(10)

# Clip with implicit function via VTK-m.
clip = vtkmClip()
clip.SetInputConnection(wavelet.GetOutputPort())
clip.SetClipFunction(sphere)

# Extract surface.
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(clip.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.SetScalarRange(37, 150)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm clip with implicit function")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
