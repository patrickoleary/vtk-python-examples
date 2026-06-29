#!/usr/bin/env python
# Demonstrate quadratic polygon cells with clip, contour, outline, and geometry filters.

import math

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkDoubleArray, vtkIdTypeArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkUnstructuredGrid
from vtkmodules.vtkFiltersCore import vtkContourFilter, vtkPolyDataNormals
from vtkmodules.vtkFiltersGeneral import vtkClipDataSet
from vtkmodules.vtkFiltersGeometry import vtkGeometryFilter
from vtkmodules.vtkFiltersModeling import vtkOutlineFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create the quadratic polygon object.
npts = 12
points = vtkPoints()
points.SetNumberOfPoints(npts)

connectivity_quad_poly_1 = []
connectivity_quad_poly_2 = []

ray = 1.0
theta_step = 4.0 * math.pi / npts
for i in range(npts // 2):
    if i < npts // 4:
        theta = theta_step * i * 2
    else:
        theta = theta_step * (i - npts // 4) * 2 + theta_step
    x = ray * math.cos(theta)
    y = ray * math.sin(theta)
    points.SetPoint(i, x, y, 0.0)
    points.SetPoint(npts // 2 + i, x, y, 1.0)
    connectivity_quad_poly_1.append(i)
    connectivity_quad_poly_2.append(npts // 2 + i)

ugrid = vtkUnstructuredGrid()
ugrid.SetPoints(points)

# VTK_QUADRATIC_POLYGON = 36
ugrid.InsertNextCell(36, npts // 2, connectivity_quad_poly_1)
ugrid.InsertNextCell(36, npts // 2, connectivity_quad_poly_2)

# Side quads (VTK_QUAD = 9).
for i in range(npts // 4):
    quad_conn = [
        i,
        (i + 1) % (npts // 4),
        ((i + 1) % (npts // 4)) + npts // 2,
        i + npts // 2,
    ]
    ugrid.InsertNextCell(9, 4, quad_conn)

# Cell ID array for identification.
cell_id_array = vtkIdTypeArray()
cell_id_array.SetName("CellID")
cell_id_array.SetNumberOfComponents(1)
cell_id_array.SetNumberOfTuples(ugrid.GetNumberOfCells())
for i in range(ugrid.GetNumberOfCells()):
    cell_id_array.SetValue(i, i)
ugrid.GetCellData().AddArray(cell_id_array)

# Point scalars.
scalars = vtkDoubleArray()
scalars.SetNumberOfComponents(1)
scalars.SetNumberOfTuples(ugrid.GetNumberOfPoints())
scalars.SetName("Scalars")
scalar_values = [1, 2, 2, 1, 2, 1, 1, 2, 2, 1, 2, 1]
for i, v in enumerate(scalar_values):
    scalars.SetValue(i, v)
ugrid.GetPointData().SetScalars(scalars)

# Clip filter.
clip = vtkClipDataSet()
clip.SetValue(1.5)
clip.SetInputData(ugrid)
clip.Update()
clip_mapper = vtkDataSetMapper()
clip_mapper.SetInputConnection(clip.GetOutputPort())
clip_mapper.SetScalarRange(1.0, 2.0)
clip_mapper.InterpolateScalarsBeforeMappingOn()
clip_actor = vtkActor()
clip_actor.SetPosition(0.0, 2.0, 0.0)
clip_actor.SetMapper(clip_mapper)

# Contour filter.
contour_filter = vtkContourFilter()
contour_filter.SetInputData(ugrid)
contour_filter.SetValue(0, 1.5)
contour_filter.Update()
contour_normals = vtkPolyDataNormals()
contour_normals.SetInputConnection(contour_filter.GetOutputPort())
contour_mapper = vtkPolyDataMapper()
contour_mapper.SetInputConnection(contour_normals.GetOutputPort())
contour_mapper.ScalarVisibilityOff()
contour_actor = vtkActor()
contour_actor.SetMapper(contour_mapper)
contour_actor.GetProperty().SetColor(0, 0, 0)
contour_actor.SetPosition(0.0, 0.01, 0.01)

# Outline filter.
outline_filter = vtkOutlineFilter()
outline_filter.SetInputData(ugrid)
outline_mapper = vtkPolyDataMapper()
outline_mapper.SetInputConnection(outline_filter.GetOutputPort())
outline_actor = vtkActor()
outline_actor.SetMapper(outline_mapper)
outline_actor.GetProperty().SetColor(0, 0, 0)
outline_actor.SetPosition(0.0, 0.01, 0.01)

# Geometry filter.
geometry_filter = vtkGeometryFilter()
geometry_filter.SetInputData(ugrid)
geometry_filter.Update()
geometry_mapper = vtkPolyDataMapper()
geometry_mapper.SetInputConnection(geometry_filter.GetOutputPort())
geometry_mapper.SetScalarRange(1.0, 2.0)
geometry_mapper.InterpolateScalarsBeforeMappingOn()
geometry_actor = vtkActor()
geometry_actor.SetMapper(geometry_mapper)

# Standard rendering pipeline.
renderer = vtkRenderer()
renderer.SetBackground(1, 1, 1)
renderer.AddActor(geometry_actor)
renderer.AddActor(outline_actor)
renderer.AddActor(clip_actor)
renderer.AddActor(contour_actor)

render_window = vtkRenderWindow()
render_window.SetSize(600, 600)
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetWindowName("quadratic polygon filters")

interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
