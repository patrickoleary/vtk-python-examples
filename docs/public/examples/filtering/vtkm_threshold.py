#!/usr/bin/env python
# Demonstrate vtkmThreshold on an image data grid with computed elevation scalars.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmThreshold
from vtkmodules.vtkCommonCore import vtkFloatArray
from vtkmodules.vtkCommonDataModel import vtkDataObject, vtkImageData
from vtkmodules.vtkCommonExecutionModel import vtkTrivialProducer
from vtkmodules.vtkFiltersCore import vtkThreshold
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create image data grid.
dim = 128
grid = vtkImageData()
grid.SetOrigin(0.0, 0.0, 0.0)
grid.SetSpacing(1.0, 1.0, 1.0)
grid.SetExtent(0, dim - 1, 0, dim - 1, 0, dim - 1)

# Compute elevation array (distance from origin).
elevation_points = vtkFloatArray()
elevation_points.SetName("Elevation")
num_points = grid.GetNumberOfPoints()
elevation_points.SetNumberOfValues(num_points)
for i in range(num_points):
    pos = grid.GetPoint(i)
    elevation_points.SetValue(i, math.sqrt(pos[0] ** 2 + pos[1] ** 2 + pos[2] ** 2))
grid.GetPointData().AddArray(elevation_points)

# Trivial producer to feed pipeline.
producer = vtkTrivialProducer()
producer.SetOutput(grid)

# Threshold via VTK-m.
threshold = vtkmThreshold()
threshold.SetInputConnection(producer.GetOutputPort())
threshold.AllScalarsOn()
threshold.SetThresholdFunction(vtkThreshold.THRESHOLD_BETWEEN)
threshold.SetLowerThreshold(0.0)
threshold.SetUpperThreshold(100.0)
threshold.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Elevation"
)

# Extract surface.
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(threshold.GetOutputPort())

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())
mapper.ScalarVisibilityOn()
mapper.SetScalarModeToUsePointFieldData()
mapper.SelectColorArray("Elevation")
mapper.SetScalarRange(0.0, 100.0)

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetAmbient(1.0)
actor.GetProperty().SetDiffuse(0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("vtkm threshold")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
