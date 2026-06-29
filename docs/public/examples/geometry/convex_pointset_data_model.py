#!/usr/bin/env python
# Demonstrate vtkConvexPointSet with elevation scalars, clipping, and contouring.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkConvexPointSet, vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkElevationFilter
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkCamera,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create points in the configuration of an octant with one 2:1 face.
points = vtkPoints()
convex_point_set = vtkConvexPointSet()
points.InsertPoint(0, 0, 0, 0)
points.InsertPoint(1, 1, 0, 0)
points.InsertPoint(2, 1, 1, 0)
points.InsertPoint(3, 0, 1, 0)
points.InsertPoint(4, 0, 0, 1)
points.InsertPoint(5, 1, 0, 1)
points.InsertPoint(6, 1, 1, 1)
points.InsertPoint(7, 0, 1, 1)
points.InsertPoint(8, 0.5, 0, 0)
points.InsertPoint(9, 1, 0.5, 0)
points.InsertPoint(10, 0.5, 1, 0)
points.InsertPoint(11, 0, 0.5, 0)
points.InsertPoint(12, 0.5, 0.5, 0)

for i in range(13):
    convex_point_set.GetPointIds().InsertId(i, i)

convex_grid = vtkUnstructuredGrid()
convex_grid.Allocate(1, 1)
convex_grid.InsertNextCell(convex_point_set.GetCellType(), convex_point_set.GetPointIds())
convex_grid.SetPoints(points)

# Display the cell.
cell_mapper = vtkDataSetMapper()
cell_mapper.SetInputData(convex_grid)
cell_actor = vtkActor()
cell_actor.SetMapper(cell_mapper)
cell_actor.GetProperty().SetColor(0, 1, 0)

# Contour and clip the cell with elevation scalars.
elevation = vtkElevationFilter()
elevation.SetInputData(convex_grid)
elevation.SetLowPoint(-1, -1, -1)
elevation.SetHighPoint(1, 1, 1)
elevation.SetScalarRange(-1, 1)

# Clip.
clip = vtkClipDataSet()
clip.SetInputConnection(elevation.GetOutputPort())
clip.SetValue(0.5)
clip_surface = vtkDataSetSurfaceFilter()
clip_surface.SetInputConnection(clip.GetOutputPort())
clip_mapper = vtkPolyDataMapper()
clip_mapper.SetInputConnection(clip_surface.GetOutputPort())
clip_mapper.ScalarVisibilityOff()
clip_actor = vtkActor()
clip_actor.SetMapper(clip_mapper)
clip_actor.GetProperty().SetColor(1, 0, 0)
clip_actor.AddPosition(2, 0, 0)

# Contour.
contour = vtkContourFilter()
contour.SetInputConnection(elevation.GetOutputPort())
contour.SetValue(0, 0.5)
contour_surface = vtkDataSetSurfaceFilter()
contour_surface.SetInputConnection(contour.GetOutputPort())
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_surface.GetOutputPort())
contour_mapper.ScalarVisibilityOff()
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(1, 0, 0)
contour_actor.AddPosition(1, 2, 0)

renderer = vtkRenderer()
renderer.AddActor(cell_actor)
renderer.AddActor(clip_actor)
renderer.AddActor(contour_actor)
renderer.SetBackground(1, 1, 1)

render_window = vtkRenderWindow()
render_window.SetSize(250, 150)
render_window.AddRenderer(renderer)
render_window.SetWindowName("convex pointset data model")

camera = vtkCamera()
camera.SetFocalPoint(1.38705, 1.37031, 0.639901)
camera.SetPosition(1.89458, -5.07106, -4.17439)
camera.SetViewUp(0.00355726, 0.598843, -0.800858)
camera.SetClippingRange(4.82121, 12.1805)
renderer.SetActiveCamera(camera)
camera.Zoom(1.5)

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
