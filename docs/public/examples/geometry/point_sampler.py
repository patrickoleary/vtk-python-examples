#!/usr/bin/env python

# Demonstrate vtkPolyDataPointSampler by creating synthetic polydata with
# triangles, a quad, a general polygon, and a triangle strip, then sampling
# points with interpolated point data.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkFloatArray, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkPolyDataPointSampler
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create synthetic polydata
points = vtkPoints()
points.SetNumberOfPoints(11)
points.SetPoint(0, 0.0, 0.0, 0.0)
points.SetPoint(1, 1.0, 0.0, 0.0)
points.SetPoint(2, 0.0, 1.0, 0.0)
points.SetPoint(3, 1.0, 1.0, 0.0)
points.SetPoint(4, 0.0, 2.0, 0.0)
points.SetPoint(5, 1.0, 2.0, 0.0)
points.SetPoint(6, 0.0, 3.0, 0.0)
points.SetPoint(7, 1.0, 3.0, 0.0)
points.SetPoint(8, 0.5, 3.5, 0.0)
points.SetPoint(9, 0.0, -1, 0.0)
points.SetPoint(10, 1.0, -1, 0.0)

# Polygon cells (two triangles, a quad, a pentagon)
cells = vtkCellArray()
cells.InsertNextCell(3)
cells.InsertCellPoint(0)
cells.InsertCellPoint(1)
cells.InsertCellPoint(2)
cells.InsertNextCell(3)
cells.InsertCellPoint(2)
cells.InsertCellPoint(1)
cells.InsertCellPoint(3)
cells.InsertNextCell(4)
cells.InsertCellPoint(2)
cells.InsertCellPoint(3)
cells.InsertCellPoint(5)
cells.InsertCellPoint(4)
cells.InsertNextCell(5)
cells.InsertCellPoint(4)
cells.InsertCellPoint(5)
cells.InsertCellPoint(7)
cells.InsertCellPoint(8)
cells.InsertCellPoint(6)

# Triangle strip
strip = vtkCellArray()
strip.InsertNextCell(4)
strip.InsertCellPoint(10)
strip.InsertCellPoint(1)
strip.InsertCellPoint(9)
strip.InsertCellPoint(0)

# Point scalars
scalars = vtkFloatArray()
scalars.SetNumberOfTuples(11)
for i, v in enumerate([0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 0.5, 0.0, 1.0]):
    scalars.SetTuple1(i, v)

# Assemble polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(cells)
poly_data.SetStrips(strip)
poly_data.GetPointData().SetScalars(scalars)

# Point sampler
sampler = vtkPolyDataPointSampler()
sampler.SetInputData(poly_data)
sampler.SetDistance(0.05)
sampler.InterpolatePointDataOn()

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(sampler.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0, 0, 0)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("point sampler")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
