#!/usr/bin/env python

# Draw a closed hexagonal polyline using vtkCellArray line cells.

import math

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
alice_blue_rgb = (0.941, 0.973, 1.0)
background_rgb = (0.102, 0.2, 0.4)

# Data: six vertices of a regular hexagon
c = math.cos(math.pi / 6)
points = vtkPoints()
points.SetNumberOfPoints(6)
points.SetPoint(0, 0.0, -1.0, 0.0)
points.SetPoint(1, c, -0.5, 0.0)
points.SetPoint(2, c, 0.5, 0.0)
points.SetPoint(3, 0.0, 1.0, 0.0)
points.SetPoint(4, -c, 0.5, 0.0)
points.SetPoint(5, -c, -0.5, 0.0)

# Polyline: closed loop through all six vertices and back to start
lines = vtkCellArray()
lines.InsertNextCell(7)
lines.InsertCellPoint(0)
lines.InsertCellPoint(1)
lines.InsertCellPoint(2)
lines.InsertCellPoint(3)
lines.InsertCellPoint(4)
lines.InsertCellPoint(5)
lines.InsertCellPoint(0)

# Assemble the polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetLines(lines)

# Mapper: map the polyline to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(alice_blue_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(background_rgb)
renderer.ResetCamera()

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("PolyLine1")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
