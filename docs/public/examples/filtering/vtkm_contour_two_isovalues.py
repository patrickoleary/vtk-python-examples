#!/usr/bin/env python
# Demonstrate vtkmContour with two isovalues on a wavelet source with elevation coloring.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmContour
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkImagingCore import vtkRTAnalyticSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

EXTENT = 30

# Wavelet source.
image_source = vtkRTAnalyticSource()
image_source.SetWholeExtent(-EXTENT, EXTENT, -EXTENT, EXTENT, -EXTENT, EXTENT)

# Elevation field.
ev = vtkElevationFilter()
ev.SetInputConnection(image_source.GetOutputPort())
ev.SetLowPoint(-EXTENT, -EXTENT, -EXTENT)
ev.SetHighPoint(EXTENT, EXTENT, EXTENT)

# Contour via VTK-m with two isovalues.
cg = vtkmContour()
cg.SetInputConnection(ev.GetOutputPort())
cg.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData"
)
cg.SetValue(0, 200.0)
cg.SetValue(1, 220.0)
cg.ComputeScalarsOn()
cg.ComputeNormalsOn()

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cg.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Elevation")
mapper.SetScalarRange(0.0, 1.0)

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm contour two isovalues")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
