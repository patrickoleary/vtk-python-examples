#!/usr/bin/env python

# Test vtkDynamic2DLabelMapper with a spiral of labeled points.

import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

import math

from vtkmodules.vtkCommonCore import (
    vtkPoints,
    vtkStringArray,
)
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkActor2D,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)
from vtkmodules.vtkRenderingLabel import vtkDynamic2DLabelMapper

num_points = 75

# Create spiral polydata
spiral_points = vtkPoints()
spiral_points.SetNumberOfPoints(num_points)

spiral_cells = vtkCellArray()

for i in range(num_points):
    v = 20.0 * float(i) / num_points
    x = v * math.cos(v)
    y = v * math.sin(v)
    spiral_points.SetPoint(i, x, y, 0.0)
    spiral_cells.InsertNextCell(1, [i])

spiral_poly = vtkPolyData()
spiral_poly.SetPoints(spiral_points)
spiral_poly.SetVerts(spiral_cells)

# Add label array
name_array = vtkStringArray()
name_array.SetName("name")
for i in range(num_points):
    name_array.InsertNextValue(str(i))
spiral_poly.GetPointData().AddArray(name_array)

# Dynamic label mapper and actor
label_mapper = vtkDynamic2DLabelMapper()
label_mapper.SetInputData(spiral_poly)

label_actor = vtkActor2D()
label_actor.SetMapper(label_mapper)

# Polydata display mapper and actor
spiral_mapper = vtkPolyDataMapper()
spiral_mapper.SetInputData(spiral_poly)

spiral_actor = vtkActor()
spiral_actor.SetMapper(spiral_mapper)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(label_actor)
renderer.AddActor(spiral_actor)

# Render window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("dynamic2d label mapper")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
