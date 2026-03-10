#!/usr/bin/env python

# Render a triangle strip in wireframe using vtkTriangleStrip.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkTriangleStrip,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkDataSetMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
peach_puff_rgb = (1.0, 0.855, 0.725)
dark_green_background_rgb = (0.0, 0.392, 0.0)

# Data: four points forming two adjacent triangles
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(0, 1, 0)
points.InsertNextPoint(1, 0, 0)
points.InsertNextPoint(1.5, 1, 0)

# Cell: a triangle strip with 4 vertices (2 triangles)
triangle_strip = vtkTriangleStrip()
triangle_strip.GetPointIds().SetNumberOfIds(4)
triangle_strip.GetPointIds().SetId(0, 0)
triangle_strip.GetPointIds().SetId(1, 1)
triangle_strip.GetPointIds().SetId(2, 2)
triangle_strip.GetPointIds().SetId(3, 3)

cells = vtkCellArray()
cells.InsertNextCell(triangle_strip)

# Assemble the polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetStrips(cells)

# Mapper: map the triangle strip to graphics primitives
mapper = vtkDataSetMapper()
mapper.SetInputData(poly_data)

# Actor: set visual properties — wireframe representation
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(peach_puff_rgb)
actor.GetProperty().SetRepresentationToWireframe()

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_green_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("TriangleStrip")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
