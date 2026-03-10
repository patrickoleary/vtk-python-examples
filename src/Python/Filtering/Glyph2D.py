#!/usr/bin/env python

# Place 2D hexagonal glyphs at three points using vtkGlyph2D with
# a vtkRegularPolygonSource as the glyph shape.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph2D
from vtkmodules.vtkFiltersSources import vtkRegularPolygonSource
from vtkmodules.vtkInteractionStyle import vtkInteractorStyleImage
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
salmon_rgb = (0.980, 0.502, 0.447)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Points: define three positions in the XY plane
points = vtkPoints()
points.InsertNextPoint(0, 0, 0)
points.InsertNextPoint(1, 1, 0)
points.InsertNextPoint(2, 2, 0)

polydata = vtkPolyData()
polydata.SetPoints(points)

# Source: regular hexagonal polygon glyph shape (6 sides by default)
polygon_source = vtkRegularPolygonSource()

# Filter: place 2D glyphs at each point
glyph_2d = vtkGlyph2D()
glyph_2d.SetSourceConnection(polygon_source.GetOutputPort())
glyph_2d.SetInputData(polydata)

# Mapper: map the glyphed output to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(glyph_2d.GetOutputPort())

# Actor: assign the mapped geometry
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(salmon_rgb)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("Glyph2D")

# Interactor: handle mouse and keyboard events with 2D image style
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)
render_window_interactor.SetInteractorStyle(vtkInteractorStyleImage())

# Launch the interactive visualization
render_window_interactor.Initialize()
render_window_interactor.Start()
