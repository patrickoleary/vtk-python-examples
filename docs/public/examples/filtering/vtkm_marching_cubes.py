#!/usr/bin/env python
# Demonstrate vtkmContour (marching cubes) on a Mandelbrot source with elevation coloring.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkAcceleratorsVTKmFilters import vtkmContour
from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkFiltersCore import vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkCountVertices
from vtkmodules.vtkImagingSources import vtkImageMandelbrotSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Mandelbrot source.
src = vtkImageMandelbrotSource()
src.SetWholeExtent(0, 250, 0, 250, 0, 250)

# Secondary elevation field for interpolation.
elevation = vtkElevationFilter()
elevation.SetInputConnection(src.GetOutputPort())
elevation.SetScalarRange(0.0, 1.0)
elevation.SetLowPoint(-1.75, 0.0, 1.0)
elevation.SetHighPoint(0.75, 0.0, 1.0)

# Count vertices (cell data).
count_verts = vtkCountVertices()
count_verts.SetInputConnection(elevation.GetOutputPort())

# Contour via VTK-m.
cubes = vtkmContour()
cubes.SetInputConnection(count_verts.GetOutputPort())
cubes.SetInputArrayToProcess(
    0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "Iterations"
)
cubes.SetNumberOfContours(1)
cubes.SetValue(0, 50.5)
cubes.ComputeScalarsOn()
cubes.ComputeNormalsOn()

# Mapper and actor.
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cubes.GetOutputPort())
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
render_window.SetWindowName("vtkm marching cubes")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
