#!/usr/bin/env python

# Demonstrate vtkCookieCutter with special cases like polylines and triangle
# strips by appending hand-crafted line data with a stripped plane, then
# cookie-cutting with a diamond loop.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkAppendPolyData, vtkStripper, vtkTriangleFilter
from vtkmodules.vtkFiltersModeling import vtkCookieCutter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Custom polydata with polylines
lines_data = vtkPolyData()
lines_points = vtkPoints()
lines_lines = vtkCellArray()
lines_data.SetPoints(lines_points)
lines_data.SetLines(lines_lines)

lines_points.InsertPoint(0, -1.0, -1.0, 0.0)
lines_points.InsertPoint(1, 1.0, -1.0, 0.0)
lines_points.InsertPoint(2, 1.0, 1.0, 0.0)
lines_points.InsertPoint(3, -1.0, 1.0, 0.0)
lines_points.InsertPoint(4, -0.2, -0.2, 0.0)
lines_points.InsertPoint(5, 0.0, 0.0, 0.0)
lines_points.InsertPoint(6, 0.2, 0.2, 0.0)

lines_lines.InsertNextCell(3)
lines_lines.InsertCellPoint(1)
lines_lines.InsertCellPoint(5)
lines_lines.InsertCellPoint(3)
lines_lines.InsertNextCell(5)
lines_lines.InsertCellPoint(0)
lines_lines.InsertCellPoint(4)
lines_lines.InsertCellPoint(5)
lines_lines.InsertCellPoint(6)
lines_lines.InsertCellPoint(2)

# Create a triangle strip from a narrow plane
plane = vtkPlaneSource()
plane.SetXResolution(25)
plane.SetYResolution(1)
plane.SetOrigin(-1, -0.1, 0)
plane.SetPoint1(1, -0.1, 0)
plane.SetPoint2(-1, 0.1, 0)

triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(plane.GetOutputPort())

stripper = vtkStripper()
stripper.SetInputConnection(triangle_filter.GetOutputPort())

# Append lines and stripped plane
append = vtkAppendPolyData()
append.AddInputData(lines_data)
append.AddInputConnection(stripper.GetOutputPort())

# Create a diamond loop for cookie cutting
loops = vtkPolyData()
loop_points = vtkPoints()
loop_polys = vtkCellArray()
loops.SetPoints(loop_points)
loops.SetPolys(loop_polys)

loop_points.SetNumberOfPoints(4)
loop_points.SetPoint(0, -0.35, 0.0, 0.0)
loop_points.SetPoint(1, 0, -0.35, 0.0)
loop_points.SetPoint(2, 0.35, 0.0, 0.0)
loop_points.SetPoint(3, 0.0, 0.35, 0.0)

loop_polys.InsertNextCell(4)
loop_polys.InsertCellPoint(0)
loop_polys.InsertCellPoint(1)
loop_polys.InsertCellPoint(2)
loop_polys.InsertCellPoint(3)

# Cookie cut
cookie = vtkCookieCutter()
cookie.SetInputConnection(append.GetOutputPort())
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
render_window.SetWindowName("cookie cutter polylines")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
