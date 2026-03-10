#!/usr/bin/env python

# Render 2D points in display coordinates using vtkActor2D and
# vtkPolyDataMapper2D.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor2D,
    vtkPolyDataMapper2D,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
dark_slate_gray_rgb = (0.184, 0.310, 0.310)
gold_rgb = (1.0, 0.843, 0.0)

# Source: create three 2D points in display coordinates
points = vtkPoints()
points.InsertNextPoint(10, 10, 0)
points.InsertNextPoint(100, 100, 0)
points.InsertNextPoint(200, 200, 0)

polydata = vtkPolyData()
polydata.SetPoints(points)

# Filter: convert points to vertex cells for rendering
glyph_filter = vtkVertexGlyphFilter()
glyph_filter.SetInputData(polydata)
glyph_filter.Update()

# Mapper: map 2D polygon data to graphics primitives
mapper = vtkPolyDataMapper2D()
mapper.SetInputConnection(glyph_filter.GetOutputPort())

# Actor: assign the mapped 2D geometry
actor = vtkActor2D()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(gold_rgb)
actor.GetProperty().SetPointSize(8)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(dark_slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("Actor2D")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
