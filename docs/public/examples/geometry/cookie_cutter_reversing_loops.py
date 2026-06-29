#!/usr/bin/env python

# Demonstrate vtkCookieCutter with reversing loops and other edge cases
# by creating two quads (one CCW, one CW) and cookie-cutting them with
# a square loop, rendering the result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkCookieCutter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Two quads with different winding orders
polys_data = vtkPolyData()
polys_points = vtkPoints()
polys_polys = vtkCellArray()
polys_data.SetPoints(polys_points)
polys_data.SetPolys(polys_polys)

polys_points.SetNumberOfPoints(8)
polys_points.SetPoint(0, 0.0, 0.0, 0.0)
polys_points.SetPoint(1, 2.0, 0.0, 0.0)
polys_points.SetPoint(2, 2.0, 2.0, 0.0)
polys_points.SetPoint(3, 0.0, 2.0, 0.0)
polys_points.SetPoint(4, -2.0, -2.0, 0.0)
polys_points.SetPoint(5, 0.0, -2.0, 0.0)
polys_points.SetPoint(6, 0.0, 0.0, 0.0)
polys_points.SetPoint(7, -2.0, 0.0, 0.0)

# CCW quad
polys_polys.InsertNextCell(4)
polys_polys.InsertCellPoint(0)
polys_polys.InsertCellPoint(1)
polys_polys.InsertCellPoint(2)
polys_polys.InsertCellPoint(3)

# CW quad (reversed)
polys_polys.InsertNextCell(4)
polys_polys.InsertCellPoint(4)
polys_polys.InsertCellPoint(7)
polys_polys.InsertCellPoint(6)
polys_polys.InsertCellPoint(5)

# Square cookie-cutting loop
loops = vtkPolyData()
loop_points = vtkPoints()
loop_polys = vtkCellArray()
loops.SetPoints(loop_points)
loops.SetPolys(loop_polys)

loop_points.SetNumberOfPoints(4)
loop_points.SetPoint(0, -1, -1, 0)
loop_points.SetPoint(1, 1, -1, 0)
loop_points.SetPoint(2, 1, 1, 0)
loop_points.SetPoint(3, -1, 1, 0)

loop_polys.InsertNextCell(4)
loop_polys.InsertCellPoint(0)
loop_polys.InsertCellPoint(1)
loop_polys.InsertCellPoint(2)
loop_polys.InsertCellPoint(3)

# Cookie cut
cookie = vtkCookieCutter()
cookie.SetInputData(polys_data)
cookie.SetLoopsData(loops)
cookie.Update()

# Cut result
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cookie.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Loop wireframe overlay
loop_mapper = vtkPolyDataMapper()
loop_mapper.SetInputData(loops)

loop_actor = vtkActor()
loop_actor.SetMapper(loop_mapper)
loop_actor.GetProperty().SetColor(1, 0, 0)
loop_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(loop_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cookie cutter reversing loops")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
