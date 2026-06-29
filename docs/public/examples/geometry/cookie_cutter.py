#!/usr/bin/env python

# Demonstrate vtkCookieCutter by creating a plane of glyphed points
# with custom glyph geometry (vertices, lines, polygons), defining
# multiple cookie-cutting loops, and rendering the cut result.

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkPoints, vtkUnsignedCharArray
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import vtkGlyph3D
from vtkmodules.vtkFiltersModeling import vtkCookieCutter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

# Plane source for glyph placement
plane = vtkPlaneSource()
plane.SetXResolution(25)
plane.SetYResolution(25)

# Custom glyph with vertex, lines, and polygon
glyph_data = vtkPolyData()
glyph_points = vtkPoints()
glyph_verts = vtkCellArray()
glyph_lines = vtkCellArray()
glyph_polys = vtkCellArray()
glyph_data.SetPoints(glyph_points)
glyph_data.SetVerts(glyph_verts)
glyph_data.SetLines(glyph_lines)
glyph_data.SetPolys(glyph_polys)

glyph_points.InsertPoint(0, -0.5, -0.5, 0.0)
glyph_points.InsertPoint(1, 0.5, -0.5, 0.0)
glyph_points.InsertPoint(2, 0.5, 0.5, 0.0)
glyph_points.InsertPoint(3, -0.5, 0.5, 0.0)
glyph_points.InsertPoint(4, 0.0, -0.5, 0.0)
glyph_points.InsertPoint(5, 0.0, -0.75, 0.0)
glyph_points.InsertPoint(6, 0.5, 0.0, 0.0)
glyph_points.InsertPoint(7, 0.75, 0.0, 0.0)
glyph_points.InsertPoint(8, 0.0, 0.5, 0.0)
glyph_points.InsertPoint(9, 0.0, 0.75, 0.0)
glyph_points.InsertPoint(10, -0.5, 0.0, 0.0)
glyph_points.InsertPoint(11, -0.75, 0.0, 0.0)
glyph_points.InsertPoint(12, 0.0, 0.0, 0.0)
glyph_points.InsertPoint(13, -0.9, 0.0, 0.0)

glyph_verts.InsertNextCell(1)
glyph_verts.InsertCellPoint(12)

glyph_lines.InsertNextCell(2)
glyph_lines.InsertCellPoint(4)
glyph_lines.InsertCellPoint(5)
glyph_lines.InsertNextCell(2)
glyph_lines.InsertCellPoint(6)
glyph_lines.InsertCellPoint(7)
glyph_lines.InsertNextCell(2)
glyph_lines.InsertCellPoint(8)
glyph_lines.InsertCellPoint(9)
glyph_lines.InsertNextCell(3)
glyph_lines.InsertCellPoint(10)
glyph_lines.InsertCellPoint(11)
glyph_lines.InsertCellPoint(13)

glyph_polys.InsertNextCell(4)
glyph_polys.InsertCellPoint(0)
glyph_polys.InsertCellPoint(1)
glyph_polys.InsertCellPoint(2)
glyph_polys.InsertCellPoint(3)

glyph = vtkGlyph3D()
glyph.SetInputConnection(plane.GetOutputPort())
glyph.SetSourceData(glyph_data)
glyph.SetScaleFactor(0.02)

# Create multiple cookie-cutting loops
loops = vtkPolyData()
loop_points = vtkPoints()
loop_polys = vtkCellArray()
loops.SetPoints(loop_points)
loops.SetPolys(loop_polys)

loop_points.SetNumberOfPoints(16)
loop_points.SetPoint(0, -0.35, 0.0, 0.0)
loop_points.SetPoint(1, 0, -0.35, 0.0)
loop_points.SetPoint(2, 0.35, 0.0, 0.0)
loop_points.SetPoint(3, 0.0, 0.35, 0.0)
loop_points.SetPoint(4, -0.35, -0.10, 0.0)
loop_points.SetPoint(5, -0.35, -0.35, 0.0)
loop_points.SetPoint(6, -0.10, -0.35, 0.0)
loop_points.SetPoint(7, 0.35, -0.10, 0.0)
loop_points.SetPoint(9, 0.35, -0.35, 0.0)
loop_points.SetPoint(8, 0.10, -0.35, 0.0)
loop_points.SetPoint(10, 0.35, 0.10, 0.0)
loop_points.SetPoint(11, 0.35, 0.35, 0.0)
loop_points.SetPoint(12, 0.10, 0.35, 0.0)
loop_points.SetPoint(13, -0.35, 0.10, 0.0)
loop_points.SetPoint(14, -0.35, 0.35, 0.0)
loop_points.SetPoint(15, -0.10, 0.35, 0.0)

loop_polys.InsertNextCell(4)
loop_polys.InsertCellPoint(0)
loop_polys.InsertCellPoint(1)
loop_polys.InsertCellPoint(2)
loop_polys.InsertCellPoint(3)

for tri_pts in [(4, 5, 6), (7, 8, 9), (10, 11, 12), (13, 14, 15)]:
    loop_polys.InsertNextCell(3)
    loop_polys.InsertCellPoint(tri_pts[0])
    loop_polys.InsertCellPoint(tri_pts[1])
    loop_polys.InsertCellPoint(tri_pts[2])

# Cookie cut
cookie = vtkCookieCutter()
cookie.SetInputConnection(glyph.GetOutputPort())
cookie.SetLoopsData(loops)
cookie.Update()

# Assign cell colors
num_cells = glyph.GetOutput().GetNumberOfCells()
glyph_scalars = vtkUnsignedCharArray()
glyph_scalars.SetNumberOfComponents(4)
glyph_scalars.SetNumberOfTuples(num_cells)
for i in range(num_cells):
    glyph_scalars.SetTuple4(i, 127, 207, 80, 127)
cookie.GetOutput().GetCellData().SetScalars(glyph_scalars)

# Cut result mapper and actor
mapper = vtkPolyDataMapper()
mapper.SetInputConnection(cookie.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

# Loop wireframe overlay
loop_mapper = vtkPolyDataMapper()
loop_mapper.SetInputData(loops)

loop_actor = vtkActor()
loop_actor.SetMapper(loop_mapper)
loop_actor.GetProperty().SetColor(1, 0, 0)
loop_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(loop_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("cookie cutter")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
