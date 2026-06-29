#!/usr/bin/env python

# Demonstrate vtkContourLoopExtraction by reading a DEM height field,
# generating contours with vtkFlyingEdges2D, extracting contour loops,
# cookie-cutting glyphed plane points with the loops, and rendering.

import os

# Factory overrides
import vtkmodules.vtkInteractionStyle  # noqa: F401
import vtkmodules.vtkRenderingFreeType  # noqa: F401
import vtkmodules.vtkRenderingOpenGL2  # noqa: F401

from vtkmodules.vtkCommonCore import vtkLookupTable, vtkPoints
from vtkmodules.vtkCommonDataModel import vtkCellArray, vtkPolyData
from vtkmodules.vtkFiltersCore import (
    vtkFlyingEdges2D,
    vtkGenerateIds,
    vtkGlyph3D,
    vtkTriangleFilter,
)
from vtkmodules.vtkFiltersModeling import vtkContourLoopExtraction, vtkCookieCutter
from vtkmodules.vtkFiltersSources import vtkPlaneSource
from vtkmodules.vtkIOImage import vtkDEMReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkPolyDataMapper,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
    vtkRenderer,
)

data_dir = os.environ.get("VPE_DATA_DIR", os.path.dirname(os.path.abspath(__file__)))

# Lookup table
lookup_table = vtkLookupTable()
lookup_table.SetHueRange(0.6, 0)
lookup_table.SetSaturationRange(1.0, 0)
lookup_table.SetValueRange(0.5, 1.0)

# Read DEM height field
dem_reader = vtkDEMReader()
dem_reader.SetFileName(os.path.join(data_dir, "SainteHelens.dem"))
dem_reader.Update()

elevation_low = dem_reader.GetOutput().GetScalarRange()[0]
elevation_high = dem_reader.GetOutput().GetScalarRange()[1]

# Generate contours at midpoint elevation
contours = vtkFlyingEdges2D()
contours.SetInputConnection(dem_reader.GetOutputPort())
contours.SetValue(0, (elevation_high + elevation_low) / 2.0)

# Extract contour loops
loops = vtkContourLoopExtraction()
loops.SetInputConnection(contours.GetOutputPort())
loops.Update()
bounds = loops.GetOutput().GetBounds()

# Plane source for glyph placement
plane = vtkPlaneSource()
plane.SetXResolution(25)
plane.SetYResolution(25)
plane.SetOrigin(bounds[0], bounds[2], bounds[4])
plane.SetPoint1(bounds[1], bounds[2], bounds[4])
plane.SetPoint2(bounds[0], bounds[3], bounds[4])

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

# Glyph the plane points
glyph = vtkGlyph3D()
glyph.SetInputConnection(plane.GetOutputPort())
glyph.SetSourceData(glyph_data)
glyph.SetScaleFactor(100)

# Generate IDs
generate_ids = vtkGenerateIds()
generate_ids.SetInputConnection(glyph.GetOutputPort())
generate_ids.Update()

# Cookie cut with contour loops
cookie = vtkCookieCutter()
cookie.SetInputConnection(generate_ids.GetOutputPort())
cookie.SetLoopsConnection(loops.GetOutputPort())
cookie.PassPointDataOff()
cookie.PassCellDataOff()

# Triangulate for rendering
triangle_filter = vtkTriangleFilter()
triangle_filter.SetInputConnection(cookie.GetOutputPort())

mapper = vtkPolyDataMapper()
mapper.SetInputConnection(triangle_filter.GetOutputPort())
mapper.ScalarVisibilityOff()

actor = vtkActor()
actor.SetMapper(mapper)

# Show the loop
loop_mapper = vtkPolyDataMapper()
loop_mapper.SetInputConnection(loops.GetOutputPort())

loop_actor = vtkActor()
loop_actor.SetMapper(loop_mapper)
loop_actor.GetProperty().SetRepresentationToWireframe()

# Renderer
renderer = vtkRenderer()
renderer.AddActor(actor)
renderer.AddActor(loop_actor)
renderer.SetBackground(0.1, 0.2, 0.4)

# Window
render_window = vtkRenderWindow()
render_window.AddRenderer(renderer)
render_window.SetWindowName("contour loop extraction")

# Scene
renderer.ResetCamera()

# Interactor
interactor = vtkRenderWindowInteractor()
interactor.SetRenderWindow(render_window)

interactor.Initialize()
interactor.Start()
