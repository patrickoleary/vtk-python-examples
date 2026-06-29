#!/usr/bin/env python

# Demonstrate vtkContourLoopExtraction with simple incomplete loops that
# touch the boundary, building polydata from hand-crafted line segments
# and extracting contour loops.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create test data with incomplete loops touching the boundary
loop_data = vtkPolyData()
loop_points = vtkPoints()
loop_lines = vtkCellArray()
loop_data.SetPoints(loop_points)
loop_data.SetLines(loop_lines)

loop_points.InsertPoint(0, -1, -2, 0)
loop_points.InsertPoint(1, 1, -2, 0)
loop_points.InsertPoint(2, -1, -1, 0)
loop_points.InsertPoint(3, 1, -1, 0)
loop_points.InsertPoint(4, -2, 0, 0)
loop_points.InsertPoint(5, -1, 0, 0)
loop_points.InsertPoint(6, -1, 0.5, 0)
loop_points.InsertPoint(7, -1, 1, 0)
loop_points.InsertPoint(8, -2, 1, 0)

# Along x-bottom boundary
loop_lines.InsertNextCell(2)
loop_lines.InsertCellPoint(0)
loop_lines.InsertCellPoint(2)

loop_lines.InsertNextCell(2)
loop_lines.InsertCellPoint(3)
loop_lines.InsertCellPoint(1)

loop_lines.InsertNextCell(2)
loop_lines.InsertCellPoint(2)
loop_lines.InsertCellPoint(3)

# Along y-left-side boundary
loop_lines.InsertNextCell(3)
loop_lines.InsertCellPoint(4)
loop_lines.InsertCellPoint(5)
loop_lines.InsertCellPoint(6)

loop_lines.InsertNextCell(2)
loop_lines.InsertCellPoint(6)
loop_lines.InsertCellPoint(7)

loop_lines.InsertNextCell(2)
loop_lines.InsertCellPoint(7)
loop_lines.InsertCellPoint(8)

# Extract contour loops
contour_loops = vtkContourLoopExtraction()
contour_loops.SetInputData(loop_data)

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(contour_loops.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("contour loop boundary")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
