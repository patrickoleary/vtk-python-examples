#!/usr/bin/env python

# Demonstrate vtkFillHolesFilter by creating a grid of quads with some
# cells removed, then filling the resulting holes.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersModeling import vtkFillHolesFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Create a grid of points
poly_data = vtkPolyData()
points = vtkPoints()
polys = vtkCellArray()
poly_data.SetPoints(points)
poly_data.SetPolys(polys)

x_res = 10
y_res = 10
x_points_res = x_res + 1
y_points_res = y_res + 1

# Insert points
for j in range(y_points_res):
    for i in range(x_points_res):
        points.InsertNextPoint(i, j, 0.0)

# Insert cells, skipping some to create holes
skip_ids = {48, 12, 13, 23, 60, 83, 72, 76, 77, 78, 87}
for j in range(1, y_res + 1):
    for i in range(1, x_res + 1):
        cell_id = i - 1 + y_res * (j - 1)
        if cell_id not in skip_ids:
            polys.InsertNextCell(4)
            polys.InsertCellPoint(i - 1 + ((j - 1) * y_points_res))
            polys.InsertCellPoint(i + ((j - 1) * y_points_res))
            polys.InsertCellPoint(i + (j * y_points_res))
            polys.InsertCellPoint(i - 1 + (j * y_points_res))

# Fill the holes
fill = vtkFillHolesFilter()
fill.SetInputData(poly_data)
fill.SetHoleSize(20.0)

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(fill.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1, 0, 0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("fill holes filter")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
