#!/usr/bin/env python

# Render a single point as a vertex using vtkPolyData.

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
tomato_rgb = (1.0, 0.388, 0.278)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Data: a single point
points = vtkPoints()
pid = points.InsertNextPoint(1.0, 2.0, 3.0)

# Topology: a vertex cell referencing the point
vertices = vtkCellArray()
vertices.InsertNextCell(1, [pid])

# Assemble the polydata
point_poly_data = vtkPolyData()
point_poly_data.SetPoints(points)
point_poly_data.SetVerts(vertices)

# Mapper: map the point polydata to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(point_poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetPointSize(20)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Point")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
