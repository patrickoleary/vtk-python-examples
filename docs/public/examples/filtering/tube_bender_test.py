#!/usr/bin/env python

# Bend tubes around polyline corners using vtkTubeBender
# and render both the original lines and the resulting tubes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkFiltersCore import (
    vtkTubeBender,
    vtkTubeFilter,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build polyline input with two cells
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.5, 0.0, 0.0)
points.InsertNextPoint(0.5, 1.0, 0.0)

points.InsertNextPoint(0.0, 2.0, 0.0)
points.InsertNextPoint(0.0, 3.0, 0.0)
points.InsertNextPoint(0.5, 2.0, 0.0)
points.InsertNextPoint(0.5, 3.0, 0.0)
points.InsertNextPoint(1.5, 3.0, 0.0)
points.InsertNextPoint(2.5, 2.2, 0.0)

cells = vtkCellArray()

# First polyline: 4 points
polyline_0 = vtkPolyLine()
polyline_0.GetPointIds().SetNumberOfIds(4)
polyline_0.GetPointIds().SetId(0, 0)
polyline_0.GetPointIds().SetId(1, 1)
polyline_0.GetPointIds().SetId(2, 2)
polyline_0.GetPointIds().SetId(3, 3)
cells.InsertNextCell(polyline_0)

# Second polyline: 6 points
polyline_1 = vtkPolyLine()
polyline_1.GetPointIds().SetNumberOfIds(6)
polyline_1.GetPointIds().SetId(0, 4)
polyline_1.GetPointIds().SetId(1, 5)
polyline_1.GetPointIds().SetId(2, 6)
polyline_1.GetPointIds().SetId(3, 7)
polyline_1.GetPointIds().SetId(4, 8)
polyline_1.GetPointIds().SetId(5, 9)
cells.InsertNextCell(polyline_1)

line = vtkPolyData()
line.SetPoints(points)
line.SetLines(cells)

# Line actor
line_mapper = vtkPolyDataMapper()
line_mapper.SetInputData(line)

line_actor = vtkActor()
line_actor.GetProperty().SetColor(0.0, 0.0, 0.1)
line_actor.SetMapper(line_mapper)

# Tube bender + tube filter
radius = 0.1

tube_bender = vtkTubeBender()
tube_bender.SetInputData(line)
tube_bender.SetRadius(radius)

tube_filter = vtkTubeFilter()
tube_filter.SetInputConnection(tube_bender.GetOutputPort())
tube_filter.SetRadius(radius)
tube_filter.SetNumberOfSides(50)

tube_mapper = vtkPolyDataMapper()
tube_mapper.SetInputConnection(tube_filter.GetOutputPort())

tube_actor = vtkActor()
tube_actor.GetProperty().SetColor(0.0, 1.0, 0.1)
tube_actor.SetMapper(tube_mapper)
tube_actor.GetProperty().SetOpacity(0.5)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(line_actor)
renderer.AddActor(tube_actor)
renderer.SetBackground(0.5, 0.5, 0.5)

# Window
render_window = vtkRenderWindow()
render_window.SetMultiSamples(0)
render_window.SetSize(500, 500)
render_window.AddRenderer(renderer)
render_window.SetWindowName("tube bender test")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
