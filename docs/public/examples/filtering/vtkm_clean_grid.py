#!/usr/bin/env python
# Demonstrate vtkmCleanGrid on a wavelet source with geometry extraction.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmCleanGrid
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
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
wavelet.SetWholeExtent(-10, 10, -10, 10, -10, 10)
wavelet.SetCenter(0, 0, 0)

# Clean grid via VTK-m.
clean_grid = vtkmCleanGrid()
clean_grid.SetInputConnection(wavelet.GetOutputPort())

# Extract surface geometry.
geometry = vtkGeometryFilter()
geometry.SetInputConnection(clean_grid.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(geometry.GetOutputPort())
mapper.SetScalarRange(37, 277)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm clean grid")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
