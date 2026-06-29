#!/usr/bin/env python
# Demonstrate vtkmThreshold with between thresholding on a wavelet with elevation coloring.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmThreshold
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkElevationFilter, vtkThreshold
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
source = vtkRTAnalyticSource()

# Elevation field.
elevation = vtkElevationFilter()
elevation.SetInputConnection(source.GetOutputPort())
elevation.SetScalarRange(0.0, 1.0)
elevation.SetLowPoint(-10.0, -10.0, -10.0)
elevation.SetHighPoint(10.0, 10.0, 10.0)

# Threshold via VTK-m between 100 and 200 on RTData.
threshold = vtkmThreshold()
threshold.SetInputConnection(elevation.GetOutputPort())
threshold.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "RTData"
)
threshold.SetThresholdFunction(vtkThreshold.THRESHOLD_BETWEEN)
threshold.SetLowerThreshold(100.0)
threshold.SetUpperThreshold(200.0)
threshold.SetAllScalars(0)

# Extract surface.
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(threshold.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
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
render_window.SetWindowName("vtkm threshold between")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
