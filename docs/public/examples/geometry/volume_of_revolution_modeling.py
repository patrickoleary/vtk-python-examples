#!/usr/bin/env python

# Demonstrate vtkVolumeOfRevolutionFilter by creating a polydata with
# vertices, lines, polygons, and triangle strips, revolving it 360
# degrees around the Y axis, extracting the surface, and rendering.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints
from vtkmodules.vtkCommonDataModel import (
    vtkCellArray,
    vtkLine,
    vtkPolyData,
    vtkPolyLine,
    vtkPolyVertex,
    vtkPolygon,
    vtkQuad,
    vtkTriangle,
    vtkTriangleStrip,
    vtkVertex,
)
from vtkmodules.vtkFiltersGeometry import vtkDataSetSurfaceFilter
from vtkmodules.vtkFiltersModeling import vtkVolumeOfRevolutionFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Build polydata with various cell types
points = vtkPoints()

# Vertex
vertex = vtkVertex()
vertex.GetPointIds().SetId(0, points.InsertNextPoint(1.0, 1.0, 0.0))

# PolyVertex
poly_vertex = vtkPolyVertex()
poly_vertex.GetPointIds().SetNumberOfIds(2)
poly_vertex.GetPointIds().SetId(0, points.InsertNextPoint(0.25, 0.0, 0.0))
poly_vertex.GetPointIds().SetId(1, points.InsertNextPoint(0.0, 0.35, 0.0))

verts = vtkCellArray()
verts.InsertNextCell(vertex)
verts.InsertNextCell(poly_vertex)

# Line
line = vtkLine()
line.GetPointIds().SetId(0, points.InsertNextPoint(0.75, 0.0, 0.0))
line.GetPointIds().SetId(1, points.InsertNextPoint(1.0, 0.0, 0.0))

# PolyLine
poly_line = vtkPolyLine()
poly_line.GetPointIds().SetNumberOfIds(3)
poly_line.GetPointIds().SetId(0, points.InsertNextPoint(1.5, 2.0, 0.0))
poly_line.GetPointIds().SetId(1, points.InsertNextPoint(1.3, 1.5, 0.0))
poly_line.GetPointIds().SetId(2, points.InsertNextPoint(1.75, 2.0, 0.0))

lines = vtkCellArray()
lines.InsertNextCell(line)
lines.InsertNextCell(poly_line)

# Triangle
triangle = vtkTriangle()
triangle.GetPointIds().SetId(0, points.InsertNextPoint(0.5, -2.0, 0.0))
triangle.GetPointIds().SetId(1, points.InsertNextPoint(1.5, -2.0, 0.0))
triangle.GetPointIds().SetId(2, points.InsertNextPoint(1.5, -1.0, 0.0))

# Quad
quad = vtkQuad()
quad.GetPointIds().SetId(0, points.InsertNextPoint(0.5, -1.0, 0.0))
quad.GetPointIds().SetId(1, points.InsertNextPoint(1.0, -1.0, 0.0))
quad.GetPointIds().SetId(2, points.InsertNextPoint(1.0, 0.2, 0.0))
quad.GetPointIds().SetId(3, points.InsertNextPoint(0.5, 0.0, 0.0))

# Polygon (pentagon)
polygon = vtkPolygon()
polygon.GetPointIds().SetNumberOfIds(5)
polygon.GetPointIds().SetId(0, points.InsertNextPoint(2.0, 2.0, 0.0))
polygon.GetPointIds().SetId(1, points.InsertNextPoint(2.0, 3.0, 0.0))
polygon.GetPointIds().SetId(2, points.InsertNextPoint(3.0, 4.0, 0.0))
polygon.GetPointIds().SetId(3, points.InsertNextPoint(4.0, 6.0, 0.0))
polygon.GetPointIds().SetId(4, points.InsertNextPoint(6.0, 1.0, 0.0))

polys = vtkCellArray()
polys.InsertNextCell(triangle)
polys.InsertNextCell(quad)
polys.InsertNextCell(polygon)

# Triangle strip
triangle_strip = vtkTriangleStrip()
triangle_strip.GetPointIds().SetNumberOfIds(4)
triangle_strip.GetPointIds().SetId(0, points.InsertNextPoint(2.0, 0.0, 0.0))
triangle_strip.GetPointIds().SetId(1, points.InsertNextPoint(2.0, 1.0, 0.0))
triangle_strip.GetPointIds().SetId(2, points.InsertNextPoint(3.0, 0.0, 0.0))
triangle_strip.GetPointIds().SetId(3, points.InsertNextPoint(3.5, 1.0, 0.0))

strips = vtkCellArray()
strips.InsertNextCell(triangle_strip)

# Assemble polydata
poly_data = vtkPolyData()
poly_data.SetPoints(points)
poly_data.SetVerts(verts)
poly_data.SetLines(lines)
poly_data.SetPolys(polys)
poly_data.SetStrips(strips)

# Volume of revolution around Y axis
revolve = vtkVolumeOfRevolutionFilter()
revolve.SetSweepAngle(360.0)
revolve.SetAxisPosition(-1.0, 0.0, 0.0)
revolve.SetAxisDirection(0.0, 1.0, 0.0)
revolve.SetInputData(poly_data)

# Extract surface for rendering
surface = vtkDataSetSurfaceFilter()
surface.SetInputConnection(revolve.GetOutputPort())

# Mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(surface.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)
actor.GetProperty().SetColor(1.0, 0.0, 0.0)

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetSize(300, 300)
render_window.SetWindowName("volume of revolution modeling")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
