#!/usr/bin/env python

# Render a single vertex at the origin using vtkVertex.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkVertex,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Data: a single point at the origin
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)

# Cell: a vertex referencing the point
vertex = vtkVertex()
vertex.GetPointIds().SetId(0, 0)

vertices = vtkCellArray()
vertices.InsertNextCell(vertex)

# Assemble the polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetVerts(vertices)

# Mapper: map the vertex to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(30)
actor.GetProperty().SetColor(peach_puff_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Vertex")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
