#!/usr/bin/env python

# Render a quadrilateral using vtkQuad.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkPolyData,
    vtkQuad,
)
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
silver_rgb = (0.75, 0.75, 0.75)
salmon_background_rgb = (0.980, 0.502, 0.447)

# Data: four points in counter-clockwise order
points = vtkPoints()
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(1.0, 1.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)

# Cell: a quad referencing the four points
quad = vtkQuad()
quad.GetPointIds().SetId(0, 0)
quad.GetPointIds().SetId(1, 1)
quad.GetPointIds().SetId(2, 2)
quad.GetPointIds().SetId(3, 3)

quads = vtkCellArray()
quads.InsertNextCell(quad)

# Assemble the polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetPolys(quads)

# Mapper: map the quad to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputData(poly_data)

# Actor: set visual properties and color
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(silver_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(salmon_background_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("Quad")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
