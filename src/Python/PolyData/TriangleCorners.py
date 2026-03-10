#!/usr/bin/env python

# Store three triangle corner points in a polydata, write to a .vtp file, and render.

# Factory overrides: importing these modules registers the OpenGL rendering
# and interaction style implementations for vtkRenderingCore factory classes.
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401
# VTK pipeline classes used in this example
from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import vtkPolyData
from vtkmodules.vtkFiltersGeneral import vtkVertexGlyphFilter
from vtkmodules.vtkIOXML import vtkXMLPolyDataWriter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Colors (normalized RGB)
tomato_rgb = (1.000, 0.388, 0.278)
slate_gray_rgb = (0.439, 0.502, 0.565)

# Source: three points (no topology)
points = vtkPoints()
points.InsertNextPoint(1.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 0.0, 0.0)
points.InsertNextPoint(0.0, 1.0, 0.0)

polydata = vtkPolyData()
polydata.SetPoints(points)

# Writer: save to VTP
writer = vtkXMLPolyDataWriter()
writer.SetFileName("TriangleCorners.vtp")
writer.SetInputData(polydata)
writer.Write()

# Filter: create vertex cells so the points are renderable
vertex_glyph = vtkVertexGlyphFilter()
vertex_glyph.SetInputData(polydata)

# Mapper: map vertex cells to graphics primitives
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(vertex_glyph.GetOutputPort())

# Actor: render the points with visible point size
actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(tomato_rgb)
actor.GetProperty().SetPointSize(10)

# Renderer: assemble the scene
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(slate_gray_rgb)

# Window: display the rendered scene
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(640, 480)
render_window.SetWindowName("TriangleCorners")

# Interactor: handle mouse and keyboard events
render_window_interactor = vtkRenderWindowInteractor()
render_window_interactor.SetRenderWindow(render_window)

# Launch the interactive visualization
render_window.Render()
render_window_interactor.Start()
