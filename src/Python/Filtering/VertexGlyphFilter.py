#!/usr/bin/env python

# Convert bare points to renderable vertex cells using
# vtkVertexGlyphFilter and display them as large yellow dots.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
yellow_rgb = (1.0, 1.0, 0.0)
green_rgb = (0.0, 0.5, 0.0)

# Points: define three positions along the diagonal
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 1, 1)
points.InsertNextPoint(2, 2, 2)

polydata = vtkPolyData()
polydata.SetPoints(points)

# Filter: add vertex cells so points are renderable
vertex_glyph_filter = vtkVertexGlyphFilter()
vertex_glyph_filter.AddInputData(polydata)

# Mapper: map the vertex glyphs to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(vertex_glyph_filter.GetOutputPort())

# Actor: assign the mapped geometry as large points
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetPointSize(10)
actor.GetProperty().SetColor(yellow_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(green_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("VertexGlyphFilter")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
