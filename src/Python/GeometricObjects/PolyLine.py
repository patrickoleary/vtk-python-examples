#!/usr/bin/env python

# Connect five points with a polyline using vtkPolyLine.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkPolyLine,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.0, 0.388, 0.278)
dark_olive_green_background_rgb = (0.333, 0.420, 0.184)

# Data: five points forming a path
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 2.0)
points.InsertNextPoint(1.0, 2.0, 3.0)

# Polyline: connect all five points in order
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(5)
poly_line.GetPointIds().SetId(0, 0)
poly_line.GetPointIds().SetId(1, 1)
poly_line.GetPointIds().SetId(2, 2)
poly_line.GetPointIds().SetId(3, 3)
poly_line.GetPointIds().SetId(4, 4)

cells = vtkCellArray()
cells.InsertNextCell(poly_line)

# Assemble the polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetLines(cells)

# Mapper: map the polyline to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_olive_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("PolyLine")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
